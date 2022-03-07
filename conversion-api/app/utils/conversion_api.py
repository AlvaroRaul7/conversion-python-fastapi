
import pandas as pd
import requests as request
async def get_fixer():
    api = pd.read_json('http://data.fixer.io/api/latest?access_key=cff4598196216dd82b488716c8ce80f6&symbols=MXN')
    df = pd.DataFrame(api)
    fixer_api = df.date
    fixer_api = fixer_api[0].date().strftime("%d/%m/%y")
    value_fixer_api = df.rates
    value_fixer_api = value_fixer_api.values[0]

    return fixer_api,value_fixer_api


async def get_xml_banxico():
    df = pd.read_html('https://www.banxico.org.mx/tipcamb/tipCamMIAction.do') 
    df_values = df[6].values 
    df = pd.DataFrame(data=df_values)
    df.to_csv('values.csv')
    df = df.dropna()
    df = df.loc[0:2]
    array = df.to_numpy()
    split_str = str(array[0]).split(" ")
    print(split_str)
    banxico_xml = split_str[16]
    banxico_xml_value = split_str[20]
    print(banxico_xml)
    return banxico_xml,banxico_xml_value


async def get_api_banxico():
    token= '8413fcf915ea661fbc6749d4962599093f13e4ea670815b2f261e0b96523b793'
    url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token=%s'% token
    data = request.get(url)
    dict_j  = data.json()
    for value in dict_j.values():
        for v in value.values():
            for k in v:
                info = k['datos']
                data = dict(info[0])
                value_banxico_api = data['dato']
                date_banxico_api = data['fecha']
    
    return value_banxico_api,date_banxico_api
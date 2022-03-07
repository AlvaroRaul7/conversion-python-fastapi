
import sys
import requests as request
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
import socket

import pandas as pd

app = FastAPI()
hostname = socket.gethostname()
version = f"{sys.version_info.major}.{sys.version_info.minor}"

from utils.conversion_api import get_fixer,get_xml_banxico, get_api_banxico

@app.get("/")
async def get_mexican_conversion():

    """ Call method async  fixer api to get values """
    fixer_api,value_fixer_api = await get_fixer()

    """ Call method async banxico xml to get values"""

    banxico_xml, banxico_xml_value = await get_xml_banxico()
    
    """ Api Rest Banxico"""

    value_banxico_api, date_banxico_api= await get_api_banxico()
        
    response = {
            "rates": {
                'provider_1':{
                    'last_update':fixer_api,
                    'value': value_fixer_api,
                },
                'provider_2_variant_1':{
                    'last_update': banxico_xml,
                    'value': float(banxico_xml_value),
                },
                'provider_2_variant_2':{
                    'last_update': date_banxico_api,
                    'value': float(value_banxico_api),
                }
            }
        }   
    return response


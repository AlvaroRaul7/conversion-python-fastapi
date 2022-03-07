

from utils.conversion_api import get_fixer,get_xml_banxico, get_api_banxico
from typing import Optional
from datetime import datetime, timedelta,date
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

from db.controller import UserInDB,fake_users_db,Token, TokenData,User
import pandas as pd







# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "fb749cfa7c7b7b87d298431abaa28470c306ba0838ee31e7defaf64af939a588"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")






pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

RATE_LIMIT={}
COUNT_RATE_LIMIT = 0



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]



@app.get("/")
async def get_mexican_conversion(current_user: User = Depends(get_current_active_user)):

    print(current_user.username)
    access_log= pd.read_csv("./db/access_log.csv")
    # print(access_log)
    today = date.today()
    
    check_login =access_log.loc[(access_log['username'] == current_user.username) & (access_log['date'] == str(today))]
    
    if(len(check_login) >= 10):
        return {
            "error": "Maximum rate limit exceeded per day (10 requests per day and per user)"
        }
    
    else:
        new_access = pd.DataFrame({'username': [current_user.username],  'date' : [str(today)]})
        df = pd.concat([access_log, new_access], ignore_index = True, axis = 0)
        print(df)
        df.to_csv("./db/access_log.csv", index=False)

    

    """ Call method async  fixer api to get values """
    fixer_api,value_fixer_api = await get_fixer()

    """ Call method async banxico xml to get values"""

    banxico_xml, banxico_xml_value = await get_xml_banxico()
    
    """ Call method async banxico api rest to get values"""

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


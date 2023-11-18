from fastapi import APIRouter, Depends, HTTPException, status 
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError
from passlib.context import CryptContext

from datetime import datetime, timedelta

ALGORITMO = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "644754187383941c61a64b221caf6c915246ccb29f7b30a923b947a6d9ad24b2"

router = APIRouter()

oauth = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password:str


users_db = {
    'luismm':{
        'username':'luismm',
        'fullname':'Luis Martel',
        'email':'luismm@gmail.com',
        'disabled': False,
        'password':'$2a$12$2CrHjtIe1G6I710mxjLRmeUO4qicssJzqGmHR9EeNdwOBYE0BoLv6'
    },
    'Edith9':{
        'username':'luismm95',
        'fullname':'Luis Martel',
        'email':'edith9@gmail.com',
        'disabled': True,
        'password':'$2a$12$WdQrY616Ugej9vC3PHtlHuix5Y3zugRKfByyKQubLWuwKjg.EIhMe'
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token : str = Depends(oauth)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Credenciales Invalidas', 
                            headers={'WWW-Authenticate':'Bearer'})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITMO]).get('sub')
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)
        

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Usuario Inactivo')
    return user


@router.post('/login')
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El Usuario No es correcto')

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La password no es Correcta!')

    access_token =  {'sub':user.username,
                      'exp':datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    
    return {'access_token': jwt.encode(access_token,SECRET,  algorithm=ALGORITMO), 'token_type':'bearer'}

@router.get('/users/me')
async def me(user:User = Depends(current_user)):
    return user
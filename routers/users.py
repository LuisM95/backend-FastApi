from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()

#User entity
class User(BaseModel):
    id : int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id = 1, name='Meli', surname='Perez', url='https://perezm.dev', age=16),
         User(id = 2, name='Luis', surname='Martel', url='https://martel.dev', age=28),
         User(id = 3 ,name='Enrique', surname='Mun', url='https://martel.mun.dev', age=30),
         User(id = 4 ,name='Edith', surname='Martel', url='https://martel-edith.dev', age=35)]


@router.get('/usersjson')
async def usersjson():
    return [{'id' : 2, 'name':'Luis', 'surname':'Martel', 'url':'https://martel.dev', 'age':28 },
            {'id' : 3,'name':'Enrique', 'surname':'Mun', 'url':'https://martel.mun.dev', 'age':30},
            {'id': 4,'name':'Edith', 'surname':'Martel', 'url':'https://martel-edith.dev', 'age':35},]

@router.get('/users')
async def users():
    return users_list

#path
@router.get('/user/{id}')
async def user(id:int):
    return search_user(id)
    
#query
@router.get('/user/')
async def user(id:int):
    return search_user(id)


def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el Usuario!"}


@router.post('/user/', status_code=201)
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El Usuario ya Existe!")
    
    users_list.append(user)
    return user

@router.put('/user/')
async def user(user : User):

    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "Usuario no encontrado"}
    
    return user

@router.delete('/user/{id}')
async def user(id:int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
        return {"Message":"Usuario Eliminado con Exito!"}

    if not found:
        return {"error": "No se ha Eliminado el Usuario"}

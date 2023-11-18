from fastapi import APIRouter

router = APIRouter(prefix='/products',
                   tags=['products'], 
                   responses={404: {'Message':'No encontrado'}})

products_list = ['Product 1', 'Product 2', 'Product 3', 'Product 4']

@router.get('/')
async def products():
    return products_list

@router.get('/{id:int}')
async def product(id:int):
    return products_list[id]
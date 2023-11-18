from fastapi import FastAPI
from routers import products, users, jwt_users, auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(jwt_users.router)
app.include_router(auth_users.router)
app.include_router(users_db.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/url')
async def url():
    return {'url': 'https://mouredev.com/python'}
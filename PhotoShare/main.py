import uvicorn
import fastapi

from fastapi import FastAPI

from src.routes import auth, users, shares, comments, public, admin


app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(shares.router, prefix='/api')
app.include_router(comments.router, prefix='/api')
app.include_router(public.router, prefix='/api/recomendations')
app.include_router(admin.router, prefix='/api/admin-moder')

@app.get('/')
def read_root():
    '''main page'''
    return {'message': 'Main page'}



if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
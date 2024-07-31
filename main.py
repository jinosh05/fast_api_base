from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

@app.get('/')
def get_home():
    return { "status":"OK", "message": "Welcome to Home Page"}
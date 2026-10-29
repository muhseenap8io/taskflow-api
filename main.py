from fastapi import FastAPI

app= FastAPI()

@app.get('/')
async def root():
    return {"message":"Taskflow Api server is running"}
from fastapi import FastAPI
from tinydb import TinyDB
from datetime import datetime

app = FastAPI()

db = TinyDB("db.json")

@app.get("/")
def home():
    return {"message": "Weather API Running"}

@app.post("/weather")
def add_weather(temperature: float, humidity: float):

    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "humidity": humidity
    }

    db.insert(data)

    return {
        "status": "saved",
        "data": data
    }

@app.get("/weather")
def get_weather():
    return db.all()
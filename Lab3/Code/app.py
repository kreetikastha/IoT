from fastapi import FastAPI
from tinydb import TinyDB
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

db = TinyDB("db.json")

@app.get("/")
def home():
    return {"message": "Weather API Running"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/index.html")


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
def get_weather(start: str = None, end: str = None):

    data = db.all()

    if not start or not end:
        return data

    filtered = []

    for row in data:

        if start <= row["timestamp"] <= end:
            filtered.append(row)

    return filtered
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Pomodoro Timer API")

class TimerSettings(BaseModel):
    work: int
    break_time: int

timer = {
    "work": 25,
    "break": 5,
    "current_time": "25:00",
    "running": False,
    "mode": "Work Session"
}

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Pomodoro Timer</title>
<style>
body {{
    background:#ff6f91;
    font-family:Arial;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}}

.card {{
    background:#ff87a5;
    padding:30px;
    border-radius:20px;
    width:320px;
    text-align:center;
    color:white;
    box-shadow:0 10px 25px rgba(0,0,0,.2);
}}

button {{
    padding:10px 20px;
    margin:5px;
    border:none;
    border-radius:10px;
    cursor:pointer;
    font-size:16px;
}}

input {{
    width:60px;
    padding:5px;
    text-align:center;
}}

</style>
</head>

<body>

<div class="card">

<h1>🍅 Pomodoro Timer</h1>

<h3 id="mode">{timer["mode"]}</h3>

<h1 id="time">{timer["current_time"]}</h1>

<button onclick="start()">Start</button>
<button onclick="pause()">Pause</button>
<button onclick="reset()">Reset</button>

<br><br>

<label>Work</label>
<input id="work" value="{timer["work"]}">

<label>Break</label>
<input id="break" value="{timer["break"]}">

<br><br>

<button onclick="save()">Save Settings</button>

</div>

<script>

async function refresh(){
let r=await fetch('/timer');
let d=await r.json();
document.getElementById('mode').innerHTML=d.mode;
document.getElementById('time').innerHTML=d.time;
}

async function start(){
await fetch('/start',{method:'POST'});
refresh();
}

async function pause(){
await fetch('/pause',{method:'POST'});
refresh();
}

async function reset(){
await fetch('/reset',{method:'POST'});
refresh();
}

async function save(){

let work=document.getElementById('work').value;
let br=document.getElementById('break').value;

await fetch('/settings',{

method:'POST',

headers:{
'Content-Type':'application/json'
},

body:JSON.stringify({

work:Number(work),
break_time:Number(br)

})

});

refresh();

}

</script>

</body>
</html>
"""

@app.get("/timer")
def timer_api():
    return {
        "mode": timer["mode"],
        "time": timer["current_time"],
        "work": timer["work"],
        "break": timer["break"],
        "running": timer["running"]
    }

@app.post("/start")
def start():
    timer["running"] = True
    return {"message":"started"}

@app.post("/pause")
def pause():
    timer["running"] = False
    return {"message":"paused"}

@app.post("/reset")
def reset():
    timer["running"] = False
    timer["mode"] = "Work Session"
    timer["current_time"] = f"{timer['work']:02}:00"
    return {"message":"reset"}

@app.post("/settings")
def settings(data: TimerSettings):
    timer["work"] = data.work
    timer["break"] = data.break_time
    timer["current_time"] = f"{data.work:02}:00"
    return {"message":"updated"}
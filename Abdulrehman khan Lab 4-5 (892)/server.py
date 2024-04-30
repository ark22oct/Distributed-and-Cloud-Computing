from fastapi import FastAPI, HTTPException
from typing import List, Optional
import uvicorn
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Route to serve the index.html file
@app.get("/")
async def get_index():
    return FileResponse("index.html")

# Global variables to store mines and rovers data
mines = {}
rovers = {}

# Models
class MineCreate(BaseModel):
    x: int
    y: int
    serial: str

class MineUpdate(BaseModel):
    x: Optional[int] = None
    y: Optional[int] = None
    serial: Optional[str] = None

class RoverCreate(BaseModel):
    commands: str

class RoverCommands(BaseModel):
    commands: str

# Map Endpoints
@app.get("/map")
async def get_map():
    with open("map.txt", 'r') as file:
        lines = file.readlines()
        map_data = [[int(num) for num in line.split()] for line in lines]
    return {"map": map_data}

@app.put("/map")
async def update_map(new_map: List[List[int]]):
    global map_data
    if not new_map or not all(isinstance(row, list) and len(row) == len(new_map[0]) for row in new_map):
        raise HTTPException(status_code=400, detail="Invalid map dimensions")
    
    map_data = new_map
    return {"message": "Map dimensions updated successfully", "new_map": map_data}

# Mines Endpoints
@app.get("/mines")
async def get_mines():
    mines_dict = {}
    with open("mines.txt", 'r') as file:
        for line in file:
            serial, name = line.strip().split(',')
            mines_dict[serial] = name
    return {"mines": mines}

@app.get("/mines/{mine_id}")
async def get_mine_by_id(mine_id: str):
    if mine_id in mines:
        return {"serial": mine_id, "name": mines[mine_id]}
    else:
        return {"error": "Mine not found"}

@app.put("/mines/{mine_id}")
async def update_mine(mine_id: str, mine_data: MineUpdate):
    if mine_id not in mines:
        raise HTTPException(status_code=404, detail="Mine not found")

    mine = mines[mine_id]
    if mine_data.x is not None:
        mine["x"] = mine_data.x
    if mine_data.y is not None:
        mine["y"] = mine_data.y
    if mine_data.serial is not None:
        mine["serial"] = mine_data.serial

    return mine

@app.delete("/mines/{mine_id}")
async def delete_mine(mine_id: str):
    if mine_id not in mines:
        raise HTTPException(status_code=404, detail="Mine not found")

    del mines[mine_id]
    return {"message": "Mine deleted successfully"}

@app.post("/mines")
async def create_mine(mine: MineCreate):
    global mines
    x, y, serial = mine.x, mine.y, mine.serial
    
    if serial in mines:
        raise HTTPException(status_code=400, detail="Mine with the same serial already exists")
    
    mines[serial] = {"x": x, "y": y}
    return {"message": "Mine created successfully", "serial": serial}

# Rovers Endpoints
@app.get("/rovers")
def get_rovers():
    return rovers

@app.get("/rovers/{id}")
def get_rover_by_id(id: str):
    if id in rovers:
        return rovers[id]
    else:
        raise HTTPException(status_code=404, detail="Rover not found")

@app.post("/rovers")
def create_rover(rover: RoverCreate):
    global rovers
    commands = rover.commands
    rover_id = len(rovers) + 1
    rover = {"id": rover_id, "commands": commands, "status": "Not Started", "position": (0, 0)}
    rovers[str(rover_id)] = rover
    return rover

@app.delete("/rovers/{id}")
def delete_rover(id: str):
    if id in rovers:
        del rovers[id]
        return {"message": "Rover deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Rover not found")

@app.post("/rovers/{id}")
def send_commands_to_rover(id: str, rover_commands: RoverCommands):
    if id not in rovers:
        raise HTTPException(status_code=404, detail="Rover not found")

    rover = rovers[id]
    if rover["status"] in ["Not Started", "Finished"]:
        rover["commands"] = rover_commands.commands
        rover["status"] = "Moving"
        return {"message": "Commands sent to rover successfully"}
    else:
        raise HTTPException(status_code=400, detail="Rover is already in motion")


@app.post("/rovers/{id}/dispatch")
def dispatch_rover(id: str):
    if id not in rovers:
        raise HTTPException(status_code=404, detail="Rover not found")

    rover = rovers[id]
    if rover["status"] == "Not Started":
        rover["status"] = "Moving"
        # Implement rover dispatching and simulation here
        rover["status"] = "Finished"  # Placeholder, replace with actual logic
        return rover
    else:
        raise HTTPException(status_code=400, detail="Rover is already in motion")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
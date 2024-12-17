import fastapi
import os
import json
import hashlib

from fastapi import HTTPException

if os.path.isfile("Templates/templates.json"):
    with open("Templates/templates.json", "r") as file:
        templates = str(json.load(file))
        templateHash = hashlib.sha256(templates.encode('utf-8')).hexdigest()
else:
    templates = None
    templateHash = None

app = fastapi.FastAPI()

@app.get("/")
def get_templates():
    if templates is None:
        raise HTTPException(status_code=500, detail="Template neexistuje")
    return templates

@app.get("/check/{sha256hash}")
def check_hash(sha256hash : str):
    if templateHash is None:
        raise HTTPException(status_code=500, detail="Template neexistuje")
    elif templateHash != sha256hash:
        raise HTTPException(status_code=500, detail="Hash se neshoduje")
    return "OK"
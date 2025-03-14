import base64
import hashlib
import os

import fastapi
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from fastapi import HTTPException, Request

from db_lib import DB_handler

if os.path.isfile("Templates/templates.json"):
    with open("Templates/templates.json", "r") as file:
        templates = file.readline()
        file.seek(0)
        templateHash = hashlib.sha256(file.readline().encode("utf-8")).hexdigest()
    if os.path.isfile("tajnykod.txt"):
        with open("tajnykod.txt", "r") as file:
            tajnyKod = hashlib.sha256(file.readline().encode("utf-8")).digest()
            algo = algorithms.AES256(tajnyKod)
            cipher = Cipher(algo, mode=modes.ECB())
            padder = padding.PKCS7(algo.block_size).padder()
            data = padder.update(templates.encode("utf-8"))
            data += padder.finalize()
            templates = base64.b64encode(cipher.encryptor().update(data)).decode()

    else:
        templates = None
        templateHash = None
        tajnyKod = None
        cipher = None
        algo = None
else:
    templates = None
    templateHash = None
    tajnyKod = None
    cipher = None
    algo = None

db = DB_handler()


def VratUserPassw(usr: str, passw: str) -> (str, str):
    if cipher is None:
        return None, None
    unpadder = padding.PKCS7(algo.block_size).unpadder()
    usr = unpadder.update(cipher.decryptor().update(base64.b64decode(usr)))
    usr += unpadder.finalize()
    usr = usr.decode()
    unpadder = padding.PKCS7(algo.block_size).unpadder()
    passw = unpadder.update(cipher.decryptor().update(base64.b64decode(passw)))
    passw += unpadder.finalize()
    passw = passw.decode()
    return usr, passw


app = fastapi.FastAPI()


@app.get("/")
def get_templates(request: Request):
    if templates is None:
        raise HTTPException(status_code=500, detail="Template neexistuje")
    usr = request.headers.get("Username")
    passw = request.headers.get("Password")
    token = request.headers.get("Token")
    if (usr is None or passw is None or token is None):
        raise HTTPException(status_code=401, detail="Headery nejsou vyplněné")
    if (cipher is None):
        raise HTTPException(status_code=500, detail="Server je špatně nastaven")
    unpadder = padding.PKCS7(algo.block_size).unpadder()
    token = cipher.decryptor().update(base64.b64decode(token))
    data = unpadder.update(token)
    try:
        data += unpadder.finalize()
        if (data.decode() != "OK"):
            raise HTTPException(status_code=401, detail="Tajný kód se neshoduje")
    except:
        raise HTTPException(status_code=401, detail="Tajný kód se neshoduje")
    usr, passw = VratUserPassw(usr, passw)
    if db.JeUzivatelRegistrovan(usr, hashlib.sha256(passw.encode("utf-8")).hexdigest()):
        return templates
    elif db.JeUzivatelCekajici(usr, hashlib.sha256(passw.encode("utf-8")).hexdigest()):
        raise HTTPException(status_code=403, detail="Uživatel není potvrzen")
    else:
        raise HTTPException(status_code=401, detail="Uživatel není registrován")


@app.get("/check/{sha256hash}")
def check_hash(sha256hash: str):
    if templateHash is None:
        raise HTTPException(status_code=500, detail="Template neexistuje")
    elif templateHash != sha256hash:
        raise HTTPException(status_code=500, detail="Hash se neshoduje")
    return "OK"


@app.post("/register")
def registruj(request: Request):
    usr = request.headers.get("Username")
    passw = request.headers.get("Password")
    token = request.headers.get("Token")
    if (usr is None or passw is None or token is None):
        raise HTTPException(status_code=401, detail="Headery nejsou vyplněné")
    if (cipher is None):
        raise HTTPException(status_code=500, detail="Server je špatně nastaven")
    unpadder = padding.PKCS7(algo.block_size).unpadder()
    token = cipher.decryptor().update(base64.b64decode(token))
    data = unpadder.update(token)
    try:
        data += unpadder.finalize()
        if (data.decode() != "OK"):
            raise HTTPException(status_code=401, detail="Tajný kód se neshoduje")
    except:
        raise HTTPException(status_code=401, detail="Tajný kód se neshoduje")
    usr, passw = VratUserPassw(usr, passw)
    if not db.VlozCekajiciho(usr, hashlib.sha256(passw.encode("utf-8")).hexdigest()):
        raise HTTPException(status_code=401, detail="Uživatelské jméno již bylo použito")

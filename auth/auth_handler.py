import time
from typing import Dict
import jwt

JWT_SECRET = 'super_secret'


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET)
    return {"access_token": token}


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET,algorithms=["HS256"])
        if decoded_token["expires"] >= time.time():
            return decoded_token 
        else: 
            return None
    except:
        return {}

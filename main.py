from fastapi import FastAPI, File, HTTPException, status, Depends
from PIL import Image
import PIL.ImageOps
import io
from fastapi.responses import StreamingResponse
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
from pydantic import BaseModel

fake_users_db = {
    "user123": {
        "username": "user123",
        "hashed_password": "fakehashedpass321!",
        "disabled": False,
    },

}

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/prime/{number}", tags=["prime number checker"])
def is_number_prime(number):
    if number.isnumeric():
        num = int(number)
        if num > 9223372036854775807:
            return "Number out of range"
        elif num <= 1:
            return "Number is not prime"
        flag = False
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    flag = True
                    break
        if (flag == True):
            return "Number is not prime"
        else:
            return "Number is prime"
    else:
        return "Number has to be an integer from range (1,9223372036854775807)"


@app.post("/picture/invert", tags=["picture inversion"])
def picture_inversion(file: bytes = File(...)):
    inverted_img = PIL.ImageOps.invert(Image.open(io.BytesIO(file)))
    converted_img = io.BytesIO()
    inverted_img.save(converted_img, format='JPEG')
    converted_img.seek(0)
    return StreamingResponse(converted_img, media_type="image/jpeg")


def fake_hash_password(password: str):
    return "fakehashed" + password


class User(BaseModel):
    username: str
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/time", tags=["current time"])
async def login_to_date(form_data: OAuth2PasswordRequestForm = Depends()):
    """To log in use username: user123, password: pass321!"""
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

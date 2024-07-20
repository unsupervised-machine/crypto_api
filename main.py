from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from crypto_api.database import (get_user, insert_user, get_user_portfolio, update_portfolio, update_current_only_data,
                                 get_all_current_only)

SECRET_KEY = "123secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_db
# db = {
#     "tim": {
#         "username": "tim",
#         "full_name": "Tim Lau",
#         "email": "Tim@gmail.com",
#         "hashed_password": "$2b$12$jNs9VEELX9MxVTKXmVvsTuSzrnXAi7EbrQo675SaWBUxqW90grLs6",
#         "disabled": False,
#     }
# }

# -- Response Models -- #


class FavoritesResponse(BaseModel):
    favorites: List[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class User(BaseModel):
    username: str
    email: str or None = None
    # full_name: str or None = None
    disabled: bool or None = None


class SignUpResponse(BaseModel):
    success: bool
    message: str


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")



app = FastAPI()
# to start app run following command in terminal:
# uvicorn main:app --reload


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_db(username: str):
    user_data = get_user(username)
    return UserInDB(**user_data)


def authenticate_user(username: str, password: str):
    user = get_user_db(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oath2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"}
                                         )

    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exception

    user = get_user_db(username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    print("access_token: ", access_token)

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup", response_model=SignUpResponse)
async def sign_up(
        email: Annotated[str, Form()],
        first_name: Annotated[str, Form()],
        last_name: Annotated[str, Form()],
        username: Annotated[str, Form()],
        plain_password: Annotated[str, Form()],
):
    try:
        result = insert_user(email, first_name, last_name, username, plain_password)
        if result == True:
            return SignUpResponse(success=True, message="User successfully signed registered.")
        elif result == "Duplicate key error":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or username already registered."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User registration failed due to a database error."
            )
    except HTTPException as e:
        # Re-raise HTTPException to return the correct status code
        raise e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.post("/users/me/favorites/add")
async def set_favorites(
        favorites: Annotated[list, Form()],
        current_user: User = Depends(get_current_active_user),
                        ):
    update_portfolio(username=current_user.username, set_favorites=favorites)


@app.post("/crypto/current_only/update_db")
async def current_only_update_db():
    update_current_only_data()


@app.get("/crypto/current_only/from_db")
async def current_only_from_db():
    data = get_all_current_only()
    return data


@app.get("/users/me/", response_model=User)
# make sure to sign in via the "Authorize" button first
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]


@app.get("/users/me/favorites")
async def read_favorites(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves the favorites field from the user's portfolio.
    :param current_user:
    :return: A list of favorite items. Returns an empty list if the user or the favorites field is not found.
    """
    result = get_user_portfolio(current_user.username)
    if result:
        return result.get("favorites", [])
    return []


if __name__ == "__main__":
    test = get_user_db("taran50")
    print(test)
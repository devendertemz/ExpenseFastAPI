# function that help use to perforom jwt operations like encoding and decoding the jwt token
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException,status
from jose import jwt


SCRET_KEY = "asdfghjkjhgfdsdfghjhgfdfghtrd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#create access token
def create_access_token (data: dict,exprires_delta: timedelta | None = None):
    to_encode = data.copy()
    if exprires_delta:
        expire = datetime.now(timezone.utc) + exprires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_token = jwt.encode(to_encode, SCRET_KEY, algorithm=ALGORITHM)
    return encoded_token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SCRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        print("Token verification failed.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


if __name__ == "__main__":
    print("This is a helper file for JWT operations. It provides functions to create and manage JWT tokens.")
    # Example usage
    data = {"sub": "user_id_123"}
    token = create_access_token(data)
    print(f"Generated token: {token}")
    # Verify the token
    payload = verify_access_token(token)
    if payload:
        print(f"Token is valid. Payload: {payload}")
    else:
        print("Token is invalid.")
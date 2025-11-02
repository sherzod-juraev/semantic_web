from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from passlib.context import CryptContext

context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

# password hashed
def hashed_pass(raw_password: str, /) -> str:
    return context.hash(raw_password)

def verify_pass(raw_password: str, hashed_password: str, /) -> bool:
    return context.verify(raw_password, hashed_password)


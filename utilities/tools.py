from passlib.context import CryptContext

### Hash ###
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

### Others ###
def parse_boolean(value):
    if value is None:
        return False
    return value.lower() in ('true', '1', 'yes', 'on')
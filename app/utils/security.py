from passlib.context import CryptContext

# Use bcrypt with a stable configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash password safely with bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against stored hash"""
    return pwd_context.verify(plain_password, hashed_password)

from app.core.security import get_password_hash

# Хешируем пароль "Password1"
hashed = get_password_hash("Password1")
print(f"Хеш пароля: {hashed}")
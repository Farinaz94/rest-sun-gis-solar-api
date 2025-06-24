from jose import jwt

SECRET_KEY = "244a734dc6205fb0187e65908e053418b4135d89166435346a3c3d30165b7c34"
ALGORITHM = "HS256"

data = {"sub": "farinaz"}  

token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
print(token)

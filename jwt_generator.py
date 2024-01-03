import jwt

def generate_jwt_token():
    # Secret key
    secret_key = 'omen'

    payload = {'username': 'gaurav0634', 'role': 'admin'}

    # Generate a JWT token
    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')

    return jwt_token

if __name__ == "__main__":
    token = generate_jwt_token()
    print(token)

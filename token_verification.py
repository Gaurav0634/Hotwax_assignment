import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImdhdXJhdjA2MzQiLCJyb2xlIjoiYWRtaW4ifQ.hws1NGa4zq8SEhE5jLl5gHKIqVLTeUsX10hMrpkGHy0"

try:
    decoded_token = jwt.decode(token, verify=False)  # Decode the token without verification
    print(decoded_token)
except jwt.ExpiredSignatureError:
    print("Token expired")
except jwt.InvalidTokenError:
    print("Invalid token")

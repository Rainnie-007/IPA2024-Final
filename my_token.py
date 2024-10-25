import os

api_token = os.getenv('API_TOKEN')

if api_token:
    print("Token is ready for use.")
else:
    print("API Token not found. Please set it in your environment variables.")

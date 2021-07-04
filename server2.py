from dotenv import load_dotenv
from os import environ
from mongoproxy.server import *

load_dotenv()
mongoinit(environ.get('mongouri'))

if __name__ == "__main__":
  uvicorn.run("server2:app", host="0.0.0.0", port=5000, log_level="info")

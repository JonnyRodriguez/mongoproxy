from dotenv import load_dotenv
from os import environ
from mongoproxy.server import *

load_dotenv()
mongoinit(environ.get('mongouri'))

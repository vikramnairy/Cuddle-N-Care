from flask import *
import pyrebase
from Config import *


firebase = pyrebase.initialize_app(config)
db=firebase.database


    
#*************My code********
import os
from dotenv import load_dotenv

load_dotenv() 

database = os.environ.get('database', 'Store')
database_config = {'user': os.environ.get('database_user'), 'password': os.environ.get('database_password'), 'host': os.environ.get('database_host')}

#print(database_config)

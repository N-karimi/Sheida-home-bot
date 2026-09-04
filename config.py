#*************My code********
import os
from dotenv import load_dotenv

load_dotenv() 

database_name = os.environ.get('database_name')
database_config = {'user': os.environ.get('database_user'), 'password': os.environ.get('database_password'), 'host': os.environ.get('database_host')}

print('database name:', database_name)
print('host:', database_config['host'])
print('d user:', database_config['user'])
#print(database_config)

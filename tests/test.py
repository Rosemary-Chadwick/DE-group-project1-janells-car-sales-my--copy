from sqlalchemy import create_engine
import pandas as pd
import os
from main import get_token, get_data
from dotenv import load_dotenv
'''
The purpose of this module is to:
    a. load clean data from database
    b. convert to json
    c. validate clients table against the data collected from api
'''
'''
step 1: recreate clients table with sql joins
step 2: load them here
'''
# get the token
# get_token()
# load_dotenv(override=True)

user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')
host = os.getenv('PG_HOST')
port = os.getenv('PG_PORT')
db = os.getenv('PG_DB')
csv_name = 'data/client_contact_status.csv'
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')


# Example: Load 'clients' table into a DataFrame
offset = 0
limit = 10
chunks = pd.read_sql_table('clients', con=engine, chunksize=limit)
for chunk in chunks:
    data_pulled_db = chunk.to_dict(orient='records')
    # print(data_pulled_db)
    data_api = get_data(offset,limit,'clients')
    # print(data_api)
    if data_pulled_db == data_api:
        print("Data matches between database and API.")
    else:
        print("Data mismatch between database and API.")
    offset += limit
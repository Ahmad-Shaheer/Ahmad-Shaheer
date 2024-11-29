import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import sqlite3



def log_progress(message):
    now = datetime.now()
    with open('code_log.txt', 'a') as file:
        file.write(str(now) +' : '+ message+'\n')
        
def extract(url, table_attribs):
    
    log_progress('Preliminaries complete. Initiating ETL process')
    
    item = requests.get(url)
    extracted_text = BeautifulSoup(item.text, 'html.parser')
    results = extracted_text.find('table', table_attribs)
    
    dfs = pd.read_html(str(results))   
    df = pd.concat(dfs)
    
    log_progress('Data extraction complete. Initiating Transformation process')

    return df
    

def transform(df, csv_path):
    
    exchange_rate = pd.read_csv(csv_path)
    dict_exchange_rate = exchange_rate.to_dict()
    df = df.rename(columns = {'Market cap (US$ billion)':'MC_USD_Billion', 'Bank name': 'Name'})
    df['MC_GBP_Billion'] = [np.round(x*dict_exchange_rate['Rate'][1],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x*dict_exchange_rate['Rate'][0],2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x*dict_exchange_rate['Rate'][2],2) for x in df['MC_USD_Billion']]

    log_progress('Data transformation complete. Initiating Loading process')
    return df



def load_to_csv(df, output_path = './Largest_banks_data.csv'):
    df.to_csv(output_path)
    
    log_progress('Data saved to CSV file')
    pass



def load_to_db(df, sql_connection, table_name):
    
    log_progress('SQL Connection initiated')
    
    df.to_sql(table_name, sql_connection, if_exists='replace')
    
    log_progress('Data loaded to Database as a table, Executing queries')
    
    pass


def run_query(query_statement, sql_connection):
    response = pd.read_sql_query(query_statement, sql_connection)
    
    log_progress('Process Complete')
    
    
    log_progress('Server Connection closed')
    
    print(f'{query_statement} \n {response}')

if __name__ == '__main__':
    connection = sqlite3.connect('Bank.db')
    url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
    
    
    df = extract(url, {'class':'wikitable'})
    df_transformed = transform(df, './exchange_rate.csv' )
    # load_to_csv(df_transformed)
    load_to_db(df_transformed, connection, table_name= 'Largest_banks')
    run_query('SELECT * FROM Largest_banks', connection)
    run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks', connection)
    run_query('SELECT Name from Largest_banks LIMIT 5', connection)

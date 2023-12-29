from tinydb import TinyDB, Query
import json
import os
from dotenv import load_dotenv
import logging
import logging.config
import yaml
from services.pbiservice import PbiService
import services.data_service as ds
from utilities.data_utils import convert_dataframe_to_dict, get_table_columns
import pandas as pd

config = yaml.load(open("config.yml"), Loader=yaml.Loader)

logging.config.dictConfig(config['logging_config'])
logger = logging.getLogger('main')

load_dotenv()

logger.info('Initiating data refresh process')

tables_to_push = []

try: 
    logger.info('Fetching and processing case data from Salesforce')
    df_case_data = ds.get_case_data()
    df_case_data = df_case_data
    df_case_data = df_case_data[get_table_columns('case_data')]
    # case_data = convert_dataframe_to_dict(df_case_data)
    tables_to_push.append({'name': 'case_data', 'df': df_case_data})
except: 
    logger.exception('Something went wrong with fetching/processing case data')

try: 
    logger.info('Fetching and processing account temperament data from Salesforce')
    df_acct_temperaments = ds.get_account_temperaments(case_data=df_case_data)
    df_acct_temperaments = df_acct_temperaments[get_table_columns('account_temperaments')]
    # acct_temperaments = convert_dataframe_to_dict(df_acct_temperaments)
    tables_to_push.append({'name': 'account_temperaments', 'df': df_acct_temperaments})
except: 
    logger.exception('Something went wrong with fetching/processing account temperament data')

try: 
    logger.info('Fetching and processing survey data from Salesforce')
    df_survey_data = ds.get_survey_data()
    df_survey_data = df_survey_data[get_table_columns('survey_data')]
    # survey_data = convert_dataframe_to_dict(df_survey_data)
    tables_to_push.append({'name': 'survey_data', 'df': df_survey_data})
except: 
    logger.exception('Something went wrong with fetching/processing survey data')

try: 
    logger.info('Fetching birthday data')
    df_birthdays = ds.get_birthdays()
    df_birthdays = df_birthdays[get_table_columns('birthdays')]
    # birthdays = convert_dataframe_to_dict(df_birthdays)
    tables_to_push.append({'name': 'birthdays', 'df': df_birthdays})
except: 
    logger.exception('Something went wrong with fetching birthday data')

try: 
    logger.info('Fetching datetime data')
    df_date_time = ds.get_time_as_dataframe()
    df_date_time = df_date_time[get_table_columns('date_time')]
    # date_time = convert_dataframe_to_dict(df_date_time)
    tables_to_push.append({'name': 'date_time', 'df': df_date_time})
except: 
    logger.exception('Something went wrong with fetching datetime data')

try:
    logger.info('Posting table data to Excel')
    path = os.environ['DATA_FILE']
    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:  
        workbook = writer.book

        for table in tables_to_push:
            (name, df) = table.values()
            df.to_excel(writer, sheet_name=name + '_s', index=False)

            worksheet = writer.sheets[name + '_s']

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            # Create a list of column headers, to use in add_table().
            column_settings = []
            for header in df.columns:
                column_settings.append({'header': header})

            # Add the table.
            worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'name': name})
        # writer.save()
except: 
    logger.exception('Something went wrong with posting table data to Excel')

"""
File: data_actions.py
Author: Sam Pierce
Date: 2023-11-05
Description: A module for fetching and processing data from Salesforce for the AssetPoint weekly Power BI dashboard. This file was originally maintained for another program and may contain unused functions or variables. 
"""

import re
import pandas as pd
import numpy as np
import random
# Date/Time
import time
from datetime import datetime as dt
from datetime import timedelta as td
#Salesforce API
from simple_salesforce import Salesforce
from io import StringIO
from pytz import timezone as tz
from dotenv import load_dotenv
import logging
import logging.config
import yaml
import os
from tinydb import TinyDB, Query

db = TinyDB('app_data.json')

config = yaml.load(open("config.yml"), Loader=yaml.Loader)

logging.config.dictConfig(config['logging_config'])
logger = logging.getLogger('main')


load_dotenv()

TODAY = dt.now(tz=None)
DATE = TODAY.strftime('%Y%m%d%H%M')
DAY_OF_WEEK = int(TODAY.strftime("%w"))
END_DATE = TODAY + td(days = 5 - DAY_OF_WEEK)
START_DATE = END_DATE - td(weeks=1)

def get_attribute(attribute, val):
        if val is None:
            return None
        else:
            return val[attribute]

def get_global_time():
    try:
        monday_of_week = TODAY - td(days = DAY_OF_WEEK - 1)
        friday_of_week = TODAY - td(days = DAY_OF_WEEK - 5)

        day_of_month1 = monday_of_week.strftime("%d")
        day_of_month2 = friday_of_week.strftime("%d")
        suffix1 = get_suffix(day_of_month1)
        suffix2 = get_suffix(day_of_month2)

        date1 = ''.join(re.match( '^(\D*\s)(?:0?)(\d.*)$', monday_of_week.strftime('%B %d')).groups()) + suffix1 + monday_of_week.strftime('%Y')
        date2 = ''.join(re.match( '^(\D*\s)(?:0?)(\d.*)$', friday_of_week.strftime('%B %d')).groups()) + suffix2 + friday_of_week.strftime('%Y')

        DATE_RANGE = date1 + ' - ' + date2
        global_time = { 'DATE': DATE,
                        'DAY_OF_WEEK': DAY_OF_WEEK,
                        'END_DATE': END_DATE,
                        'START_DATE': START_DATE,
                        'TODAY': TODAY,
                        'DATE_RANGE': DATE_RANGE
                    }
    except Exception as err:
        logger.exception("Error retrieving global time: %s", err)
    return global_time
   
def get_time_as_dataframe():
    return pd.DataFrame(get_global_time(), index=[0])

def opened_this_week(row):
    if row['Date/Time Opened'] >= START_DATE:
        return 1
    else: 
        return 0

def closed_this_week(row):
    if row['Date/Time Closed'] >= START_DATE:
        return 1
    else: 
        return 0
        
def iter_cells(table):
    for row in table.rows:
        for cell in row.cells:
            yield cell
            
def get_suffix(dayString): 
    day = int(dayString)
    if(day > 14):
            day = day % 10
    
    switch = {
        0: 'th ',
        1: 'st ', 
        2: 'nd ',
        3: 'rd ',
        4: 'th ', 
        5: 'th ', 
        6: 'th ', 
        7: 'th ', 
        8: 'th ', 
        9: 'th ', 
        10: 'th ',
        11: 'th ', 
        12: 'th ', 
        13: 'th ', 
        14: 'th '
    }
    return switch.get(day,  '')

def get_birthdays():
    try:
        team_members = get_support_members()
        birthdays_temp = [{'Name': tm.get('preferred_name'), 'Birthday': dt(dt.today().year, dt.fromisoformat(tm.get('birthday')).month, dt.fromisoformat(tm.get('birthday')).day)} for tm in team_members if tm.get('active') == True]
        birthdays = pd.DataFrame(birthdays_temp)

        def increment_year(bd):
            if (bd.year < dt.today().year or 
                    (bd.year <= dt.today().year and bd.month < dt.today().month) or
                        (bd.year <= dt.today().year and bd.month <= dt.today().month and bd.day < dt.today().day)):
                            return dt(bd.year + 1, bd.month, bd.day)
            else:
                return bd

        birthdays['Birthday'] = birthdays['Birthday'].apply(lambda bd: increment_year(bd))
        birthdays['Countdown (Days)'] = birthdays['Birthday'].apply(lambda bd: (bd - dt.combine(dt.today(), dt.min.time())).days)
    except Exception as err:
        logger.exception("Error retrieving birthdays: %s", err)
    return birthdays

def api_call(query):
    try:
        SF_INSTANCE = os.environ['SF_INSTANCE']
        SF_USERNAME = os.environ['SF_USERNAME']
        SF_PASSWORD = os.environ['SF_PASSWORD']
        SF_TOKEN = os.environ['SF_TOKEN']
        sf = Salesforce(instance_url=SF_INSTANCE, username=SF_USERNAME, password=SF_PASSWORD, security_token=SF_TOKEN)
        result = sf.query_all(query)
    except Exception as err:
        logger.exception("Error with salesforce API: %s", err)

    return result

def get_case_data():
    # LAST_N_WEEKS:52 starts at the end of the previous week and goes back 52 weeks. LAST_N_DAYS:10 overlaps with LAST_N_WEEKS:52 to fill in gap.
    #Added Region field and Is Support Case criterion ID 2022-12-16
    try:
        QUERY = '''
                SELECT 
                    Owner.Name,
                    CreatedById,
                    CaseNumber,
                    QS_Severity__c,
                    Service_Team__r.Name,
                    Account.Name, 
                    Account.Region__c,
                    Type,
                    Subject,
                    CreatedDate,
                    Last_Action_Date__c,
                    LastModifiedDate,
                    Hours_Since_Creation__c,
                    Contact.Name,  
                    Status, 
                    Sub_Status__c,
                    Case_Survey_Sent__c,
                    ClosedDate,
                    QS_Escalation_Owner__r.Name,
                    QS_Escalation_Date__c,
                    QS_Escalation_Status__c,
                    QS_Escalation_Details_Comments__c,
                    LastViewedDate 
                FROM Case 
                WHERE
                        Product_Line__c IN ('AssetPoint', 'Aptean EAM')
                    AND (
                            CreatedDate = LAST_N_WEEKS:52
                        OR  CreatedDate = LAST_N_DAYS:10
                        OR  ClosedDate = LAST_N_WEEKS:52
                        OR  ClosedDate = LAST_N_DAYS:10
                        OR  Status != 'Closed'
                        )
                    AND Is_Support_Case__c = TRUE

                '''

        result = api_call(QUERY)
        df = pd.DataFrame.from_dict(result['records'])
        df.rename(columns={
                    'Owner': 'Case Owner',
                    'CaseNumber': 'Case Number',
                    'QS_Severity__c': 'Severity', 
                    'Service_Team__r': 'Service Team',
                    'Account': 'Account Name',
                    'CreatedDate': 'Date/Time Opened', 
                    'Last_Action_Date__c': 'Last Action Date',
                    'LastModifiedDate': 'Case Last Modified Date', 
                    'Sub_Status__c': 'Sub-Status',
                    'Case_Survey_Sent__c': 'Case Survey Sent', 
                    'ClosedDate': 'Date/Time Closed', 
                    'QS_Escalation_Owner__r': 'Escalation Owner',
                    'QS_Escalation_Date__c': 'Escalation Date', 
                    'QS_Escalation_Status__c': 'Escalation Status',
                    'QS_Escalation_Details_Comments__c': 'Escalation Details / Comments'
                        }, inplace=True)

        

        df['Case Owner'] = df['Case Owner'].apply(lambda o: get_attribute('Name', o))
        df['Account Region'] = df['Account Name'].apply(lambda o: get_attribute('Region__c', o))
        df['Account Name'] = df['Account Name'].apply(lambda o: get_attribute('Name', o))
        df['Contact'] = df['Contact'].apply(lambda o: get_attribute('Name', o))
        df['Service Team'] = df['Service Team'].apply(lambda o: get_attribute('Name', o))
        df['Escalation Owner'] = df['Escalation Owner'].apply(lambda o: get_attribute('Name', o))
        df.drop(columns=['attributes'], inplace=True)
        df['Open'] = df['Status'].apply(lambda status: 0 if status == 'Closed' else 1)
        

        df['Date/Time Opened'] = pd.to_datetime(df['Date/Time Opened'])
        df['Date/Time Closed'] = pd.to_datetime(df['Date/Time Closed'])
        df['Date/Time Opened'] = df['Date/Time Opened'].dt.tz_localize(None)
        df['Date/Time Closed'] = df['Date/Time Closed'].dt.tz_localize(None)
        df['Closed'] = df.apply(lambda row: (row['Open'] + 1) % 2 , axis=1)
        df['Opened This Week'] = df.apply(opened_this_week, axis=1)
        df['Closed This Week'] = df.apply(closed_this_week, axis=1)
        df['Quarter'] = df['Date/Time Opened'].dt.quarter
        df['Quarter'] = df['Date/Time Closed'].dt.quarter
        df['Year'] = df['Date/Time Opened'].dt.year
        df['Year'] = df['Date/Time Closed'].dt.year
        df['Age'] = df.apply(lambda row: TODAY - row['Date/Time Opened'], axis=1).dt.days

        SUPPORT_MEMBERS = get_support_members()
        df['Is Support Member'] = df['Case Owner'].apply(lambda owner: owner in [member.get('name') for member in SUPPORT_MEMBERS])
    
    except Exception as err:
        logger.exception("Error retrieving case data: %s", err)

    return df

def get_support_members():
    try:
        tb_team_members = db.table('team_members')
        SUPPORT_MEMBERS = tb_team_members.all()
    except Exception as err:
        logger.exception("Error retrieving support members: %s", err)
    return SUPPORT_MEMBERS
         

def get_survey_data():
    try:
        QUERY = '''
                SELECT 
                    QS_Case_Owner__r.Name,
                    QS_Case__r.CaseNumber,
                    QS_Account__r.Name,
                    QS_Contact2__r.Name,
                    QS_Customer_Comments__c,
                    QS_Case__r.ClosedDate,
                    Question_Problem_Diagnosis__c,
                    Question_Product_Knowledge__c,
                    Question_Professionalism__c,
                    Question_Communication__c,
                    QS_CSAT__c
                FROM QS_Survey_Feedback__c
                WHERE
                        Product_Line__c = 'AssetPoint'
                    AND (
                            QS_Case__r.ClosedDate = LAST_N_WEEKS:52
                        OR  QS_Case__r.ClosedDate = LAST_N_DAYS:10
                        )
                '''

        result = api_call(QUERY)
        df = pd.DataFrame.from_dict(result['records'])
        df.rename(columns={
                    'QS_Case_Owner__r': 'Case Owner',
                    'CaseNumber': 'Case Number',
                    'QS_Customer_Comments__c': 'Customer Comments',
                    'QS_CSAT__c': 'Overall Satisfaction', 
                    'Question_Communication__c': 'Question: Communication',
                    'Question_Professionalism__c': 'Question: Professionalism',
                    'Question_Product_Knowledge__c': 'Question: Product Knowledge',
                    'Question_Problem_Diagnosis__c': 'Question: Problem Diagnosis',
                    'QS_Account__r': 'Account Name',
                    'QS_Contact2__r': 'Contact Name'
                        }, inplace=True)


        df['Case Owner'] = df['Case Owner'].apply(lambda o: get_attribute('Name', o))
        df['Account Name'] = df['Account Name'].apply(lambda o: get_attribute('Name', o))
        df['Contact Name'] = df['Contact Name'].apply(lambda o: get_attribute('Name', o))
        df['Date/Time Closed'] = df['QS_Case__r'].apply(lambda o: o['ClosedDate'])
        df['Case Number'] = df['QS_Case__r'].apply(lambda o: o['CaseNumber'])
        df.drop(columns=['attributes', 'QS_Case__r'], inplace=True)

        
        df['Date/Time Closed'] = pd.to_datetime(df['Date/Time Closed'])
        df['Date/Time Closed'] = df['Date/Time Closed'].dt.tz_localize(None)

        df.sort_values(by=['Case Owner', 'Account Name', 'Contact Name'], inplace=True)
    except Exception as err:
        logger.exception("Error retrieving survey data: %s", err)

    return df

def get_weekly_case_data(data):
    try:
        df_cases = data
        
        #
        # Filter conditions  
        #
        df_cases = df_cases[
            df_cases['Is Support Member']
            & (
                (df_cases['Opened This Week'] == 1) 
            |   (df_cases['Closed This Week'] == 1) 
            |   (   (df_cases['Open'] == 1)
                &   (~df_cases['Status'].isin(["Closed", "Waiting on Release", "With Fulfillment", "With Sales", "With Services"]))
                &   (~df_cases['Sub-Status'].isin(["Change Request (Bug)", "Change Request (ER)", "Deployment (PROD)", "Deployment (Test)", "Deployment (Stage)", "Management", "SME - Services", "SME - Support"]))
                &   (~df_cases['Service Team'].isin(["Assetpoint - Tech", "Aptean Cloud Services"]))
                )
            )
            ]
    except Exception as err:
        logger.exception("Error retrieving weekly case data: %s", err)

    return df_cases

def get_account_temperaments():
    try:
        QUERY = '''
        SELECT 
            Name, 
            Product_Line_Profile__c,
            Temperament__c,
            Temperament_Notes__c
        FROM Account
        WHERE
            Product_Line_Profile__c IN ('AssetPoint', 'Aptean EAM')
        '''
        
        result = api_call(QUERY)
        account_temperament = pd.DataFrame.from_dict(result['records'])
        account_temperament.drop(columns=['attributes'], inplace=True)
        account_temperament.rename(columns={
            'Product_Line_Profile__c': 'Product Line', 
            'Temperament__c': 'Temperament',
            'Temperament_Notes__c': 'Temperament Notes'

        }, inplace=True)
        def convert_html(match_obj):
            if match_obj.group(1) is not None:
                return "\n"
            if match_obj.group(2) is not None:
                return ""
        account_temperament['Temperament Notes'] = account_temperament['Temperament Notes'].apply(lambda x: re.sub("(<br>)|(<[^>]*>)", convert_html, str(x)))

        case_data = get_case_data()
        df = case_data.merge(account_temperament, left_on="Account Name", right_on="Name", how="right")
    except Exception as err:
        logger.exception("Error retrieving account temperaments: %s", err)

    return df

def get_calendar():
    try:
        month_start = dt.today().replace(day=1)
        first_calendar_day = month_start - td(days=month_start.weekday() + 1)
        month_end = dt(year=month_start.year + (1 if month_start.month == 12 else 0), month=(month_start.month + 1) % 13,day=1) - td(days=1)
        last_calendar_day = month_end + td(days=7 - month_end.weekday())
        date_range = pd.date_range(start=first_calendar_day, end=last_calendar_day)
        date_range = pd.DataFrame(date_range).rename({0: "Date"}, axis='columns')
        #date_range['Weekday'] = date_range['Date'].apply(lambda date: date.strftime(""%A""))
        cols = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        cal = pd.DataFrame( columns=cols)
        for i in range(0, len(date_range), 7):
            cal.loc[len(cal), :] = date_range['Date'].tolist()[i:i+7]
        calendar = cal
    except Exception as err:
        logger.exception("Error retrieving calendar: %s", err)

    return calendar


if __name__ == '__main__':
    # import os
    # case_data = get_case_data()
    # data = get_weekly_case_data(case_data)
    # data.to_excel('test.xlsx')
    # os.startfile('test.xlsx')
    pass

    
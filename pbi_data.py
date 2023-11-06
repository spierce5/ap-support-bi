import sys
import os

# This needs to be set to the project directory
path = "C:/Users/spierce1/Documents/Python_Automation/AssetPoint_Weekly_BI"
sys.path.insert(0, path)
import data_actions as da
os.chdir(path)

case_data = da.get_case_data()
weekly_case_data = da.get_weekly_case_data(case_data).copy(deep=True)
date_time = da.get_time_as_dataframe()
birthdays = da.get_birthdays()
survey_data = da.get_survey_data()
account_temperaments = da.get_account_temperaments()
calendar = da.get_calendar()
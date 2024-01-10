from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from tempfile import NamedTemporaryFile
import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils import get_column_interval
import re
from datetime import date


ssid_subm = '10Od0nhz92hKVpuAwXFg45XGRZMz6x8vYf3cPvtxQe5E'
ssid_full = '1SsrJp5370HOfCURm64vOHIjZnMxmeC5deVZ6bLTEJE4'


creds = service_account.Credentials.from_service_account_file(
          'serviceacc.json',
          scopes=['https://www.googleapis.com/auth/drive.file',
                  'https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/drive.metadata',
                  'https://www.googleapis.com/auth/spreadsheets'
                  ]
          )  

def today_string():
    today = date.today()
    current_date = today.strftime('%Y-%m-%d')
    return current_date

def today_string_file():
    today = date.today()
    current_date = today.strftime('%m%d')
    return current_date

def load_workbook_range(range_string, ws):
    col_start, col_end = re.findall("[A-Z]+", range_string)

    data_rows = []
    for row in ws[range_string]:
        data_rows.append([cell.value for cell in row])

    return pd.DataFrame(data_rows, columns=get_column_interval(col_start, col_end))

def excel_reader_get_data(excel_file, facility_list):
    wb = openpyxl.load_workbook(excel_file, read_only=True)
    data = {}
    for facility in facility_list:
       ws = wb[facility]
       data[facility] = load_workbook_range(range_string='A1:N17', ws=ws)  # df
    return data  # dict of dfs

def excel_storage_conversion(df):
    goog = df.values.tolist()
    return { 'values': goog }

def reformat_add_df_context(df, facility, submission_id):
    df['Facility'] = facility
    df['submission_id'] = submission_id
    df=df[1:]
    return df


def stored_GET_data(spreadsheetId, spreadsheetRange):   
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    spreadsheetId = spreadsheetId
    spreadsheetRange = spreadsheetRange
    result = service.spreadsheets().values().get(
                                                spreadsheetId=spreadsheetId, 
                                                range=spreadsheetRange
                                                ).execute()
    df = pd.DataFrame(result['values'])
    df.columns = df.iloc[0]
    dfpiv = df[1:]
    return df, dfpiv
    
def stored_SET_data(spreadsheetId, spreadsheetRange, valueBody, inputOption='USER_ENTERED'):  
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    spreadsheetId = spreadsheetId  # '1-zYgl-7ffj8cV2N80aICDHHKHfqyQX5rE3HXDcgSsfc'
    spreadsheetRange = spreadsheetRange  # 'CurrentFacilityValues!A1:BQ321'
    inputOption = 'USER_ENTERED'
    valueBody = valueBody
    result = service.spreadsheets().values().update(
                                              spreadsheetId=spreadsheetId, 
                                              range=spreadsheetRange,
                                              valueInputOption=inputOption, 
                                              body=valueBody
                                              ).execute()
    
def stored_APPEND_data(spreadsheetId, spreadsheetRange, valueBody, inputOption='USER_ENTERED'):  
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    spreadsheetId = spreadsheetId  # '1-zYgl-7ffj8cV2N80aICDHHKHfqyQX5rE3HXDcgSsfc'
    spreadsheetRange = spreadsheetRange  # 'CurrentFacilityValues!A:BQ'
    inputOption = 'USER_ENTERED'
    valueBody = valueBody
    result = service.spreadsheets().values().append(
                                              spreadsheetId=spreadsheetId, 
                                              range=spreadsheetRange,
                                              valueInputOption=inputOption, 
                                              body=valueBody
                                              ).execute()

def upload_file_to_drive(upload_file, file_name):
  service = build("drive", "v3", credentials=creds)
  try: 
    file_metadata = {"name": file_name, "parents":["113OEOtoIU3iF3mQ4EwlZZGtPgbZfePqc"]}
    with NamedTemporaryFile(dir='.', suffix='.xlsx') as f:
      f.write(upload_file.getbuffer())
      media = MediaFileUpload(f.name, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") 
    file = (
        service.files()
        .create(supportsTeamDrives=True, body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print(f'File ID: {file.get("id")}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  fileid = file.get("id")
  permission1 = {
       'type': 'user',
       'role': 'writer',
       'emailAddress': 'charlotteradiologydatateam@gmail.com',  # Please set your email of Google account.
   }
  service.permissions().create(fileId=fileid, body=permission1).execute()
  permission2 = {
        'type': 'anyone',
        'role': 'writer',
    }
  service.permissions().create(fileId=fileid, body=permission2).execute()
  
  return fileid


def final_combine_and_store_all_facilities(excel_file, facility_list, submission_id):
   fdfs = excel_reader_get_data(excel_file, facility_list)
   for facility in facility_list:
      df = fdfs[facility]
      df = reformat_add_df_context(df, facility, submission_id)
      body = excel_storage_conversion(df)
      stored_APPEND_data(ssid_full, 'Mamm!A:P', body)
      
def get_iteration(service_line, forecast_month):
   subm_df = stored_GET_data(ssid_subm, 'All!A1:K')[0]
   filtered_list = subm_df[(subm_df['ServiceLine']==service_line) & (subm_df['Version']==forecast_month)]
   return len(filtered_list)

def number_naming_convention(num):
   nums = str(num)
   return_str = ''
   for x in range(4-len(nums)):
       return_str += '0'
   return return_str + nums


def add_submission_line(metadata):
    metadata_df = pd.DataFrame(metadata, index=[0])
    goog = excel_storage_conversion(metadata_df)
    stored_APPEND_data(ssid_subm, 'All!A:K', goog)
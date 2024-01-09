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

def RangeValue(ws, rs, cs, re, ce):
    return(tuple(tuple(ws.cell(row=cs+i, column=rs+j).value for j in range(re-rs+1)) for i in range(ce-cs+1)))


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
       data[facility] = load_workbook_range(range_string='A1:N17', ws=ws)
    return data

def excel_storage_conversion(df):
    goog = df.values.tolist()
    return { 'values': goog }

def reformat_add_df_context(df, facility, submission_id):
    df.loc[:,'submission_id'] = submission_id
    df.loc[:,'Facility'] = facility
    col_order = df.columns.tolist()
    new_cols = ['submission_id', 'Facility']
    new_col_order = new_cols.append(col_order)
    df = df[new_col_order]
    return df


def stored_GET_data(spreadsheetId, spreadsheetRange):   
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    spreadsheetId = spreadsheetId  # '1-zYgl-7ffj8cV2N80aICDHHKHfqyQX5rE3HXDcgSsfc'
    spreadsheetRange = spreadsheetRange  # 'CurrentFacilityValues!A1:BQ321'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, 
        range=spreadsheetRange).execute()
    

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

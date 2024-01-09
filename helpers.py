from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import pandas as pd
from tempfile import NamedTemporaryFile


def upload_basic(upload_file, file_name):
  """Insert new file.
  Returns : Id's of the file uploaded
  """
  creds = service_account.Credentials.from_service_account_file(
            'serviceacc.json',
            scopes=['https://www.googleapis.com/auth/drive.file',
                    'https://www.googleapis.com/auth/drive',
                    'https://www.googleapis.com/auth/drive.metadata',
                    'https://www.googleapis.com/auth/spreadsheets'
                    ]
            )

  try:
    # service = build("drive", "v3", credentials=creds)
    # file_metadata = {"name": file_name, "parents":["113OEOtoIU3iF3mQ4EwlZZGtPgbZfePqc"]}
    # media = MediaFileUpload(upload_file, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # # media = upload_file
    # file = (
    #     service.files()
    #     .create(supportsTeamDrives=True, body=file_metadata, media_body=media, fields="id")
    #     .execute()
    # )
    service = build("drive", "v3", credentials=creds)
    file_metadata = {"name": file_name, "parents":["113OEOtoIU3iF3mQ4EwlZZGtPgbZfePqc"]}
    
    with NamedTemporaryFile() as f:
        f.write(upload_file)
        
    media = MediaFileUpload(f, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
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
# hold
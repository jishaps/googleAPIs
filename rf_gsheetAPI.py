import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import csv

# This is the OAUTH Scope for google API. In this case we are limiting the scope just to spread sheet and also read only. Least privilege principles
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Just used the sample publicily avilable spreadsheet. The ID can be figured out from the URL. 
# In future as needed, change the ID and Sheet names as appropriate and even parameterize these as inputs
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

"""
Main method to call the sheets API to fetch data. First step is to create the credentials to access the spreadsheet and then call the sheets API
A credentials (json file) is created from Cloud API console under Service Account Key. Note this has to be stored securely 
"""
def main():

    # created from Cloud console  Service account 
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    secretCreds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    
    try:
        service = build('sheets', 'v4', credentials=secretCreds)

        # Standard Sheets API calls. Nothing Fancy here! Reused as available from official documentation
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        
        # Stage 2 : Writing data back to the CSV file 
        # Define Header
        header = ['Name', 'Gender','Class Level','State','Major']
        # Create a file in write mode header , followed by data 
        with open('rf_csv.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            for row in values:
                writer.writerow(row)
        # Debugging code : Clean up after testing!!
        #print('Name, Major:')
        #for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s, %s' % (row[0], row[4]))
            
            
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()

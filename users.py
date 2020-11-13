import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)
groups = [file['name'] for file in client.list_spreadsheet_files()]
print(groups)

table = client.open("PM")

params = []
for sheet in table.worksheets():
    # sheet_row = sheet.row_values(1)
    # link = sheet_row[1]
    # repetiotions_per_week = sheet_row[3]
    # number_of_repetitions = sheet_row[5]
    # wrong_answer = sheet_row[7]
    #
    # params.append([link, repetiotions_per_week, number_of_repetitions, wrong_answer])
    #
    # questions = sheet.col_values(1)[2:]
    # answers = sheet.col_values(2)[2:]
    # repetitions = sheet.col_values(3)[2:]
    # pairs_qa = list(zip(questions, answers, repetitions))
    # print(pairs_qa)
    # print(params)
    # # data = sheet.get_all_records()
    print(sheet)
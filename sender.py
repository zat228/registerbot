import httplib2
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from config import FILE, ID


credentials = ServiceAccountCredentials.from_json_keyfile_name(FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                      'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
spreadsheetId = ID  # Код гугл таблицы


def creator(ready_info):
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheetlist = spreadsheet.get('sheets')
    sheet_name = []
    sheet_name.clear()
    for sheet in sheetlist:
        sheet_name.append(sheet['properties']['title'])

    # print(spreadsheet)
    # print(sheetlist)
    # print(sheet_name)

    if ready_info.group in sheet_name:
        print(f"Лист с названием {ready_info.group} найден!")
        send(ready_info)
    else:
        print(f"Создатель листов: Создаю лист с именем {ready_info.group}")
        try:
            result = service.spreadsheets().batchUpdate(
                spreadsheetId=ID,
                body={
                    "requests": [
                        {
                            "addSheet": {
                                "properties": {
                                    "title": f"{ready_info.group}",
                                    "gridProperties": {
                                        "rowCount": 200,
                                        "columnCount": 12
                                    }
                                }
                            }
                        }
                    ]
                }).execute()
            send(ready_info)
        except HttpError as error:
            print(f"Менеджер отправки: ошибка {error}")


def send(ready_info):
    print(f"Менеджер отправки: Отправляю данные на лист {ready_info.group}")
    try:
        values = [
            [ready_info.name, ready_info.second_name, ready_info.patronymic, ready_info.tg]
        ]

        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(spreadsheetId=ID, range=f"{ready_info.group}!B2",
                                                        valueInputOption="USER_ENTERED", body=body).execute()

    except HttpError as error:
        print(f"Менеджер отправки: ошибка {error}")


def checker(user_dog):
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheetlist = spreadsheet.get('sheets')
    list_of_ids = []
    for sheet in sheetlist:
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=f"{sheet['properties']['title']}!E2:E9999").execute()
            for i in result.get('values', []):
                list_of_ids.append(i[0])
                # rows = result.get('values')
        except HttpError as error:
            print(f"An error occurred: {error}")
    if "@"+user_dog in list_of_ids:
        return True
    else:
        return False


def update_group():
    info = []
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    list_of_names = []
    sheetlist = spreadsheet.get('sheets')
    for sheet in sheetlist:
        list_of_names.append([sheet['properties']['title'], sheet['properties']['sheetId']])
    for i in list_of_names:
        try:
            course_old = i[0].split("-")[1][0]
            course_new = i[0].replace(str(course_old), str(int(course_old) + 1), 1)
            if (int(course_old) + 1) <= 6:
                results = service.spreadsheets().batchUpdate(
                    spreadsheetId=ID,
                    body={
                        "requests": [
                            {"updateSheetProperties":
                                {"properties":
                                    {
                                        "sheetId": i[1],
                                        "title": course_new,
                                    },
                                    "fields": "title",
                                }
                            }
                        ]
                    }).execute()
                info.append(f"{i[0]} --> {course_new}")
            else:
                results = service.spreadsheets().batchUpdate(
                    spreadsheetId=ID,
                    body={
                        "requests": [
                            {
                                "deleteSheet": {
                                    "sheetId": i[1]
                                }
                            }
                        ]
                    }).execute()
                info.append(f"{i[0]} --> УДАЛЁН")
        except Exception as e:
            info.append(f"{i[0]} --> Ошибка с названием")
            print(f"{i[0]} skipped")
    print(info)
    return info


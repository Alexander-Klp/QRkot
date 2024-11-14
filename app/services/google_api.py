import logging
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services.tools import format_timedelta


logger = logging.getLogger("uvicorn.error")

FORMAT = "%Y/%m/%d %H:%M:%S"

SPREADSHEETS_BODY = {
    'properties': {'title': '',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}

TABLE_VALUES = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

UPDATE_BODY = {
    'majorDimension': 'ROWS',
    'values': TABLE_VALUES
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    SPREADSHEETS_BODY['properties']['title'] = (   # type: ignore
        f'Отчёт на {now_date_time}'
    )
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEETS_BODY
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    logger.info(f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}')
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    now_date_time = datetime.now().strftime(FORMAT)
    TABLE_VALUES[0][1] = now_date_time
    table_values = []
    table_values.extend(TABLE_VALUES)
    for project in projects:
        new_row = [
            str(project['name']),
            format_timedelta(project['investing_time']),
            str(project['description']),
        ]
        table_values.append(new_row)
    UPDATE_BODY['values'] = table_values
    response = await wrapper_services.as_service_account( # noqa
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=UPDATE_BODY
        )
    )

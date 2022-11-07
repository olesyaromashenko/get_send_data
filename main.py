import json
import os
from typing import Optional

import requests
from google_drive_data_transfer.GoogleDriveDataTransfer import GoogleDriveDataTransfer

OPENWEATHERMAP_API_KEY = os.environ.get('owm_api_key')
PATH_GOOGLE_SECRETS = os.environ.get('google_secrets')


def get_weather(lat: float, lon: float, *, api_key: str = OPENWEATHERMAP_API_KEY, units: str = 'metric',
                lang: str = 'ru') -> Optional[dict]:
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}&lang={lang}"
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    print(f'Error {response.status_code} content: {response.json()}')
    return None


def save_result_to_file(data: str) -> str:
    file = './weather.json'
    with open(file, 'w') as f:
        f.write(data)
    return file


def save_result_to_gdrive(file_name):
    auth_dir = PATH_GOOGLE_SECRETS
    drive = GoogleDriveDataTransfer(auth_dir)
    drive.upload_file(file_name)


def main():
    lat = 55.75
    lon = 37.6167
    if not OPENWEATHERMAP_API_KEY or not PATH_GOOGLE_SECRETS:
        raise ValueError('Please configure environ. owm_api_key and google_secrets must be specified')
    if weather := get_weather(lat, lon):
        return save_result_to_gdrive(save_result_to_file(json.dumps(weather)))


if __name__ == "__main__":
    main()

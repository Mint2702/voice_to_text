import requests
from loguru import logger
from datetime import datetime, timedelta

from settings import settings


class Erudite:
    ERUDITE_API_URL = "https://nvr.miem.hse.ru/api/erudite/records"
    ERUDITE_API_KEY = settings.erudite_api_key

    @classmethod
    def get_all_records_per_day(cls) -> list:
        today = datetime.today().date() - timedelta(days=1)
        fromdate = f"{today} 9:00:00"
        todate = f"{today} 21:00:00"

        params = {"fromdate": fromdate, "todate": todate}
        r = requests.get(cls.ERUDITE_API_URL, params=params)
        code = r.status_code
        if code == 200:
            return r.json()
        elif code == 404:
            logger.warning(f"No records for {fromdate} found")
            return []
        else:
            logger.error(f"Erudite returned - {code}")
            return []

    @classmethod
    def patch_record(cls, keywords: list, record_id: str) -> None:
        data = {"keywords": keywords}
        r = requests.patch(
            f"{cls.ERUDITE_API_URL}/{record_id}",
            json=data,
            headers={"key": cls.ERUDITE_API_KEY},
        )
        code = r.status_code
        if code == 200:
            logger.info("Record updated successfully")
        elif code == 404:
            logger.warning(f"Record with id - {record_id} not found")
        else:
            logger.error(f"Erudite returned - {code}")

    @staticmethod
    def filter_records(records: list) -> list:
        offline = []
        zoom = []
        jitsi = []
        for record in records:
            if record["type"] == "Offline":
                offline.append(record)
            elif record["type"] == "Zoom":
                zoom.append(record)
            elif record["type"] == "Jitsi":
                jitsi.append(record)

        return offline, zoom, jitsi

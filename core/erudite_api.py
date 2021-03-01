import requests
from loguru import logger
from datetime import datetime, timedelta

from settings import settings


class Erudite:
    ERUDITE_API_URL = "https://nvr.miem.hse.ru/api/erudite/records"
    ERUDITE_API_KEY = settings.erudite_api_key

    def __init__(self) -> None:
        self.fromdate = f"{self.set_dates()} 9:00:00"
        self.todate = f"{self.set_dates()} 21:00:00"

    def set_dates(self) -> str:
        today = datetime.today().date() - timedelta(days=1)
        return today

    def get_all_records_per_day(self) -> list:
        params = {"fromdate": self.fromdate, "todate": self.todate}
        r = requests.get(self.ERUDITE_API_URL, params=params)
        code = r.status_code
        if code == 200:
            return r.json()
        elif code == 404:
            logger.warning(f"No records for {self.fromdate} found")
            return []
        else:
            logger.error(f"Erudite returned - {code}")
            return []

    def patch_record(self, keywords: list, record_id: str) -> None:
        data = {"keywords": keywords}
        r = requests.patch(
            f"{self.ERUDITE_API_URL}/{record_id}",
            json=data,
            headers={"key": self.ERUDITE_API_KEY},
        )
        code = r.status_code
        if code == 200:
            return r.json()
        elif code == 404:
            logger.warning(f"Record with id - {record_id} not found")
            return []
        else:
            logger.error(f"Erudite returned - {code}")
            return []

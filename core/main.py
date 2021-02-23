import requests
import date

params = {"fromdate": "2021-02-19 9:30:00", "todate": "2021-02-22 21:01:32.532552"}
r = requests.get("https://nvr.miem.hse.ru/api/erudite/records", params=params)
print(r.json())


class EruditeRecords:
    def __init__(self):
        self.fromdate = 1

    def set_dates(self):
        today = datetime.datetime.today()
        return

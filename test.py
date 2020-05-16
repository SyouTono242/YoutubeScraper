from datetime import datetime

date = "May 7, 2020"
datetime_object = datetime.strptime(date, "%b %d, %Y").date()
print(str(datetime_object).replace("-","."))

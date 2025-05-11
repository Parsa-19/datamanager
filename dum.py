
import datetime
from datetime import timedelta, date

now = datetime.datetime.now()
print(now)

end_date = now + timedelta(days=10)
print(end_date)
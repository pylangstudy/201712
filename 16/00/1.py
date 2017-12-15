import ssl
timestamp = ssl.cert_time_to_seconds("Jan  5 09:34:43 2018 GMT")
print(timestamp)
from datetime import datetime
print(datetime.utcfromtimestamp(timestamp))

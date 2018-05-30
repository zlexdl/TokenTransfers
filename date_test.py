
import datetime, time
from pymongo import MongoClient

conn = MongoClient('192.168.1.8', 27017)
db = conn.token_address
myset = db.btc
myset.save({"address":"ssss", "name":"btc_001"})

now = datetime.datetime.now()

# 前一小时
d1 = now - datetime.timedelta(hours=1)
print (d1.strftime("%Y-%m-%d %H:%S:%M"))

# 前一天
d2 = now - datetime.timedelta(days=1)
print (d2.strftime("%Y-%m-%d 00:00:00"))

now = datetime.datetime.now()

d1 = now - datetime.timedelta(days=1)

if datetime.datetime.strptime(str(d1), '%Y-%m-%d %H:%M:%S.%f') < d1:
    print('1')

hour_stamp = datetime.datetime.now().replace(hour=0, minute=0, second=0,microsecond=0)

print(hour_stamp)

print(type(hour_stamp))

print(time.mktime(time.strptime('2018-04-23 21:49:42', "%Y-%m-%d %H:%M:%S")))

#

#
# date_time = datetime.strptime(str(datetime.now()), '%b-%d-%Y %H:%M:%S %p')
#
# print(date_time)
#
# date_201712 = datetime.strptime('2017-12-01 00:00:01', '%Y-%m-%d %H:%M:%S')
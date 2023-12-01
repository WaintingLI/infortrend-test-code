import sys
import time
import datetime



s1 = "0.01% 06:19:56"
name = s1.split("% ")
print(name[1])

#將字串轉為秒數
num_get_meta = name[1].split(":")
num_get = int(num_get_meta[0])*60*60+int(num_get_meta[1])*60+int(num_get_meta[2])
print("num_get = ",num_get,"; type of num_get =",type(num_get))

#將字串轉為時間日期
date_time = datetime.datetime.strptime(name[1],"%H:%M:%S")
print("date_time =",date_time,"; type of date_time =",type(date_time))
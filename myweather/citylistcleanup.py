import json
import time
import codecs
start_time = time.time()
weatherstations = json.load(codecs.open('myweather/citylist.json', 'r', 'utf-8-sig'))
found=0
for i in data:
    if i["name"] == "Zabrze":
        found+=1
if(not found):
    print("Weather station not found")
else:
    print(i["id"],i["coord"])

elapsed_time = time.time() - start_time
print(elapsed_time)

with open("myweather/apikey.json", "r") as read_file:
    jsonkey = json.load(read_file)
    api_key=jsonkey["api_key"]
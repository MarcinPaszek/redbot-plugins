from redbot.core import commands
from redbot.core.data_manager import bundled_data_path
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import bs4
import datetime
import codecs
from pytz import timezone

class Weather(commands.Cog):
    """Weather cog"""

    @commands.command()
    async def weather(self, ctx, *, location):
        async def inspection(self, ctx, name):
            file_path = bundled_data_path(self) / 'citylist.json'
            try:
                weatherstations = json.load(codecs.open('citylist.json', 'r', 'utf-8-sig'))
                found=0
                for i in weatherstations:
                    if i["name"] == location:
                        found+=1
                if(not found):
                    await ctx.send("Weather station not found")
                else:
                    locationID=i["id"]
            except FileNotFoundError:
                return await ctx.send('Could not find the requested file')
        #weatherstations = json.load(codecs.open('citylist.json', 'r', 'utf-8-sig'))


     # get date and time
            timeNow=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            localTimeZone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
            #
            numberOfForecasts=5
            async def inspection(self, ctx, name):
                file_path = bundled_data_path(self) / 'apikey.json'
                try:
                    with open("apikey.json", "r") as read_file:
                        jsonkey = json.load(read_file)
                        api_key=jsonkey["api_key"]
                except FileNotFoundError:
                    return await ctx.send('Could not find the requested file')
            baseurl='https://api.openweathermap.org/'
            weather_url='data/2.5/weather?id='+str(locationID)+'&appid='+api_key
            forecast_url='data/2.5/forecast?id='+str(locationID)+'&appid='+api_key
            url=baseurl+weather_url
            uClient=urlopen(url)
            page_weather_json=uClient.read()
            uClient.close()
            jsonWeather = json.loads(page_weather_json)
            
            url=baseurl+forecast_url
            uClient=urlopen(url)
            page_forecast_json=uClient.read()
            uClient.close()
            jsonForecast = json.loads(page_forecast_json)
            
            listForecastsDateStamps=[]
            for forecastIdex in range(len(jsonForecast["list"])):
                listForecastsDateStamps.append(jsonForecast["list"][forecastIdex]["dt"])
            iteratorForecastsDateStamps=iter(listForecastsDateStamps)
            futureForecastDateStamp=0
            while(futureForecastDateStamp<=jsonWeather["dt"]):
                futureForecastDateStamp=next(iteratorForecastsDateStamps)
            
            listForecastTimes=[]
            listTemperatureForecasts=[]
            listHumidityForecasts=[]
            listWeatherForecasts=[]
            
            for i in range(numberOfForecasts):
                listTemperatureForecasts.append(round(list((x["main"]["temp"] for x in jsonForecast["list"] if x["dt"]==futureForecastDateStamp))[0]-273,1))
                listHumidityForecasts.append(list((x["main"]["humidity"] for x in jsonForecast["list"] if x["dt"]==futureForecastDateStamp))[0])
                listWeatherForecasts.append(list((x["weather"][0]["main"] for x in jsonForecast["list"] if x["dt"]==futureForecastDateStamp))[0])
                listForecastTimes.append(datetime.datetime.fromtimestamp(futureForecastDateStamp,localTimeZone).strftime("%d.%m.%Y %H:%M"))
                futureForecastDateStamp=next(iteratorForecastsDateStamps)
            #print(listTemperatureForecasts,listHumidityForecasts,listWeatherForecasts)
            #print(listForecastTimes)
            
            #  format weather into variables
            outsideTemperature=round(jsonWeather["main"]['temp']-273,1)
            outsideWeather=jsonWeather["weather"][0]["main"]
            outsideHumidity=jsonWeather["main"]['humidity']
            tupleWeather = (timeNow,outsideTemperature,outsideHumidity,outsideWeather)
            listoftupleForecasts=[]
            for i in range(numberOfForecasts):
                listoftupleForecasts.append((listForecastTimes[i],listTemperatureForecasts[i],listHumidityForecasts[i],listWeatherForecasts[i]))
            
            await ctx.send("Displaying weather for: "+location)
            await ctx.send(str(tupleWeather[0])+", Temperature: "+str(tupleWeather[1])+"°C, Humidity: "+str(tupleWeather[2])+"%, Weather: "+str(tupleWeather[3]))
            for i in range(numberOfForecasts):
                await ctx.send(str(listoftupleForecasts[i][0])+", Temperature: "+str(listoftupleForecasts[i][1])+"°C, Humidity: "+str(listoftupleForecasts[i][2])+"%, Weather: "+str(listoftupleForecasts[i][3]))

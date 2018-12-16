import os
import requests
import datetime

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

WEATHER_URL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore"
WEATHER_KEY = "CWB-CCC8945C-3B4E-46A9-B399-7736148D270A"
WEATHER_LOCATION = "%E8%87%BA%E5%8D%97%E5%B8%82"  # Tainan

NOW_YEAR = datetime.datetime.now().year
NOW_MONTH = datetime.datetime.now().month
NOW_DAY = datetime.datetime.now().day
NOW_HOUR = datetime.datetime.now().hour
NOW_MIN = datetime.datetime.now().minute
NOW_SEC = datetime.datetime.now().second
NOW_TIME = "{0}-{1}-{2} {3}:{4}:{5}".format(NOW_YEAR, NOW_MONTH, NOW_DAY, NOW_HOUR, NOW_MIN, NOW_SEC)
print_time = "{0}-{1}-{2} {3}:{4}".format(NOW_YEAR, NOW_MONTH, NOW_DAY, NOW_HOUR, NOW_MIN)

def forecast_3day_temp(id, text):
	'''每三小時為單位，顯示現在的溫度
		抓現在系統的時間去比對落在哪一時段
		第一個參數是使用者id，第二個參數是地區'''

	date_id = "F-D0047-077"
	
	weatherurl = "{0}/{1}?Authorization={2}&format=JSON&elementName=T".format(WEATHER_URL, date_id, WEATHER_KEY, WEATHER_LOCATION)
	weather = requests.get(weatherurl)
	if weather.status_code == requests.codes.ok:
		print("OK")

	body = weather.json()

	zone_num = 18  # 預設東區18
	for i in range(37):
		zone = body['records']['locations'][0]['location'][i]['locationName']
		if zone == text:
			zone_num = i
			break
	zone = body['records']['locations'][0]['location'][zone_num]['locationName']
	
	url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	title = "現在" + body['records']['locations'][0]['location'][0]['weatherElement'][0]['description']
	location = body['records']['locations'][0]['locationsName']
	weatherElement = body['records']['locations'][0]['location'][zone_num]['weatherElement'][0]['time']
	start_time = []
	end_time = []
	parameter = []
	toUser = []

	for i in range(24):
		if i < 23:
			start_time.append(weatherElement[i]['dataTime'])
		if i > 0:
			end_time.append(weatherElement[i]['dataTime'])
		parameter.append(weatherElement[i]['elementValue'][0]['value'])
		toUser.append(print_time + "\n" + parameter[i] + "°C")

	time_interval = split_time(start_time,end_time,NOW_TIME)
	if time_interval == None:
		time_interval = 1
	alltoUser = title + "\n" + location + " " + zone + "\n\n" + toUser[time_interval]

	payload = {
		"recipient": {"id": id},
		"message": {"text": alltoUser}
	}
	response = requests.post(url, json=payload)

	if response.status_code != 200:
		print("Unable to send message: " + response.text)
	return response.text

def forecast_3day(id, text, element):
	'''每三小時為單位，顯示現在的天氣狀況或降雨機率
		抓現在系統的時間去比對落在哪一時段
		第一個參數是使用者id，第二個參數是地區，第三個參數是詢問的天氣預報因子'''

	date_id = "F-D0047-077"
	elementName = "WeatherDescription"  # 預設全部顯示
	
	if element == 'PoP6h' or element == 'Wx':
		elementName = element
	
	weatherurl = "{0}/{1}?Authorization={2}&format=JSON&elementName={3}".format(WEATHER_URL, date_id, WEATHER_KEY, elementName)
	weather = requests.get(weatherurl)
	if weather.status_code == requests.codes.ok:
		print("OK")

	body = weather.json()

	zone_num = 18  # 預設東區18
	for i in range(37):
		zone = body['records']['locations'][0]['location'][i]['locationName']
		if zone == text:
			zone_num = i
			break
	zone = body['records']['locations'][0]['location'][zone_num]['locationName']
	
	url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	title = "現在" + body['records']['locations'][0]['location'][0]['weatherElement'][0]['description']
	location = body['records']['locations'][0]['locationsName']
	weatherElement = body['records']['locations'][0]['location'][zone_num]['weatherElement'][0]['time']
	start_time = []
	end_time = []
	parameter = []
	paracode = []
	toUser = []

	if element == 'PoP6h':
		for i in range(12):
			start_time.append(weatherElement[i]['startTime'])
			end_time.append(weatherElement[i]['endTime'])
			parameter.append(weatherElement[i]['elementValue'][0]['value'])
			toUser.append(print_time + "\n" + parameter[i])
	else:
		for i in range(24):
			start_time.append(weatherElement[i]['startTime'])
			end_time.append(weatherElement[i]['endTime'])
			parameter.append(weatherElement[i]['elementValue'][0]['value'])
			paracode.append(weatherElement[i]['elementValue'][1]['value'])
			parameter[i] = add_unicode(paracode[i], parameter[i])
			toUser.append(print_time + "\n" + parameter[i])

	time_interval = split_time(start_time,end_time,NOW_TIME)
	alltoUser = title + "\n" + location + " " + zone + "\n\n" + toUser[time_interval]

	payload = {
		"recipient": {"id": id},
		"message": {"text": alltoUser}
	}
	response = requests.post(url, json=payload)

	if response.status_code != 200:
		print("Unable to send message: " + response.text)
	return response.text

def forecast_1week(id, text):
	'''每十二小時為單位，顯示未來一周的天氣狀況
		判斷抓到的資料如果起始時間跟結束時間都是同一天，將那天的天氣狀況複寫
		第一個參數是使用者id，第二個參數是地區'''

	date_id = "F-D0047-079"  # 台南
	weatherurl = "{0}/{1}?Authorization={2}&format=JSON&elementName=WeatherDescription".format(WEATHER_URL, date_id, WEATHER_KEY)
	weather = requests.get(weatherurl)
	if weather.status_code == requests.codes.ok:
		print("OK")

	body = weather.json()

	zone_num = 18  # 預設東區18
	for i in range(37):
		zone = body['records']['locations'][0]['location'][i]['locationName']
		if zone == text:
			zone_num = i
			break
	zone = body['records']['locations'][0]['location'][zone_num]['locationName']

	url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	title = "未來一週綜合天氣預報"
	location = body['records']['locations'][0]['locationsName']
	weatherElement = body['records']['locations'][0]['location'][zone_num]['weatherElement'][0]['time']
	start_time = []
	end_time =[]
	parameter = []
	toUser = []

	j = 0
	for i in range(14):
		start_time.append(weatherElement[i]['startTime'])
		end_time.append(weatherElement[i]['endTime'])
		if start_time[i][:10] == end_time[i][:10]:
			if j > 0 and start_time[i][:10] == toUser[j-1][:10]:
				j = j - 1
			parameter.append(weatherElement[i]['elementValue'][0]['value'])
			toUser.append(start_time[i][:10] + "\n" + parameter[j])
			j = j + 1
			
	alltoUser = title + "\n" + location + " " + zone
	for i in range(j):
		alltoUser = alltoUser + "\n\n" + toUser[i]

	payload = {
		"recipient": {"id": id},
		"message": {"text": alltoUser}
	}
	response = requests.post(url, json=payload)

	if response.status_code != 200:
		print("Unable to send message: " + response.text)
	return response.text

def send_start(id, text):
	'''傳訊息
		第一個參數是使用者id，第二個參數是要傳送的訊息'''

	url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
	payload = {
		"recipient": {"id": id},
		"message": {"text": text}
	}
	response = requests.post(url, json=payload)

	if response.status_code != 200:
		print("Unable to send message: " + response.text)
	return response.text

def split_time(start, end, time):
	'''找出時間的區間
		第一個參數是起始時間的list，第二個參數是結束時間的list，第三個參數是想找出的時間區間
		回傳list的index'''
	index = 0
	t = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
	for s, e in zip(start, end):
		st = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
		et = datetime.datetime.strptime(e, '%Y-%m-%d %H:%M:%S')
		if(st <= t and et > t):
			return index
		index += 1

def add_unicode(paracode, text):
	'''在回傳的天氣狀況前面加上符號
		第一個參數是天氣描述代碼，第二個參數是天氣狀況'''

	cloud = ['02', '05', '06', '49', '58']
	rain = ['04', '12', '17', '26', '29', '31']
	umbrella = ['13', '18', '24', '34', '36', '57', '59']
	mine = ['17', '29', '31', '36']
	if paracode == '07' or paracode == '08':
		text = u'\u26c5 ' + text  # 雲和太陽
	if paracode == '01':
		text = u'\u2600 ' + text  # 太陽
	if paracode in cloud:
		text = u'\u2601 ' + text  # 雲
	if paracode in rain:
		text = u'\u2614 ' + text  # 雨
	if paracode in umbrella:
		text = u'\uf302 ' + text  # 陣雨
	if paracode in mine:
		text = u'\u26a1 ' + text  # 雷
	if paracode == '60' or paracode == '61':
		text = u'\u26c4 ' + text  # 雪
	return text
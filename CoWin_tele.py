import requests
import time
from datetime import datetime

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot1834001435:AAFB10yJxE2nYHema0mVjIg20csgkzecnwo/sendMessage?chat_id=@__groupid__&text="
group_id = "WinOverCovid_India"
tricity_ids = [187, 108, 496]
##187 FOR MOHALI
##108 FOR CHANDIGARH
##496 FOR PANCHKULA
def fetch_data_from_cowin(district_id):
	query_params = "?district_id={}&date={}".format(district_id, today_date)
	final_url = base_cowin_url+query_params
	response = requests.get(final_url)
	extract_availability_data(response)
	


def fetch_data_for_state(district_ids):
	for district_id in district_ids:
		fetch_data_from_cowin(district_id)

def extract_availability_data(response):
	response_json = response.json()
	for center in response_json["centers"]:
		for session in center["sessions"]:
			if session["available_capacity_dose1"] > 0 and session["min_age_limit"]==18:
				message = "Pincode: {}, Name: {}, Slots: {}, Minimum Age: {}".format(
					center["pincode"], center["name"],
					session["available_capacity_dose1"],
					session["min_age_limit"]
				)
				send_message_telegram(message)

def send_message_telegram(message):
	final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
	final_telegram_url = final_telegram_url + message
	response = requests.get(final_telegram_url)
	print(response)


if __name__ == "__main__":
	fetch_data_for_state(tricity_ids)
	time.sleep(60*60)

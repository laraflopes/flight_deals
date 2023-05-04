import requests

SHEETY_GET_ENDPOINT = "https://api.sheety.co/"
SHEETY_PUT_ENDPOINT = "https://api.sheety.co/"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/"

class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.costumer_data = ""

    def get_destination_data(self):
        response = requests.get(url=SHEETY_GET_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PUT_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def get_emails(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        self.costumer_data = data["users"]
        return self.costumer_data

    # def update_destination_data(self, new_data):
    #     try
    #         #put SHEETY_PUT_ENDPOINT
    #     except
    #
    #     self.__update_destination_data_attrb(new_data)
    #
    # def __update_destination_data_attrb(self, new_data):
    #     self.destination_data = new_data

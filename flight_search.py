import requests
from flight_data import FlightData
from pprint import pprint

TEQUILA_KEY = "secret key"
GET_IATA_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
SEARCH_FLIGHTS_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API

    def get_iata_code(self, city_name):
        headers = {
            "apikey": TEQUILA_KEY
        }
        query_params = {
            "term": city_name,
            "location_types": "city",
            "active_only": True
        }
        response = requests.get(url=GET_IATA_ENDPOINT, params=query_params, headers=headers)
        response.raise_for_status()
        code = response.json()["locations"][0]["code"]
        return code

    def check_flights(self, code_from, code_to, date_from, date_to):
        headers = {
            "apikey": TEQUILA_KEY
        }
        params = {
            "fly_from": code_from,
            "fly_to": code_to,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "EUR",
            "max_stopovers": 0
        }
        response = requests.get(url=SEARCH_FLIGHTS_ENDPOINT, params=params, headers=headers)
        ##################################################################################
        try:
            data = response.json()["data"][0]
        except IndexError:
            params["max_stopovers"] = 1
            response = requests.get(url=SEARCH_FLIGHTS_ENDPOINT, params=params, headers=headers)
            try:
                data = response.json()["data"][0]
                pprint(data)
            except IndexError:
                print(f"There are no flights to {code_to}")
                return None
            except:
                print("Unknown error.")
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    departure_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                departure_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            return flight_data
    ################################################################################


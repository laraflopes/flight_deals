# This file will need to use the DataManager,FlightSearch,
# FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

ORIGIN_CITY_CODE = "LON"

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# If the first element is the only one populated the code doesn't run tp
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata_code(row["city"])
# Never change an attribute without/outside a class method
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_CODE,
        destination["iataCode"],
        tomorrow,
        six_months
    )
    ##################
    if flight is None:
        continue
    #################
    if flight.price < destination["lowestPrice"]:

        users = data_manager.get_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message=f"Low price alert! Only {flight.price}€ to fly from {flight.origin_city}-" \
                f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, " \
                f"from {flight.departure_date} to {flight.return_date}"

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)
        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}." \
               f"{flight.departure_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        notification_manager.send_email(message, emails, link)


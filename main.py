import os
import json
import csv
import time 
import gooey
import dotenv
import textwrap
import googlemaps

dotenv.load_dotenv()

"""
Main application with Gooey
to switch from CLI use --ignore-gooey
"""
@gooey.Gooey(
    # GUI setup
    program_name=f"google-maps-api-with-apify",
    required_cols=1,
    default_size=(400, 800),
)
def main():
    # Gooey parser
    parser = gooey.GooeyParser()

    # Required argument API key
    # key can be found in credentials
    # make sure Places API is enabled
    # and geocoding API
    parser.add_argument(
        "--google_api_key",

        default=os.environ.get("GOOGLE_API_KEY"),

        help="google project api key " + \
            "make sure places and geocode API " + 
            "is enabled.",
    )

    # Required argment places_search
    # filter the search results using a certain keyword
    # i.e coffee pizza
    parser.add_argument(
        "--places_search",
        type=str,

        default=os.environ.get("PLACES_SEARCH"),
        
        help="filter the search results using a certain keyword" + \
            "i.e coffee pizza",
    )

    # Required argumnet places_location
    # filter the search results by location
    # i.e chicago 
    parser.add_argument(
        "--places_location",
        type=str,
        
        default=os.environ.get("PLACES_LOCATION"),

        help="filter the search results by location"
    )

    # Required argumnet places_type
    # filter the search results with valid place types
    # i.e restaurant accounting
    parser.add_argument('--places_type', 
        widget='Dropdown',
        type=str,

        default=os.environ.get("PLACES_TYPE"),

        choices=[
            "accounting",
            "airport",
            "amusement_park",
            "aquarium",
            "art_gallery",
            "atm",
            "bakery",
            "bank",
            "bar",
            "beauty_salon",
            "bicycle_store",
            "book_store",
            "bowling_alley",
            "bus_station",
            "cafe",
            "campground",
            "car_dealer",
            "car_rental",
            "car_repair",
            "car_wash",
            "casino",
            "cemetery",
            "church",
            "city_hall",
            "clothing_store",
            "convenience_store",
            "courthouse",
            "dentist",
            "department_store",
            "doctor",
            "drugstore",
            "electrician",
            "electronics_store",
            "embassy",
            "fire_station",
            "florist",
            "funeral_home",
            "furniture_store",
            "gas_station",
            "gym",
            "hair_care",
            "hardware_store",
            "hindu_temple",
            "home_goods_store",
            "hospital",
            "insurance_agency",
            "jewelry_store",
            "laundry",
            "lawyer",
            "library",
            "light_rail_station",
            "liquor_store",
            "local_government_office",
            "locksmith",
            "lodging",
            "meal_delivery",
            "meal_takeaway",
            "mosque",
            "movie_rental",
            "movie_theater",
            "moving_company",
            "museum",
            "night_club",
            "painter",
            "park",
            "parking",
            "pet_store",
            "pharmacy",
            "physiotherapist",
            "plumber",
            "police",
            "post_office",
            "primary_school",
            "real_estate_agency",
            "restaurant",
            "roofing_contractor",
            "rv_park",
            "school",
            "secondary_school",
            "shoe_store",
            "shopping_mall",
            "spa",
            "stadium",
            "storage",
            "store",
            "subway_station",
            "supermarket",
            "synagogue",
            "taxi_stand",
            "tourist_attraction",
            "train_station",
            "transit_station",
            "travel_agency",
            "university",
            "veterinary_care",
            "zoo"
        ],
        help='filter the search results with valid place types.', 
    )


    # Required argument place_results
    # Limit the search to a specific number
    parser.add_argument(
        "--places_max_result",
        type=int,

        default=os.environ.get("PLACES_MAX_RESULT"),

        help="Limit the search to a specific number"
    )
    
    # Parse arguments
    args = parser.parse_args()

    # Google maps client
    client = googlemaps.Client(args.google_api_key)
    client_max_results = args.places_max_result
    geocode = client.geocode(address=args.places_location)[0] \
        ["geometry"]["location"]

    
    
    # Container for resultsclear
    places = []

    # token for getting the next results
    page_token = False

    # get complete details of each place
    with open("main.tsv", "wt", newline="", encoding="utf-8") as tsv:
        tsv_write = csv.writer(tsv, delimiter="\t")

        # write columns
        tsv_write.writerow([
            "Name",
            "Address",
            "Phone Number",
            "Website",
            "Monday Hours",
            "Tuesday Hours",
            "Wednesday Hours",
            "Thursday Hours",
            "Friday Hours",
            "Saturday Hours",
            "Sunday Hours"
        ])
    
        # if container is less than max results
        result_counter = 0
        while result_counter != client_max_results:
    
            if not page_token and len(places) <= 0:            
                # search for places
                data = client.places(

                    # query i.e coffee shop
                    query=args.places_search,

                    # type i.e restaurant
                    type=args.places_type,

                    # lat ang long from geocode
                    location=f"{geocode['lat']},{geocode['lng']}",
                )

                # assign next page token
                page_token = data.get("next_page_token")

            elif page_token:
                # delay the next request
                # sometimes google server needs
                # time to serve the next page token
                time.sleep(3)

                # search for places using the next page
                data = client.places(page_token=page_token)
            
            else:
                # break the loop
                # no more search results
                data = False

            if not data:
                break

            # for each data results 
            for place in data["results"]:
                
                # skip if the business if closed
                if place["business_status"] != "OPERATIONAL":
                    continue


                result_counter += 1

                place_id = place["place_id"]
                # request for specific details of a place
                data = client.place(place_id=place_id,
                    fields=[
                        "name",
                        "formatted_address",
                        "opening_hours",
                        "formatted_phone_number",
                        "website"
                    ]
                )

                # place details
                place = data["result"]
                print(f"{result_counter}: {place['name']}")

                # write initial fields 
                tsv_fields = [
                    place.get("name") or "n/a",
                    place.get("formatted_address") or "n/a",
                    place.get("formatted_phone_number") or "n/a",
                    place.get("website") or "n/a"
                ]

                


                # parse and clean opening hours
                opening_fields = []
                opening_hours = place.get("opening_hours")
                
                # container for days
                days = [
                    "Monday", 
                    "Tuesday", 
                    "Wednesday", 
                    "Thursday", 
                    "Friday", 
                    "Saturday", 
                    "Sunday"
                ]

                # we only parse if it exists
                if opening_hours:
                    # loop through each day
                    for index, day in enumerate(days):          
                        try:
                            period = opening_hours["periods"][index]
                            
                            
                            # get opening closing periods
                            _open = period["open"]
                            _close = period["close"]
                            

                            # 2200 -> 22:00
                            opening_hour = ":".join(textwrap.wrap(_open["time"], 2))
                            closing_hour = ":".join(textwrap.wrap(_close["time"], 2))

                            opening_fields.append(f"{opening_hour} - {closing_hour}")
                        
                        except IndexError:
                            # Fallback if index of day
                            # does not exist
                            opening_fields.append("n/a")

                        
                else:
                    # fallback if no hours specified
                    opening_fields = ["n/a" for x in days]


                
                # combine fields
                tsv_fields = tsv_fields + opening_fields
                
                # finally write the rows
                tsv_write.writerow(tsv_fields)

        # end
        tsv.close()

    



if __name__ == "__main__":
    main()
# Google Places API Search

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@sagocodes.work/how-to-scrape-tweets-and-automatically-like-using-python-faed9d97470b) [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee/sagocodes)

![Pasted image 20221023153042](https://user-images.githubusercontent.com/101981345/197380816-a335cf24-3586-4e52-bab0-b6ac60e08338.png)


Using [googlemaps](https://github.com/googlemaps/google-maps-services-python) (geocode and places) fetch businesses and their details then output the results to .tsv

## Quickstart

```
$ pip install -r requirements.txt
$ python main.py
```


## Usage

```
$ python main.py --help --ignore--gooey
usage: main.py [-h] 
	[--google_api_key GOOGLE_API_KEY] 
	[--places_search PLACES_SEARCH] 
	[--places_location PLACES_LOCATION]
	[--places_type {...types}]
  [--places_max_result PLACES_MAX_RESULT]

options:
  -h, --help            show this help message and exit
  --google_api_key GOOGLE_API_KEY
                        google project api key make sure places and geocode API is enabled.
  --places_search PLACES_SEARCH
                        filter the search results using a certain keyword
  --places_location PLACES_LOCATION
                        filter the search results by location
  --places_type {..types}
                        filter the search results with valid place types.
  --places_max_result PLACES_MAX_RESULT
                        Limit the search to a specific number
```



## ENV

```
GOOGLE_API_KEY=
PLACES_SEARCH=
PLACES_LOCATION=
PLACES_TYPE=
PLACES_MAX_RESULT=
```


*DISCLAIMER*

*This repository has been created purely for learning purposes. Project maintainers are not responsible if a user gets banned, blocked or be liable for misuse of the tool. Use responsibly.*

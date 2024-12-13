import requests


def geo_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1
    }

    headers = {
        # Replace with your app details
        'User-Agent': 'showa_available/1.0 (adepojuadebobola6@gmail.com)'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("Raw response:", data)

        if data:
            return {
                "latitude": data[0]["lat"],
                "longitude": data[0]["lon"],

            }
        else:
            print("No results found for the address.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error while geocoding: {e}")
        return None

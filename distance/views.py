from django.shortcuts import render

# Create your views here.

from geopy.distance import geodesic
import requests
from django.http import JsonResponse


import requests
from django.http import JsonResponse
from geopy.distance import geodesic


from django.conf import settings


def plan_trip(request, origin_code_or_coords, destination_code_or_coords, mode="car"):
    """
    Plan a trip by car or plane.

    - mode: 'car' or 'plane'
    - origin_code_or_coords / destination_code_or_coords:
        * for plane: IATA airport codes
        * for car: "lat,lon" string
    """
#we collect our destination and origin airports here by using AviationStack API
    def get_airports(iata_code):
        url = "https://api.aviationstack.com/v1/airports"
        params = {"access_key": settings.AVIATION_STACK_API_KEY, "iata_code": iata_code}
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            a = data.get("data", [])[0]

#we need the find the cordinates of airport by latitude and longitude. Then calculates the distance between them
            return (a.get("latitude"), a.get("longitude"))
        except:
            return None

    if mode == "plane":
        origin_coords = get_airports(origin_code_or_coords)
        dest_coords = get_airports(destination_code_or_coords)

        if not origin_coords or not dest_coords:
            return JsonResponse({"error": "Airport not found"}, status=404)
        
#to calculate we use geopy library. It takes two parameters. Latitude and longitude. 
        distance_km = geodesic(origin_coords, dest_coords).km
# by average plane speed 
        travel_time = distance_km / 850  # avg plane speed
# by average cost in per km . (The average cost per kilometer for a flight is around $0.06 to $0.15)
        cost = 50 + (distance_km * 0.07)

        return JsonResponse({
            "mode": "plane",
            "origin_code": origin_code_or_coords,
            "destination_code": destination_code_or_coords,
            "distance_km": round(distance_km, 2),
            "travel_time_hours": round(travel_time, 2),
            "cost_estimate": round(cost, 2)
        })

    elif mode == "car":
        try:
            # Parse coordinates
            origin_lat, origin_lon = map(float, origin_code_or_coords.split(","))
            dest_lat, dest_lon = map(float, destination_code_or_coords.split(","))

            url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
            headers = {"Authorization": settings.OPEN_ROUTE_SERVICE_API_KEY}
            body = {
                "coordinates": [[origin_lon, origin_lat], [dest_lon, dest_lat]]
            }

            res = requests.post(url, json=body, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()

            # Check if 'features' exists
            if "features" not in data or len(data["features"]) == 0:
                return JsonResponse({"error": "No route found. Check coordinates or route length.", "raw": data}, status=400)

            route = data["features"][0]["properties"]["segments"][0]
            distance_km = route["distance"] / 1000
            travel_time_hours = route["duration"] / 3600

            return JsonResponse({
                "mode": "car",
                "origin_coords": [origin_lat, origin_lon],
                "destination_coords": [dest_lat, dest_lon],
                "distance_km": round(distance_km, 2),
                "travel_time_hours": round(travel_time_hours, 2)
            })

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Request failed", "details": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Unexpected error", "details": str(e)}, status=400)

        

# def search_airports(request):

#     country=request.GET.get('country')
#     code=request.GET.get('code')

#     url="http://api.aviationstack.com/v1/airports"
#     params={"access_key":AVIATION_STACK_API_KEY}

#     if country:
#         params["country_iso2"] = country
    
#     if code:
#         params["iata_code"] = code
        
#     response = requests.get(url,params=params)
#     data=response.json()

#     airports=[
#        {
#         "code": a.get("iata_code"),
#         "name": a.get("airport_name"),
#         "city": a.get("city", "Unknown"),
#         "country": a.get("country_name"),
#         "lat": a.get("latitude"),
#         "lon": a.get("longitude"),
#     }
#         for a in data.get("data", [])
#         if a["iata_code"] and a["latitude"] and a["longitude"]
#     ]
#     return JsonResponse({"results":airports})
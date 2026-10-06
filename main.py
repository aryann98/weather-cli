import requests as rt
from colorama import Fore, Style


geo_url = "https://geocoding-api.open-meteo.com/v1/search"
weather_url = "https://api.open-meteo.com/v1/forecast"


# -------------------------
# App Header
# -------------------------

print()
print(Fore.CYAN + Style.BRIGHT + "╔══════════════════════════════╗")
print("║        WEATHER CLI APP       ║")
print("╚══════════════════════════════╝" + Style.RESET_ALL)
print()


user_input = input(
    Fore.YELLOW + Style.BRIGHT
    + "Enter City Name: "
    + Style.RESET_ALL
)


# -------------------------
# Geocoding Request
# -------------------------

geo_params = {
    "name": user_input,
    "count": 1
}

try:
    response = rt.get(
        geo_url,
        params=geo_params,
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        print(
            Fore.RED + Style.BRIGHT
            + "\n✗ City not found!"
            + Style.RESET_ALL
        )
        exit()

    location = data["results"][0]


    # -------------------------
    # Weather Request
    # -------------------------

    weather_params = {
        "longitude": location["longitude"],
        "latitude": location["latitude"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    weather_response = rt.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()
    weather_information = weather_data["current"]


    # -------------------------
    # Weather Output
    # -------------------------

    print()
    print(Fore.CYAN + Style.BRIGHT + "┌──────────────────────────────┐")
    print("│        CURRENT WEATHER       │")
    print("└──────────────────────────────┘" + Style.RESET_ALL)

    print(
        Fore.WHITE + Style.BRIGHT
        + "  City        : "
        + Fore.GREEN
        + location["name"]
        + Style.RESET_ALL
    )

    print(
        Fore.WHITE + Style.BRIGHT
        + "  Time        : "
        + Fore.GREEN
        + weather_information["time"]
        + Style.RESET_ALL
    )

    print(
        Fore.WHITE + Style.BRIGHT
        + "  Temperature : "
        + Fore.GREEN
        + f'{weather_information["temperature_2m"]} °C'
        + Style.RESET_ALL
    )

    print(
        Fore.WHITE + Style.BRIGHT
        + "  Wind Speed  : "
        + Fore.GREEN
        + f'{weather_information["wind_speed_10m"]} km/h'
        + Style.RESET_ALL
    )

    print(
        Fore.WHITE + Style.BRIGHT
        + "  Humidity    : "
        + Fore.GREEN
        + f'{weather_information["relative_humidity_2m"]}%'
        + Style.RESET_ALL
    )

    print()


except rt.exceptions.Timeout:
    print(
        Fore.RED + Style.BRIGHT
        + "\n✗ Request timed out. Please try again."
        + Style.RESET_ALL
    )

except rt.exceptions.RequestException:
    print(
        Fore.RED + Style.BRIGHT
        + "\n✗ Network/API request failed."
        + Style.RESET_ALL
    )

except (KeyError, TypeError):
    print(
        Fore.RED + Style.BRIGHT
        + "\n✗ Unexpected response from the weather API."
        + Style.RESET_ALL
    )
from FlightRadar24.api import FlightRadar24API

# Glasgow airport box
AIRPORT_CODE = "YQR"
AIRPORT_BOX = (
    (50.44045660068935, -104.68327840842834),
    (50.42421889047764, -104.64808833115006),
)

# Glasgow runway box
RUNWAYS = {
    "Runway 1": (
        (50.43958365692861, -104.6723385156276),
        (50.44034143049153, -104.6715025835228),
        (50.4243870659345, -104.64925656954928),
        (50.42395712379187, -104.65012462603535),
    ),

    "Runway 2": (
        (50.42946600480248, -104.68217447507722),
        (50.42948735791148, -104.6578062943159),
        (50.42879101484094, -104.65709916386622),
        (50.42862633686695, -104.68230278674153)
    )
}


def point_in_a_box(polygon, lat, lon):
    """
    Check if a point (lat, lon) is inside a polygon defined by a list/tuple of (lat, lon) vertices.

    Args:
        point: (lat, lon) tuple
        polygon: iterable of (lat, lon) tuples

    Returns:
        True if point is inside polygon, False otherwise
    """
    inside = False

    n = len(polygon)
    for i in range(n):
        lat1, lon1 = polygon[i]
        lat2, lon2 = polygon[(i + 1) % n]

        # Check if the horizontal ray crosses this polygon edge
        if ((lon1 > lon) != (lon2 > lon)) and (
            lat < (lat2 - lat1) * (lon - lon1) / (lon2 - lon1) + lat1
        ):
            inside = not inside

    return inside


def look_at_runway():
    # Get the bounds for the airport and check for planes
    api = FlightRadar24API()
    airport_box = {
        "tl_x": AIRPORT_BOX[0][1],
        "tl_y": AIRPORT_BOX[0][0],
        "br_x": AIRPORT_BOX[1][1],
        "br_y": AIRPORT_BOX[1][0],
    }
    bounds = api.get_bounds(airport_box)
    flights = api.get_flights(bounds=bounds) or []

    for flight in flights:
        # If we've got valid lat/lon then test if the plane is in the runway box
        latitude = flight.latitude
        longitude = flight.longitude

        if latitude and longitude:
            # Loop through each runway we have defined
            for runway_name, runway_box in RUNWAYS.items():
                # See if the plane is in the runway box
                if point_in_a_box(runway_box, latitude, longitude):
                    # We have a plane in the runway box, so print out some info
                    origin = flight.origin_airport_iata or ""
                    dest = flight.destination_airport_iata or ""
                    landing = dest == AIRPORT_CODE

                    print(
                        f"{runway_name} -> {flight.callsign} | {origin} to {dest} | {'LANDING' if landing else 'TAKING OFF'}"
                    )


if __name__ == "__main__":
    look_at_runway()

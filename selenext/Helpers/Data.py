from difflib import SequenceMatcher
from math import radians, sin, cos, sqrt, asin


def levenshtein_distance(s1, s2):
    """
    The minimum amount of edits needed to make s2 into s1.

    Args:
        s1: string
        s2: string

    Returns:
        int

    """

    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2+1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(
                    1 + min(
                        (
                            distances[index1],
                            distances[index1+1],
                            new_distances[-1]
                        )
                    )
                )
        distances = new_distances
    distance = distances[-1]
    return distance


def string_similarity(s1, s2):
    """
    Get a float representation of the difference between 2 strings.

    Args:
        s1: string
        s2: string

    Returns: float
    """

    return SequenceMatcher(None, s1, s2).ratio()


def haversine(lat1, lon1, lat2, lon2, units='metric'):
    """

    Args:
        lat1: float
        lon1: float
        lat2: float
        lon2: float

    Returns: float

    """
    earth_radius = 6372.8  # Earth radius in kilometers

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    km = earth_radius * c

    if units == 'metric':
        return km
    elif units == 'imperial':
        # Return miles.
        return km / 1.609344
    else:
        return km


# if __name__ == '__main__':
#     print haversine(45.5231, 122.6765, 39.7392, 104.9903, units='imperial')
#     print string_similarity('Hello World', 'Hello WOrld!')
#     print levenshtein_distance('Hello World', 'Hello WOrld!')

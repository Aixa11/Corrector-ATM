import pyproj
from datetime import datetime

def calculate_solar_position(latitude, longitude, date_time):
    # Calcular la posición solar
    solar = pyproj.Proj(proj='eqc', ellps='WGS84')
    solar_position = solar(longitude, latitude, date_time)
    return solar_position

# Ejemplo de uso
lat = -34.6037
lon = -58.3816
date_time = datetime(2023, 7, 4, 12, 0, 0)
solar_pos = calculate_solar_position(lat, lon, date_time)
print("Posición Solar:", solar_pos)

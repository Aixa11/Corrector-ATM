import numpy as np
from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timezone
from Py6S import SixS, AtmosProfile, AeroProfile, Geometry, Wavelength

def get_solar_position(latitude, longitude, date_time):
    """
    Calcula la elevación y el azimut solar para una ubicación y tiempo específicos.
    """
    solar_elevation = get_altitude(latitude, longitude, date_time)
    solar_azimuth = get_azimuth(latitude, longitude, date_time)
    return solar_elevation, solar_azimuth

def atmospheric_correction(solar_elevation, solar_azimuth):
    """
    Realiza la corrección atmosférica utilizando Py6S.
    """
    s = SixS()
    s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeSummer)
    s.aero_profile = AeroProfile.PredefinedType(AeroProfile.Maritime)
    s.geometry = Geometry.User()
    s.geometry.solar_z = 90 - solar_elevation  # ángulo zenital
    s.geometry.solar_a = solar_azimuth
    s.geometry.view_z = 0
    s.geometry.view_a = 0
    s.wavelength = Wavelength(0.56)  # banda verde
    s.run()
    return s.outputs.atmos_corrected_reflectance

def correct_reflectance(reflectance, solar_elevation):
    """
    Aplica la corrección de reflectancia basada en el ángulo de elevación solar.
    """
    corrected_reflectance = reflectance / np.cos(np.radians(90 - solar_elevation))
    return corrected_reflectance

def calculate_et(tmean, tmax, tmin, rh_mean, u2, rs, elevation):
    """
    Calcula la evapotranspiración (ET) usando la fórmula de Penman-Monteith.
    """
    G = 0  # Flujo de calor del suelo (MJ/m²/día)
    gamma = 0.665e-3 * (101.3 * ((293 - 0.0065 * elevation) / 293) ** 5.26)  # Constante psicrométrica (kPa/°C)
    delta = (4098 * (0.6108 * np.exp((17.27 * tmean) / (tmean + 237.3)))) / (tmean + 237.3) ** 2  # Pendiente de la curva de presión de vapor (kPa/°C)
    es = (0.6108 * np.exp((17.27 * tmax) / (tmax + 237.3)) + 0.6108 * np.exp((17.27 * tmin) / (tmin + 237.3))) / 2  # Presión de vapor de saturación (kPa)
    ea = es * rh_mean / 100  # Presión de vapor real (kPa)
    
    # Fórmula de Penman-Monteith
    et = (0.408 * delta * (rs - G) + gamma * (900 / (tmean + 273)) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))
    return et

# Datos de ejemplo (deben ser reemplazados con datos reales)
latitude = -34.6037
longitude = -58.3816
date_time = datetime(2023, 7, 4, 12, 0, 0, tzinfo=timezone.utc)

tmean = 25.0
tmax = 30.0
tmin = 20.0
rh_mean = 60.0
u2 = 2.0
rs = 20.0
elevation = 100.0
reflectance = 0.2  # Ejemplo de reflectancia sin corregir

# Obtención de la posición solar
solar_elevation, solar_azimuth = get_solar_position(latitude, longitude, date_time)
print(f"Elevación solar: {solar_elevation} grados")
print(f"Azimut solar: {solar_azimuth} grados")

# Corrección atmosférica
atmos_corrected_reflectance = atmospheric_correction(solar_elevation, solar_azimuth)
print(f"Reflectancia corregida atmosféricamente: {atmos_corrected_reflectance}")

# Corrección por el ángulo de iluminación solar
corrected_reflectance = correct_reflectance(atmos_corrected_reflectance, solar_elevation)
print(f"Reflectancia corregida por el ángulo de iluminación solar: {corrected_reflectance}")

# Cálculo de la evapotranspiración (ET)
et = calculate_et(tmean, tmax, tmin, rh_mean, u2, rs, elevation)
print("Evapotranspiración (ET):", et, "mm/día")

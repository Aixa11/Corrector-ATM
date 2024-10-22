#Cálculo de Evapotranspiración (ET) usando el método de Penman-Monteith

#Podes visualizarlo con matplotlib u seaborn, etc

#https://www.fao.org/4/X0490E/x0490e00.htm 

import math

def calculate_et(tmean, tmax, tmin, rh_mean, u2, rs, elevation):
    """
    Cálculo de la evapotranspiración (ET) usando la fórmula de Penman-Monteith.
    
    tmean: Temperatura media (°C)
    tmax: Temperatura máxima (°C)
    tmin: Temperatura mínima (°C)
    rh_mean: Humedad relativa media (%)
    u2: Velocidad del viento a 2m (m/s)
    rs: Radiación solar (MJ/m²/día)
    elevation: Elevación del sitio (m)
    """
    # Constantes
    G = 0  # Flujo de calor del suelo (MJ/m²/día)
    gamma = 0.665e-3 * (101.3 * ((293 - 0.0065 * elevation) / 293) ** 5.26)  # Constante psicrométrica (kPa/°C)
    delta = (4098 * (0.6108 * math.exp((17.27 * tmean) / (tmean + 237.3)))) / (tmean + 237.3) ** 2  # Pendiente de la curva de presión de vapor (kPa/°C)
    es = (0.6108 * math.exp((17.27 * tmax) / (tmax + 237.3)) + 0.6108 * math.exp((17.27 * tmin) / (tmin + 237.3))) / 2  # Presión de vapor de saturación (kPa)
    ea = es * rh_mean / 100  # Presión de vapor real (kPa)
    
    # Fórmula de Penman-Monteith
    et = (0.408 * delta * (rs - G) + gamma * (900 / (tmean + 273)) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))
    return et

# Datos de ejemplo
tmean = 25.0
tmax = 30.0
tmin = 20.0
rh_mean = 60.0
u2 = 2.0
rs = 20.0
elevation = 100.0

et = calculate_et(tmean, tmax, tmin, rh_mean, u2, rs, elevation)
print("Evapotranspiración (ET):", et, "mm/día")

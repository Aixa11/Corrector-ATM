from Py6S import *

s = SixS()
s.geometry = Geometry.User()
s.geometry.solar_z = 30  # Elevación solar en grados
s.geometry.solar_a = 0   # Azimut solar en grados
s.run()
print(s.outputs.atmos_corrected_reflectance)
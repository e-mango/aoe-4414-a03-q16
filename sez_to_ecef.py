# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Converts SEZ coordinate frame components into ECEF components
# Parameters:
#  o_lat_deg: Latitude in deg
#  o_lon_deg: Longitude in deg
#  o_hae_km: Height above the elipsoid in km
#  s_km: South component of SEZ in km
#  e_km: East component of SEZ in km
#  z_km: Zenith component of SEZ in km
#  ...
# Output:
#  Prints the x, y, and z coordinates in the ECEF reference frame
#
# Written by Evan Schlein
# Other contributors: None
#
# import Python modules
import math # math module
import sys  # argv

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456

# helper functions

## calculated denominator
def calc_denom(E_E, o_lat_rad):
  return math.sqrt(1.0-(E_E**2)*(math.sin(o_lat_rad)**2))

# initialize script arguments
o_lat_deg = float('nan') # Latitude in deg
o_lon_deg = float('nan') # Longitude in deg
o_hae_km = float('nan') # Height above the elipsoid in km
s_km = float('nan') # South component of SEZ in km
e_km = float('nan') # East component of SEZ in km
z_km = float('nan') # Zenith component of SEZ in km

# parse script arguments
if len(sys.argv)==7:
    o_lat_deg = float(sys.argv[1]) # Latitude in deg
    o_lon_deg = float(sys.argv[2]) # Longitude in deg
    o_hae_km = float(sys.argv[3]) # Height above the elipsoid in km
    s_km = float(sys.argv[4]) # South component of SEZ in km
    e_km = float(sys.argv[5]) # East component of SEZ in km
    z_km = float(sys.argv[6]) # Zenith component of SEZ in km
else:
  print(\
   'Usage: '\
   'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
  exit()

# write script below this line

# Convert lat lon deg into rad
o_lat_rad = o_lat_deg * math.pi/180.0
o_lon_rad = o_lon_deg * math.pi/180.0

# Calculate denom of fractions
denom = calc_denom(E_E,o_lat_rad)

# Calculate CE and SE
c_E = R_E_KM/denom
s_E = (R_E_KM*(1-E_E**2))/denom

# Calculate rx ry rz components
r_x_km = (c_E + o_hae_km)*math.cos(o_lat_rad)*math.cos(o_lon_rad)
r_y_km = (c_E + o_hae_km)*math.cos(o_lat_rad)*math.sin(o_lon_rad)
r_z_km = (s_E + o_hae_km)*math.sin(o_lat_rad)

# Convert SEZ components to ECEF compatable
conv_x_km = z_km*math.cos(o_lat_rad)*math.cos(o_lon_rad)+s_km*math.cos(o_lon_rad)*math.sin(o_lat_rad)-e_km*math.sin(o_lon_rad)
conv_y_km = e_km*math.cos(o_lon_rad)+z_km*math.cos(o_lat_rad)*math.sin(o_lon_rad)+s_km*math.sin(o_lat_rad)*math.sin(o_lon_rad)
conv_z_km = -s_km*math.cos(o_lat_rad)+z_km*math.sin(o_lat_rad)

# Calculate ECEF components
ecef_x_km = r_x_km + conv_x_km
ecef_y_km = r_y_km + conv_y_km
ecef_z_km = r_z_km + conv_z_km

# Print ECEF components in km
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)

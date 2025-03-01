import arcpy

#assign bands
source = r"H:\PythonGeog676\Harmann-online-GEOG676-spring2025-1\Lab_7"
band1 = arcpy.sa.Raster(source + r"\band1.tif")
band2 = arcpy.sa.Raster(source + r"\band2.tif")
band3 = arcpy.sa.Raster(source + r"\band3.tif")
band4 = arcpy.sa.Raster(source + r"\band4.tif")
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\output_combined.tif")

#Hillshade
azimuth = 315
altitude = 45
shadows = 'NO_SHADOWS'
z_factor = 1
arcpy.ddd.HillShade(source + r"\DEM.tif", source + r"\output_Hillshade.tif", azimuth, altitude, shadows, z_factor)

#Slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(source + r"\DEM.tif",source + r"\output_Slope.tif", output_measurement, z_factor)
print("success!")

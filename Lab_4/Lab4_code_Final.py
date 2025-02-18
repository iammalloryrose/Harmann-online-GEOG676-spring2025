import arcpy

# Set workspace
arcpy.env.workspace = r'H:\PythonGeog676\Harmann-online-GEOG676-spring2025\Lab_4'

# Define folder and geodatabase
folder_path = r'H:\PythonGeog676\Harmann-online-GEOG676-spring2025\Lab_4'
gdb_name = 'Test16.gdb'
gdb_path = folder_path + '\\' + gdb_name

# Create File GDB
arcpy.CreateFileGDB_management(folder_path, gdb_name)

# Define input CSV and create an event layer
csv_path = folder_path + '\\garages.csv'
garage_layer_name = 'Garage_Points'

garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)
input_layer = garages

# Convert to feature class inside GDB
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)

# Define feature class path inside GDB
garage_points = gdb_path + '\\' + garage_layer_name

# Open campus GDB and copy building features
campus = folder_path + '\\Campus.gdb'
buildings_campus = campus + '\\Structures'
buildings = gdb_path + '\\Buildings'

arcpy.Copy_management(buildings_campus, buildings)

# Get spatial reference from the copied buildings
spatial_ref = arcpy.Describe(buildings).spatialReference

# Project Re-Projection
garage_reprojected = gdb_path + '\\Garage_Points_reprojected'
arcpy.Project_management(garage_points, garage_reprojected, spatial_ref)

# Prompt user for buffer distance
buffer_distance = input("Enter the buffer distance in meters: ")

# Buffer the garages
garage_buffered = gdb_path + '\\Garage_Points_buffered'
arcpy.Buffer_analysis(garage_reprojected, garage_buffered, buffer_distance)

# Perform intersection with Buildings
intersection_output = gdb_path + '\\Garage_Building_Intersection'
arcpy.Intersect_analysis([garage_buffered, buildings], intersection_output, "ALL")

# Export intersection results to CSV
output_csv = folder_path + '\\nearbyBuildings2.csv'
arcpy.TableToTable_conversion(intersection_output, folder_path, "nearbyBuildings2.csv")

print("Intersection results exported to", output_csv)
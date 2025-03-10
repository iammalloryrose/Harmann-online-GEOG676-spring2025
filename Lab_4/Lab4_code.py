
#create a gdb and garage feature
import arcpy

arcpy.env.workspace = r'H:\Lab3Python\Harmann-online-GEOG676-spring2025\Lab_4'
folder_path = r'H:\Lab3Python\Harmann-online-GEOG676-spring2025\Lab_4'
gdb_name = 'Test14.gdb'
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r'H:\Lab3Python\Harmann-online-GEOG676-spring2025\Lab_4\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

#open campus gdb, copy building feature to our gdb
campus = r'H:\Lab3Python\Harmann-online-GEOG676-spring2025\Lab_4\Campus.gdb'
buildings_campus = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)

# Re-Projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, '\Garage_Points_reprojected', spatial_ref)

#Buffer the garages
garageBuffered = arcpy.Buffer_analysis(gdb_path, +'\Garage_Points_reprojected', gdb_path, '\Garage_Points_buffered', 150)

#Intersect our buffer with the buildings
arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path +'\Garage_Building_Intersection', 'ALL')

arcpy.TableToTable_conversion(gdb_path +'\Garage_Building_intersection.dbf', 'H:\Lab3Python\Harmann-online-GEOG676-spring2025\Lab_4', 'nearbyBuildings.csv')


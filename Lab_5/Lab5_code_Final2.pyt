import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GarageBuildingIntersection]

class GarageBuildingIntersection(object):
    def __init__(self):
        """Define tool name"""
        self.label = "Lab5 Toolbox"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GBD Name",
            name="GBDName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",  # Fixed typo: "GarageSCVFile" -> "GarageCSVFile"
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="CampusGDB",  # Fixed parameter name (no spaces allowed)
            datatype="DEWorkspace",  # Corrected from "DEType" to "DEWorkspace" for GDB
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )

        paracms = [param0, param1, param2, param3, param4, param5]
        return paracms

    def isLiensed(self):
        """Set whether tool is licensed to execute"""
        return True

    def updateParameters(self, parameters):
        """Modify parameter properties before validation"""
        return

    def updateMessages(self, parameters):
        """Modify validation messages"""
        return

    def execute(self, parameters, messages):
        """The source code of the tool"""
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        gdb_path = folder_path + '\\' + gdb_name

        # Create File Geodatabase
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        # Read CSV and create event layer
        csv_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

        # Export event layer to geodatabase
        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + '\\' + garage_layer_name

        # Open campus GDB and copy building feature
        campus = parameters[4].valueAsText
        buildings_campus = campus + '\\Structures'
        buildings = gdb_path + '\\Buildings'
        arcpy.Copy_management(buildings_campus, buildings)

        # Reprojection
        spatial_ref = arcpy.Describe(buildings).spatialReference
        reprojected_garages = gdb_path + '\\Garage_Points_reprojected'
        arcpy.Project_management(garage_points, reprojected_garages, spatial_ref)

        # Buffer garages
        buffer_distance = parameters[5].value
        garage_buffered = gdb_path + '\\Garage_Points_buffered'
        arcpy.Buffer_analysis(reprojected_garages, garage_buffered, buffer_distance)

        # Intersect buffer with buildings
        intersection_output = gdb_path + '\\Garage_Building_Intersection'
        arcpy.Intersect_analysis([garage_buffered, buildings], intersection_output, 'ALL')

        # Export result to table
        arcpy.TableToTable_conversion(intersection_output, r'H:\PythonGeog676\Harmann-online-GEOG676-spring2025\Lab_4', 'nearbyBuildings')

        return None
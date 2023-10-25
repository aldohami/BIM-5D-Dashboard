import ifcopenshell
from ifcopenshell import file
import pandas as pd
import sqlite3

def pull_data(data_file_path, ifc_file, export_path):
    index = 0

    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect(data_file_path)
    df = pd.read_sql_query("select * from Summary", con)


    df.head()
    Array2d_result = df.values
    cells_status = []
    cells_id = []
    color_factor = []

    # Label each building ID with a cost status according to the data in the database
    for i in range(len(Array2d_result)):
        cells_id.append(Array2d_result[i][3])
        if (Array2d_result[i][4] - Array2d_result[i][5]) < Array2d_result[i][4] * (-0.05):
            cells_status.append("OVER BUDGET")
            color_factor.append(float(Array2d_result[i][4]/Array2d_result[i][5]))
        elif ((Array2d_result[i][4] * (-0.05)) < (Array2d_result[i][4] - Array2d_result[i][5]) < (Array2d_result[i][4] * 0.05)):
            if (Array2d_result[i][4] - Array2d_result[i][5] > 0):
                color_factor.append(Array2d_result[i][5]/Array2d_result[i][4])
            else:
                color_factor.append(float(Array2d_result[i][4])/Array2d_result[i][5])
            cells_status.append("ON BUDGET")
        else:
            cells_status.append("UNDER BUDGET")
            color_factor.append(float(Array2d_result[i][5])/Array2d_result[i][4])

    #read ifc file and get all the building elements into an array
    ifcfile: file = ifcopenshell.open(ifc_file)
    products = ifcfile.by_type("IfcBuildingElement")
    owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
    building_elements =[]
    for i in products:
        building_elements.append(i)
    toDelete = ifcfile.by_type("IfcSurfaceStyleRendering")
    for a in toDelete:
        ifcfile.remove(a)

    #cross-reference the model and the excel values
    for i in building_elements:
        for j in cells_id:
            if j == i.GlobalId:
                property_values = [
                ifcfile.createIfcPropertySingleValue("Cost Status", "Cost Status", ifcfile.create_entity("IfcText",cells_status[index]), None),]

                #assign the properties according to the excel table
                property_set = ifcfile.createIfcPropertySet(i.GlobalId, owner_history, "Cost Status ", None, property_values)
                ifcfile.createIfcRelDefinesByProperties(i.GlobalId, owner_history, None, None, [i], property_set)
                index = index + 1
    #export
    ifcfile.write(export_path)
    return cells_status, cells_id, color_factor

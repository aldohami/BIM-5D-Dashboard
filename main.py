from assign_cost_status import *
from Visualize import *



ifc_file_path = 'DSSRDP(Schema4).ifc'
export_path = 'DSSRDP(Schema4)_cost.ifc'
export_path2 = 'DSSRDP(Schema4)_cost_color.ifc'
data_file_path = "CostManagement.db"

this_list = pull_data(data_file_path, ifc_file_path, export_path)
coloring(export_path, export_path2, this_list[0], this_list[1], this_list[2])



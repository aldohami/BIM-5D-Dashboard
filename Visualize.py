from ifcopenshell import file
import ifcopenshell.util.schema
import assign_cost_status
from assign_cost_status import pull_data

def coloring(export_path, export_path2, cells_status, cells_id, color_factor):
    shapes = []
    # Pull the exported IFC with cost parameters
    ifcfile: file = ifcopenshell.open(export_path)
    products = ifcfile.by_type("IfcBuildingElement")
    for p in products:
        try:
            shapes.append(p.Representation.Representations)
        except:
            shapes.append(0)
    # Color building elements according to their cost status
    for i in range(len(products)):
        for y in range(len(cells_id)):
            if products[i].GlobalId == cells_id[y]:
                if shapes[i] != 0:
                    if cells_status[y] == 'ON BUDGET':
                        IfcColourRgb_Blue = ifcfile.createIfcColourRgb('blue', 0.1, 0.1, color_factor[y])
                        IfcSurfaceStyleShading = ifcfile.createIfcSurfaceStyleShading(IfcColourRgb_Blue, .0)
                        IfcSurfaceStyle = ifcfile.createIfcSurfaceStyle(IfcColourRgb_Blue.Name, "BOTH", (IfcSurfaceStyleShading,))
                        Assign = ifcfile.createIfcPresentationStyleAssignment((IfcSurfaceStyle,))
                        for s in range(len(shapes[i])):
                            items = shapes[i][s].Items
                            for item in items:
                                IfcStyledItem = ifcfile.createIfcStyledItem(item, [Assign], 'Label_On-Budget')
                    elif cells_status[y] == 'OVER BUDGET':
                        IfcColourRgb_Red = ifcfile.createIfcColourRgb('red', color_factor[y], 0.1, 0.1)
                        IfcSurfaceStyleShading = ifcfile.createIfcSurfaceStyleShading(IfcColourRgb_Red, .0)
                        IfcSurfaceStyle = ifcfile.createIfcSurfaceStyle(IfcColourRgb_Red.Name, "BOTH", (IfcSurfaceStyleShading,))
                        Assign = ifcfile.createIfcPresentationStyleAssignment((IfcSurfaceStyle,))
                        items = shapes[i][0].Items
                        for s in range(len(shapes[i])):
                            items = shapes[i][s].Items
                            for item in items:
                                IfcStyledItem = ifcfile.createIfcStyledItem(item, [Assign], 'Label_Overrun')
                    else:
                        IfcColourRgb_Green = ifcfile.createIfcColourRgb('green', 0.1, color_factor[y], 0.1)
                        IfcSurfaceStyleShading = ifcfile.createIfcSurfaceStyleShading(IfcColourRgb_Green, .0)
                        IfcSurfaceStyle = ifcfile.createIfcSurfaceStyle(IfcColourRgb_Green.Name, "BOTH", (IfcSurfaceStyleShading,))
                        Assign = ifcfile.createIfcPresentationStyleAssignment((IfcSurfaceStyle,))
                        items = shapes[i][0].Items
                        for s in range(len(shapes[i])):
                            items = shapes[i][s].Items
                            for item in items:
                                IfcStyledItem = ifcfile.createIfcStyledItem(item, [Assign], 'Label_Under-Budget')
    ifcfile.write(export_path2)
    return()




import ifcopenshell

class qty():
    def __init__(self):
        pass      
        
    def netarea(element):
        definitions=element.IsDefinedBy
        for definition in definitions:
            if definition.is_a()=="IfcRelDefinesByProperties":
                property_definition=definition.RelatingPropertyDefinition
                if property_definition.is_a()=='IfcElementQuantity':
                    quantities=property_definition.Quantities
                    for quantity in quantities:
                        if element.is_a()=='IfcWall':
                            if quantity.is_a()=='IfcQuantityArea' and quantity.Name=='NetSideArea':
                                break
                        if element.is_a()=='IfcColumn':
                            if quantity.is_a()=='IfcQuantityArea' and quantity.Name=='OuterSurfaceArea':
                                break  
                    return quantity
                           
    
    def netvolume(element):
        definitions=element.IsDefinedBy
        for definition in definitions:
            if definition.is_a()=="IfcRelDefinesByProperties":
                property_definition=definition.RelatingPropertyDefinition
                if property_definition.is_a()=='IfcElementQuantity':
                    quantities=property_definition.Quantities
                    for quantity in quantities:
                        if quantity.is_a()=='IfcQuantityVolume' and quantity.Name=='NetVolume':
                            break
                    return quantity
   
    def perimeter(element):
        definitions=element.IsDefinedBy
        for definition in definitions:
            if definition.is_a()=="IfcRelDefinesByProperties":
                property_definition=definition.RelatingPropertyDefinition
                if property_definition.is_a()=='IfcElementQuantity':
                    quantities=property_definition.Quantities
                    for quantity in quantities:
                        if quantity.is_a()=='IfcQuantityLength' and quantity.Name=='Perimeter':
                            break
                    return quantity

    def width(element):
        definitions=element.IsDefinedBy
        for definition in definitions:
            if definition.is_a()=="IfcRelDefinesByProperties":
                property_definition=definition.RelatingPropertyDefinition
                if property_definition.is_a()=='IfcElementQuantity':
                    quantities=property_definition.Quantities
                    for quantity in quantities:
                        if quantity.is_a()=='IfcQuantityLength' and quantity.Name=='Width':
                            break
                    return quantity

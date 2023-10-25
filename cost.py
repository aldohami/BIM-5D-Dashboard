import ifcopenshell
import json
from pprint import pprint
from qty import *
import sqlite3

connector=sqlite3.connect('CostManagement.db')

curs=connector.cursor()

curs.execute(""" CREATE TABLE IF NOT EXISTS Summary (
	"ElementID"	INTEGER,
	"IfcRef"	TEXT,
    "Name"	TEXT,
	"GuID"  TEXT,
    "PlannedValue" DOUBLE,
    "ActualValue" DOUBLE,
    "Currency" TEXT,
	PRIMARY KEY("ElementID" AUTOINCREMENT)
)""")

curs.execute("DELETE FROM Summary ")

with open('costdata.json') as f:
    data=json.load(f)
    datas=data['IFCELEMENTS']
            
model=ifcopenshell.open("DSSRDP(Schema4).ifc")
MonetaryUnit=model.create_entity('IfcMonetaryUnit',Currency='EUR') 

def new_cost_val(valname,val):
        new_val=model.create_entity('IfcCostValue',AppliedValue=model.create_entity('IfcMeasureWithUnit',\
            ValueComponent=model.create_entity('IfcMonetaryMeasure',val),UnitComponent=MonetaryUnit))
        return new_val

for d in datas:
    ename=d['Name']
    elements=model.by_type(ename)
    tasks=d['Tasks']
    for element in elements:
        grandtotal=[]
        for task in tasks:
            t=model.create_entity('IfcTask',GlobalId=ifcopenshell.guid.new(),Name=task['Name'],Status='Not Complete')
            resources=task['Resources']
            #get quantity of element
            definitions=element.IsDefinedBy
            for definition in definitions:
                if definition.is_a()=="IfcRelDefinesByProperties":
                    property_definition=definition.RelatingPropertyDefinition
                    if property_definition.is_a()=='IfcElementQuantity':
                        quantities=property_definition.Quantities
                        for quantity in quantities:
                            if quantity.Name==task['QType']:
                                if task['QType']=="NetVolume":
                                    newQ=model.create_entity('IfcQuantityVolume',Name='Volume',VolumeValue=quantity.VolumeValue*task['Ratio'])
                                if task['QType']=="NetSideArea":
                                    newQ=model.create_entity('IfcQuantityArea',Name='Area',AreaValue=quantity.AreaValue*task['Ratio'])
                                if task['QType']=="OuterSurfaceArea":
                                    newQ=model.create_entity('IfcQuantityArea',Name='SurfaceArea',AreaValue=quantity.AreaValue*task['Ratio'])
                                break
                            elif task['QType']=="Weight":
                                newQ=model.create_entity("IfcQuantityWeight",Name='Weight',WeightValue=qty.netvolume(element).VolumeValue*task['Ratio'])
                            elif task['QType']=="Each":
                                newQ=model.create_entity("IfcQuantityCount",Name='Count',CountValue=1*task['Ratio'])    
            values=[]
            for resource in resources:
                unitcost=resource['Quantity']*resource['UnitPrice']/task['Productivity']
                monetarymeasure=model.create_entity('IfcMonetaryMeasure',unitcost)
                MeasureWithUnit=model.create_entity('IfcMeasureWithUnit',ValueComponent=monetarymeasure,UnitComponent=MonetaryUnit)
                val=model.create_entity('IfcCostValue',Name=resource['Name'],AppliedValue=MeasureWithUnit)
                values.append(val)
                resources=task['Resources']
            c=model.create_entity('IfcCostItem',GlobalId=ifcopenshell.guid.new(),Name=t.Name,CostValues=values,CostQuantities=[newQ])
            
            #link cost item to element
            model.create_entity('IfcRelAssignstoControl',GlobalId=ifcopenshell.guid.new(),RelatingControl=t,RelatedObjects=[c])
            model.create_entity('IfcRelAssignsToProduct', GlobalId=ifcopenshell.guid.new(),RelatingProduct=element,RelatedObjects=[t])
            gradntotal=[]
            totalval=[]
            for x in c.CostValues:                 
                totalval.append(x.AppliedValue.ValueComponent.wrappedValue) 
            
            if c.CostQuantities[0].is_a()=='IfcQuantityVolume':                               
                quan=c.CostQuantities[0].VolumeValue
                                
            if c.CostQuantities[0].is_a()=='IfcQuantityWeight':                            
                quan=c.CostQuantities[0].WeightValue
                                
            if c.CostQuantities[0].is_a()=='IfcQuantityArea':                        
                quan=c.CostQuantities[0].AreaValue 
                                
            if c.CostQuantities[0].is_a()=='IfcQuantityCount':                          
                quan=c.CostQuantities[0].CountValue
            
            totalcost=sum(totalval)*quan
            grandtotal.append(totalcost)

            print(f"Total cost of {task['Name']} for {element.Name} is {totalcost}")
        print(f"Total cost of {element.Name} with guid {element.GlobalId} is {sum(grandtotal)}")   
        row=[]
        row.clear
        row=[(element.is_a(),element.Name,element.GlobalId,sum(grandtotal),0,"EUR")]
        curs.executemany("INSERT INTO Summary (IfcRef,Name,GuID,PlannedValue,ActualValue,Currency) VALUES (?,?,?,?,?,?)", row)
        
curs.execute("SELECT SUM(PlannedValue) FROM Summary")
print(curs.fetchone())

connector.commit()
connector.close()  

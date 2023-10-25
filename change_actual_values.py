import sqlite3
import random

# Connect to the SQLite database
connector = sqlite3.connect('CostManagement.db')
curs = connector.cursor()

# Fetch all ElementIDs from the Summary table
curs.execute("SELECT ElementID FROM Summary")
element_ids = [row[0] for row in curs.fetchall()]

# Generate random ActualValues between 500 and 2000 for each ElementID
for element_id in element_ids:
    new_actual_value = random.uniform(500, 2000)
    
    # SQL statement to update the ActualValue
    update_query = "UPDATE Summary SET ActualValue = ? WHERE ElementID = ?"
    curs.execute(update_query, (new_actual_value, element_id))

# Commit the changes and close the connection
connector.commit()
connector.close()

import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

attributed_to_value = 'https://example.com/user1'
name_value = 'Event Name'
content_value = 'Event Content'
start_time_value = '2023-12-25 12:00:00'  
location_value = 'Event Location'
updated_value = '2023-12-26 09:00:00' 

cur.execute("""
    INSERT INTO events (attributedTo, name, content, startTime, location, published, updated)
    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
""", (attributed_to_value, name_value, content_value, start_time_value, location_value, updated_value))

# Commit the changes and close the connection
connection.commit()
connection.close()

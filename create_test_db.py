import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Create the departments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
);
''')

# Create the employees table with a foreign key
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    dept_id INTEGER,
    annual_salary REAL,
    FOREIGN KEY (dept_id) REFERENCES departments (dept_id)
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database 'test.db' created successfully with 'employees' and 'departments' tables.")
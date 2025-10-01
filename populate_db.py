from sqlalchemy import create_engine, text
import os

# --- Configuration ---
DB_FILE = "test.db"

# --- Sample Data ---
DEPARTMENTS_DATA = [
    (1, 'Engineering'),
    (2, 'Human Resources'),
    (3, 'Sales')
]

EMPLOYEES_DATA = [
    # Engineering Department
    (1, 'Alice Johnson', 1, 110000.00),
    (2, 'Bob Williams', 1, 130000.00),
    (3, 'Charlie Brown', 1, 95000.00),
    (4, 'Diana Prince', 1, 150000.00), # Highest paid in Engineering
    
    # Human Resources Department
    (5, 'Eve Adams', 2, 80000.00),
    (6, 'Frank Miller', 2, 85000.00),

    # Sales Department
    (7, 'Grace Lee', 3, 120000.00),
    (8, 'Henry Wilson', 3, 125000.00),
    (9, 'Ivy Green', 3, 115000.00),
    (10, 'Jack King', 3, 140000.00) # Second highest paid overall
]

def populate_database():
    """
    Connects to the SQLite database and inserts sample data.
    """
    if not os.path.exists(DB_FILE):
        print(f"Error: Database file '{DB_FILE}' not found. Please run create_test_db.py first.")
        return

    engine = create_engine(f"sqlite:///{DB_FILE}")
    
    try:
        with engine.connect() as connection:
            print("Inserting department data...")
            # Clear existing data to prevent duplicates
            connection.execute(text("DELETE FROM departments;"))
            for dept in DEPARTMENTS_DATA:
                connection.execute(text("INSERT INTO departments (dept_id, dept_name) VALUES (:id, :name)"), 
                                   {"id": dept[0], "name": dept[1]})
            
            print("Inserting employee data...")
            # Clear existing data
            connection.execute(text("DELETE FROM employees;"))
            for emp in EMPLOYEES_DATA:
                connection.execute(
                    text("""
                        INSERT INTO employees (emp_id, full_name, dept_id, annual_salary) 
                        VALUES (:id, :name, :dept, :salary)
                    """),
                    {"id": emp[0], "name": emp[1], "dept": emp[2], "salary": emp[3]}
                )
            
            # Commit the changes
            connection.commit()
            print("\nDatabase populated successfully with 3 departments and 10 employees.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    populate_database()
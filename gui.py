import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import mysql.connector
from mysql.connector import Error
from dateutil.relativedelta import relativedelta


def create_tenant(): # This creates a new tenant by asking the user to input all required information as dictated by the original table creation query
    try:
        first_name = simpledialog.askstring("Input", "Enter first name:", parent=app)
        last_name = simpledialog.askstring("Input", "Enter last name:", parent=app)
        email = simpledialog.askstring("Input", "Enter email:", parent=app)
        phone_number = simpledialog.askstring("Input", "Enter phone number:", parent=app)
        initial_lease_date = simpledialog.askstring("Input", "Enter initial lease date (YYYY-MM-DD):", parent=app)

        if first_name and last_name and email and phone_number and initial_lease_date: # Checks if all values are present
            query = "INSERT INTO Tenant (first_name, last_name, email, phone_number, initial_lease_date) VALUES (%s, %s, %s, %s, %s)" # Using %s values throughout to prevent injection attacks
            cursor.execute(query, (first_name, last_name, email, phone_number, initial_lease_date))
            connection.commit()
            messagebox.showinfo("Success", "Tenant added successfully")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def update_tenant(): # Updates tenant information
    try:
        tenant_id = simpledialog.askstring("Input", "Enter tenant ID to update:", parent=app)
        new_first_name = simpledialog.askstring("Input", "Enter new first name:", parent=app)
        new_last_name = simpledialog.askstring("Input", "Enter new last name:", parent=app)
        new_email = simpledialog.askstring("Input", "Enter new email:", parent=app)
        new_phone_number = simpledialog.askstring("Input", "Enter new phone number:", parent=app)
        new_initial_lease_date = simpledialog.askstring("Input", "Enter new initial lease date (YYYY-MM-DD):", parent=app)

        if tenant_id and (new_first_name or new_last_name or new_email or new_phone_number or new_initial_lease_date): # Checks that there is at least one item that was inputted to be updated
            query = "UPDATE Tenant SET "
            params = [] # Holds params we are updating based on what was inputted
            if new_first_name:
                query += "first_name = %s, "
                params.append(new_first_name)
            if new_last_name:
                query += "last_name = %s, "
                params.append(new_last_name)
            if new_email:
                query += "email = %s, "
                params.append(new_email)
            if new_phone_number:
                query += "phone_number = %s, "
                params.append(new_phone_number)
            if new_initial_lease_date:
                query += "initial_lease_date = %s, "
                params.append(new_initial_lease_date)

            query += " WHERE id = %s"
            params.append(tenant_id)

            cursor.execute(query, tuple(params))
            connection.commit()
            messagebox.showinfo("Success", "Tenant information updated successfully")
        else:
            messagebox.showwarning("Input Error", "Tenant ID is required and at least one field to update.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def delete_tenant(): # Deletes tenant record based on tenant ID
    try:
        tenant_id = simpledialog.askstring("Input", "Enter tenant ID to delete:", parent=app)

        if tenant_id:
            tenant_id = int(tenant_id) 

            query = "DELETE FROM Tenant WHERE id = %s"
            cursor.execute(query, (tenant_id,))
            connection.commit()

            if cursor.rowcount > 0: # Checks to see if any records were removed
                messagebox.showinfo("Success", f"Tenant with ID {tenant_id} deleted successfully")
            else:
                messagebox.showwarning("Not Found", f"No tenant found with ID {tenant_id}")
        else:
            messagebox.showwarning("Input Error", "Tenant ID is required.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def create_unit(): # Creates new unit record
    try:
        rent_amount = simpledialog.askstring("Input", "Enter rent amount:", parent=app)
        payment_due_date = simpledialog.askstring("Input", "Enter payment due date (YYYY-MM-DD):", parent=app)
        remaining_balance = simpledialog.askstring("Input", "Enter remaining balance:", parent=app)
        current_tenant = simpledialog.askstring("Input", "Enter current tenant ID (leave blank if none):", parent=app)

        if rent_amount and payment_due_date and remaining_balance: # Confirms necessary items and converts to appropriate types 
            rent_amount = float(rent_amount)
            remaining_balance = float(remaining_balance)
            current_tenant = int(current_tenant) if current_tenant else None # Converts tenant unless no tenant is currently renting said unit

            query = "INSERT INTO Unit (rent_amount, payment_due_date, remaining_balance, current_tenant) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (rent_amount, payment_due_date, remaining_balance, current_tenant))
            connection.commit()
            messagebox.showinfo("Success", "Unit added successfully")
        else:
            messagebox.showwarning("Input Error", "Rent amount, payment due date, and remaining balance are required.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def update_unit(): # Updates unit data
    try:
        unit_number = simpledialog.askinteger("Input", "Enter unit number to update:", parent=app)
        new_rent_amount = simpledialog.askstring("Input", "Enter new rent amount (leave blank if no change):", parent=app)
        new_payment_due_date = simpledialog.askstring("Input", "Enter new payment due date (YYYY-MM-DD, leave blank if no change):", parent=app)
        new_remaining_balance = simpledialog.askstring("Input", "Enter new remaining balance (leave blank if no change):", parent=app)
        new_current_tenant = simpledialog.askstring("Input", "Enter new current tenant ID (leave blank if no change):", parent=app)

        query_parts = [] 
        params = []

        if new_rent_amount:
            query_parts.append("rent_amount = %s")
            params.append(float(new_rent_amount))
        if new_payment_due_date:
            query_parts.append("payment_due_date = %s")
            params.append(new_payment_due_date)
        if new_remaining_balance:
            query_parts.append("remaining_balance = %s")
            params.append(float(new_remaining_balance))
        if new_current_tenant:
            query_parts.append("current_tenant = %s")
            params.append(int(new_current_tenant))

        if query_parts:
            query = "UPDATE Unit SET " + ", ".join(query_parts) + " WHERE unit_number = %s"
            params.append(unit_number)
            cursor.execute(query, tuple(params))
            connection.commit()
            messagebox.showinfo("Success", f"Unit {unit_number} updated successfully")
        else:
            messagebox.showwarning("Input Error", "No updates provided.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def delete_unit(): # Deletes unit record
    try:
        unit_number = simpledialog.askinteger("Input", "Enter unit number to delete:", parent=app)

        if unit_number:
            query = "DELETE FROM Unit WHERE unit_number = %s"
            cursor.execute(query, (unit_number,))
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Unit {unit_number} deleted successfully")
            else:
                messagebox.showwarning("Not Found", f"No unit found with number {unit_number}")
        else:
            messagebox.showwarning("Input Error", "Unit number is required.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def create_payment(): # Creates new payment 
    try:
        payment_date = simpledialog.askstring("Input", "Enter payment date (YYYY-MM-DD):", parent=app)
        payment_amount = simpledialog.askstring("Input", "Enter payment amount:", parent=app)
        unit_number = simpledialog.askinteger("Input", "Enter unit number:", parent=app)

        if payment_date and payment_amount and unit_number:
            query = "INSERT INTO payment_log (payment_date, payment_amount, unit_number) VALUES (%s, %s, %s)"
            cursor.execute(query, (payment_date, float(payment_amount), unit_number))
            connection.commit()
            messagebox.showinfo("Success", "Payment added successfully")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def update_payment(): # Updates payment record
    try:
        payment_id = simpledialog.askinteger("Input", "Enter payment ID to update:", parent=app)
        new_payment_date = simpledialog.askstring("Input", "Enter new payment date (YYYY-MM-DD, leave blank if no change):", parent=app)
        new_payment_amount = simpledialog.askstring("Input", "Enter new payment amount (leave blank if no change):", parent=app)
        new_unit_number = simpledialog.askinteger("Input", "Enter new unit number (leave blank if no change):", parent=app)

        query_parts = []
        params = []

        if new_payment_date:
            query_parts.append("payment_date = %s")
            params.append(new_payment_date)
        if new_payment_amount:
            query_parts.append("payment_amount = %s")
            params.append(float(new_payment_amount))
        if new_unit_number is not None:
            query_parts.append("unit_number = %s")
            params.append(new_unit_number)

        if query_parts:
            query = "UPDATE payment_log SET " + ", ".join(query_parts) + " WHERE id = %s"
            params.append(payment_id)
            cursor.execute(query, tuple(params))
            connection.commit()
            messagebox.showinfo("Success", f"Payment {payment_id} updated successfully")
        else:
            messagebox.showwarning("Input Error", "No updates provided.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def delete_payment(): # Deletes payment records
    try:
        payment_id = simpledialog.askinteger("Input", "Enter payment ID to delete:", parent=app)

        if payment_id:
            query = "DELETE FROM payment_log WHERE id = %s"
            cursor.execute(query, (payment_id,))
            connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Payment {payment_id} deleted successfully")
            else:
                messagebox.showwarning("Not Found", f"No payment found with ID {payment_id}")
        else:
            messagebox.showwarning("Input Error", "Payment ID is required.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def show_late_payers(): # Shows anybody who paid their bill past the first of the month
    try: # This query joins together the unit and tenant tables as well as the payment and unit tables in order to pull information regarding payment info, tenant info, and payment dates/due dates
        query = """
        SELECT t.first_name, t.last_name, t.email, u.unit_number, p.payment_date, u.payment_due_date FROM Tenant t
        JOIN Unit u ON t.id = u.current_tenant
        JOIN payment_log p ON u.unit_number = p.unit_number
        WHERE p.payment_date > u.payment_due_date 
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if results: # Checks if there were any matches and then returns
            result_str = "\n".join([f"Tenant: {row[0]} {row[1]}, Email: {row[2]}, Unit: {row[3]}, Paid On: {row[4]}, Due Date: {row[5]}" for row in results]) # Concatonates a new line with the late payers info
            messagebox.showinfo("Late Payers", result_str)
        else:
            messagebox.showinfo("Late Payers", "No late payments found.")
    except Error as e:
        messagebox.showerror("Error", str(e))

def show_tenants_with_high_balance(): # Shows tenants whose current balance exceeds their monthly rent
    try: # Joins unit and tenant tables in order to get balances and rent info
        query = """
        SELECT t.first_name, t.last_name, t.email, u.unit_number, u.rent_amount, u.remaining_balance
        FROM Tenant t
        JOIN Unit u ON t.id = u.current_tenant
        WHERE u.remaining_balance > u.rent_amount
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            result_str = "\n".join([f"Tenant: {row[0]} {row[1]}, Email: {row[2]}, Unit: {row[3]}, Rent: {row[4]}, Balance: {row[5]}" for row in results]) 
            messagebox.showinfo("Tenants With High Balance", result_str)
        else:
            messagebox.showinfo("Tenants With High Balance", "No tenants found with balance higher than rent.")
    except Error as e:
        messagebox.showerror("Error", str(e))

def update_balances(): # This function processes payments by updating the current balances of tenants based on the payment log
    try: # Joins payment and unit tables to update values according to tenants payment history. 
         # Realistically most people pay rent in one payment, but some may pay in multiple smaller payments if behind on payments already, 
         # hence why I used the sum of all payments for each unit number.
        query = """
        SELECT u.unit_number, u.remaining_balance, SUM(p.payment_amount) as total_payments
        FROM Unit u
        LEFT JOIN payment_log p ON u.unit_number = p.unit_number
        GROUP BY u.unit_number
        """
        cursor.execute(query)
        results = cursor.fetchall()

        for unit in results:
            unit_number, current_balance, total_payments = unit # This unpacks the unit tuple into 3 seperate variables
            total_payments = total_payments if total_payments is not None else 0
            new_balance = current_balance - total_payments

            update_query = "UPDATE Unit SET remaining_balance = %s WHERE unit_number = %s"
            cursor.execute(update_query, (new_balance, unit_number))

        connection.commit()
        messagebox.showinfo("Success", "All balances updated successfully.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def update_rent_and_due_dates(): # This updates the due date of payments to the following month and adds the corrosponding rent payment to each unit balance
    try:
        select_query = "SELECT unit_number, remaining_balance, rent_amount, payment_due_date FROM Unit"
        cursor.execute(select_query)
        units = cursor.fetchall()

        for unit in units:
            unit_number, current_balance, rent_amount, current_due_date = unit
            if current_due_date:
                next_due_date = (current_due_date + relativedelta(months=1)).replace(day=1) # This adds a month to the due date and sets it to the first day of that month
                new_balance = current_balance + rent_amount
                update_query = "UPDATE Unit SET remaining_balance = %s, payment_due_date = %s WHERE unit_number = %s"
                cursor.execute(update_query, (new_balance, next_due_date, unit_number))

        connection.commit()
        messagebox.showinfo("Success", "Balances and payment due dates updated successfully.")
    except Error as e:
        messagebox.showerror("Error", str(e))
        connection.rollback()

def show_all_tenants(): # Shows a list of all tenants and their info
    try:
        query = "SELECT * FROM Tenant"
        cursor.execute(query)
        tenants = cursor.fetchall()

        if tenants:
            result_str = "\n".join([f"ID: {tenant[0]}, Name: {tenant[1]} {tenant[2]}, Email: {tenant[3]}, Phone: {tenant[4]}, Lease Date: {tenant[5]}" for tenant in tenants])
            messagebox.showinfo("All Tenants", result_str)
        else:
            messagebox.showinfo("All Tenants", "No tenants found.")
    except Error as e:
        messagebox.showerror("Error", str(e))


def search_for_tenant(): # Allows for searching of tenants by partial or full name
    try:
        search_query = simpledialog.askstring("Search Tenant", "Enter tenant's full or partial name to search:", parent=app)

        if search_query:
            query = "SELECT * FROM Tenant WHERE CONCAT(first_name, ' ', last_name) LIKE %s"
            search_pattern = f"%{search_query}%" # The % are wildcards used to search for similar entries to the user input
            cursor.execute(query, (search_pattern,))
            results = cursor.fetchall()

            if results:
                result_str = "\n".join([f"ID: {t[0]}, Name: {t[1]} {t[2]}, Email: {t[3]}, Phone: {t[4]}, Lease Date: {t[5]}" for t in results])
                messagebox.showinfo("Search Results", result_str)
            else:
                messagebox.showinfo("Search Results", "No tenants found matching the search criteria.")
        else:
            messagebox.showwarning("Search Tenant", "Please enter a name to search.")
    except Error as e:
        messagebox.showerror("Error", str(e))

def search_for_unit(): # Searches for unit info based on Unit number
    try:
        unit_number = simpledialog.askinteger("Search Unit", "Enter unit number to search:", parent=app)

        if unit_number is not None:
            query = "SELECT * FROM Unit WHERE unit_number = %s"
            cursor.execute(query, (unit_number,))
            result = cursor.fetchone()

            if result:
                result_str = f"Unit Number: {result[0]}, Rent Amount: {result[1]}, Payment Due Date: {result[2]}, Remaining Balance: {result[3]}, Current Tenant ID: {result[4]}"
                messagebox.showinfo("Search Results", result_str)
            else:
                messagebox.showinfo("Search Results", "No unit found with the specified number.")
        else:
            messagebox.showwarning("Search Unit", "Please enter a valid unit number to search.")
    except Error as e:
        messagebox.showerror("Error", str(e))

def search_payments_by_tenant(): # Searches for all payments by tenant name
    try:
        tenant_name = simpledialog.askstring("Search Payments by Tenant", "Enter tenant name to search for payments:", parent=app)

        if tenant_name:
            query = """
            SELECT * FROM payment_log p
            JOIN Unit u ON p.unit_number = u.unit_number
            JOIN Tenant t ON u.current_tenant = t.id
            WHERE t.first_name LIKE %s OR t.last_name LIKE %s
            """
            search_pattern = f"%{tenant_name}%"
            cursor.execute(query, (search_pattern, search_pattern))
            results = cursor.fetchall()

            if results:
                result_str = "\n".join([f"Payment ID: {r[0]}, Date: {r[1]}, Amount: {r[2]}, Unit Number: {r[3]}" for r in results])
                messagebox.showinfo("Payments by Tenant", result_str)
            else:
                messagebox.showinfo("Payments by Tenant", "No payments found for the specified tenant.")
        else:
            messagebox.showwarning("Search Error", "Please enter a tenant's name to search.")
    except Error as e:
        messagebox.showerror("Error", str(e))

# Database Connection
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='windycreekapartments'
    )
    cursor = connection.cursor()
except Error as e:
    messagebox.showerror("Database Connection Error", str(e))
    exit(1)

# GUI Setup
app = tk.Tk()
app.title("Windy Creek Apartments Management System")
app.geometry("700x400")
style = ttk.Style()


# Basic formatting for GUI
general_frame = ttk.LabelFrame(app, text="General Operations", padding=2)
general_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

other_frame = ttk.LabelFrame(app, text="Other Operations", padding=10)
other_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Buttons for General Operations
ttk.Button(general_frame, text="Add Tenant", command=create_tenant, style="TButton").grid(row=0, column=0, padx=5, pady=5)
ttk.Button(general_frame, text="Update Tenant", command=update_tenant).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(general_frame, text="Delete Tenant", command=delete_tenant).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(general_frame, text="Seach Tenants By Name", command=search_for_tenant).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(general_frame, text="Add Unit", command=create_unit).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(general_frame, text="Update Unit", command=update_unit).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(general_frame, text="Delete Unit", command=delete_unit).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(general_frame, text="Seach Units by Number", command=search_for_unit).grid(row=1, column=3, padx=5, pady=5)
ttk.Button(general_frame, text="Add Payment", command=create_payment).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(general_frame, text="Update Payment", command=update_payment).grid(row=2, column=1, padx=5, pady=5)
ttk.Button(general_frame, text="Delete Payment", command=delete_payment).grid(row=2, column=2, padx=5, pady=5)
ttk.Button(general_frame, text="Search for Payment by Name", command=search_payments_by_tenant).grid(row=2, column=3, padx=5, pady=5)

# Other operation buttons
ttk.Button(other_frame, text="Show All Tenants", command=show_all_tenants).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(other_frame, text="Show Tenants With High Balance", command=show_tenants_with_high_balance).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(other_frame, text="Show Late Payers", command=show_late_payers).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(other_frame, text="Process Payments", command=update_balances).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(other_frame, text="Update Rent and Due Dates", command=update_rent_and_due_dates).grid(row=2, column=1, padx=5, pady=5)
ttk.Button(other_frame, text="Seach Tenants By Name", command=search_for_tenant).grid(row=2, column=2, padx=5, pady=5)

# Start the GUI
app.mainloop()

# Close database connection after closing app
if connection.is_connected():
    cursor.close()
    connection.close()

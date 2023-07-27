from tkinter import *
from tkinter import messagebox as msg
from PIL import ImageTk
import cx_Oracle
import tkinter.ttk as ttk

cust_win = Tk()

# Function to execute SQL query to modify cart
def modify():
    # Create a new window to get input from user
    modify_win = Toplevel(cust_win)
    modify_win.title('Modify Cart')

    # Create labels and entry widgets for user input
    pid_label = Label(modify_win, text='Product ID:')
    pid_label.grid(row=0, column=0, padx=5, pady=5)
    pid_entry = Entry(modify_win)
    pid_entry.grid(row=0, column=1, padx=5, pady=5)

    # Function to execute SQL query to delete cart item
    def delete_item():
        try:
            local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
            connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
            cursor = connector.cursor()
            query = f"""
                delete from cart_item where (product_id='{pid_entry.get()}' and Cart_id in (
                    select cart_id from customer where customer_id='cid100'
                ))
            """
            cursor.execute(query)
            connector.commit()
            cursor.close()
            connector.close()
            msg.showinfo('Success', 'Cart item deleted successfully.')

        except Exception as e:
            msg.showerror('Error', f'Error deleting cart item: {e}')

        modify_win.destroy()

    # Create a button to delete the cart item
    delete_btn = Button(modify_win, text='Delete', command=delete_item)
    delete_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def filter_products():
    # Get the filter values from the user
    p_size = p_size_entry.get()
    gender = gender_entry.get()
    p_type = p_type_entry.get()

    try:
        local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
        connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
        cursor = connector.cursor()

        # Construct the query with the filter values
        query = f"""
            select product_id, color, cost, seller_id from product where (type='{p_type}' and p_size='{p_size}' and gender='{gender}' and quantity>0)
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connector.close()

        # Create a new window to show the filtered results in a table
        filtered_win = Toplevel(cust_win)
        filtered_win.title('Filtered Products')

        # Create a treeview widget to display the filtered results in a table
        treeview = ttk.Treeview(filtered_win)
        treeview.pack(side='left', fill='both', expand=True)

        # Define columns for the table
        treeview['columns'] = ('Product ID', 'Color', 'Cost', 'Seller ID')

        # Format the columns
        treeview.column('#0', width=0, stretch=NO)
        treeview.column('Product ID', width=100)
        treeview.column('Color', width=100)
        treeview.column('Cost', width=100)
        treeview.column('Seller ID', width=100)

        # Add column headings
        treeview.heading('#0', text='', anchor=CENTER)
        treeview.heading('Product ID', text='Product ID')
        treeview.heading('Color', text='Color')
        treeview.heading('Cost', text='Cost')
        treeview.heading('Seller ID', text='Seller ID')

        # Insert the rows of data into the table
        for row in rows:
            treeview.insert('', 'end', text='', values=row)

    except Exception as e:
        print(e)
    filtered_win.mainloop()
# Function to execute SQL query and display order history
def history():
    try:
        local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
        connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
        cursor = connector.cursor()
        query = """
            select product_id,Quantity_wished from Cart_item where (purchased='Y' and Cart_id in (select Cart_id from customer where Customer_id='cid100'))
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connector.close()

        # Create a new window to show the order history in a table
        history_win = Toplevel(cust_win)
        history_win.title('Order History')

        # Create a treeview widget to display the order history in a table
        treeview = ttk.Treeview(history_win)
        treeview.pack(side='left', fill='both', expand=True)

        # Define columns for the table
        treeview['columns'] = ('Product ID', 'Quantity Wished')

        # Format the columns
        treeview.column('#0', width=0, stretch=NO)
        treeview.column('Product ID', anchor=CENTER, width=100)
        treeview.column('Quantity Wished', anchor=CENTER, width=150)

        # Add column headings
        treeview.heading('#0', text='', anchor=CENTER)
        treeview.heading('Product ID', text='Product ID', anchor=CENTER)
        treeview.heading('Quantity Wished', text='Quantity Wished', anchor=CENTER)

        # Insert the rows of data into the table
        for row in rows:
            treeview.insert('', 'end', text='', values=row)

    except Exception as e:
        print(e)

# Function to execute SQL query and display results in a new window
def show_cart():
    try:
        local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
        connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
        cursor=connector.cursor()
        query = """
            select * from product where product_id in(
                select product_id from Cart_item where (Cart_id in (
                    select Cart_id from Customer where Customer_id='cid100'
                ))
            and purchased='Y')
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connector.close()

        # Create a new window to show the results in a table
        cart_win = Toplevel(cust_win)
        cart_win.title('Cart Items')

        # Create a treeview widget to display the results in a table
        treeview = ttk.Treeview(cart_win)
        treeview.pack(side='left', fill='both', expand=True)

        # Define columns for the table
        treeview['columns'] = ('Product ID', 'Product Name', 'Description', 'Price')

        # Format the columns
        treeview.column('#0', width=0, stretch=NO)
        treeview.column('Product ID', width=100)
        treeview.column('Product Name', width=100)
        treeview.column('Description', width=100)
        treeview.column('Price', width=100)

        # Add column headings
        treeview.heading('#0', text='', anchor=CENTER)
        treeview.heading('Product ID', text='Product ID')
        treeview.heading('Product Name', text='Product Name')
        treeview.heading('Description', text='Description')
        treeview.heading('Price', text='Price')

        # Insert the rows of data into the table
        for row in rows:
            treeview.insert('', 'end', text='', values=row)

    except Exception as e:
        print(e)

# Create "show cart" button

show_cart_btn = Button(cust_win, text='Show Cart', command=show_cart)
show_cart_btn.pack()
history_btn = Button(cust_win, text='History', command=history)
history_btn.pack()
filter_btn = Button(cust_win, text='Filter', command=filter_products)
filter_btn.pack()
Label(cust_win, text="Product Size: ").pack()
p_size_entry = Entry(cust_win, width=20)
p_size_entry.pack()
Label(cust_win, text="Gender: ").pack()
gender_entry = Entry(cust_win, width=20)
gender_entry.pack()
Label(cust_win, text="Product Type: ").pack()
p_type_entry = Entry(cust_win, width=20)
p_type_entry.pack()
modify_btn = Button(cust_win, text='Modify', command=modify)
modify_btn.pack()
cust_win.mainloop()
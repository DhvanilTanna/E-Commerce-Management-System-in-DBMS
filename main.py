from tkinter import *
from tkinter import messagebox as msg
from PIL import ImageTk
import cx_Oracle
import tkinter.ttk as ttk

main=Tk()

def login_window():
    # Function to open the login window based on user selection

    # Get the selected option
    selection = option.get()

    # Create a new window for login

    login_win = Toplevel()
    login_win.geometry('338x200+300+25')
    login_win.resizable(False,False)
    login_win.title("Login")
    # Add radio buttons to select login option
    back_ground_image=ImageTk.PhotoImage(file='111112.jpg') #variable for background image
    back_ground_label=Label(login_win,image=back_ground_image)
    back_ground_label.place(x=0,y=0)

    # Add labels and entry fields for login details
    if selection == 1:
        Label(login_win, text="Customer ID: ",font=('Microsoft Yahei UI Light',20,'bold')).grid(row=0, column=0)
        cust_id_entry = Entry(login_win)
        cust_id_entry.grid(row=0, column=1)
    else:
        Label(login_win, text="Seller ID: ",font=('Microsoft Yahei UI Light',20,'bold')).grid(row=0, column=0)
        seller_id_entry = Entry(login_win)
        seller_id_entry.grid(row=0, column=1)

    Label(login_win, text="Password: ",font=('Microsoft Yahei UI Light',20,'bold')).grid(row=1, column=0)
    password_entry = Entry(login_win, show="*")
    password_entry.grid(row=1, column=1)

    # Add a login button
    def check_login():
        # Get the entered login details
        if selection == 1:
            cust_id = cust_id_entry.get()

            # Connect to the database
            local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
            connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
            cursor=connector.cursor()

            # Execute the query and check the result
            cursor.execute("SELECT * FROM customer WHERE customer_id=:1 AND c_pass=:2",(cust_id,password_entry.get()))
            result = cursor.fetchone()
            if result:
                msg.showinfo("Login Successful", "You have successfully logged in!")
                # main.destroy()
                # import cart_item
                # import cust_win
                customer(cust_id)
                # Add your code to do something after successful login
            else:
                msg.showerror("Login Failed", "Invalid credentials, please try again.")
            # Close the database connection
            connector.commit()
            cursor.close()
            connector.close()
        else:
            seller_id = seller_id_entry.get()
            # Connect to the database
            local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
            connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
            cursor=connector.cursor()
    
            # Execute the query and check the result
            cursor.execute("SELECT * FROM seller WHERE seller_id=:1 AND s_pass=:2",(seller_id,password_entry.get()))
            result = cursor.fetchone()
            if result:
                msg.showinfo("Login Successful", "You have successfully logged in!")
                # main.destroy()
                # import product
                # import sell_win
                seller(seller_id)
                # Add your code to do something after successful login
            else:
                msg.showerror("Login Failed", "Invalid credentials, please try again.")
            # Close the database connection
            connector.commit()
            cursor.close()
            connector.close()

    Button(login_win, text="Login", command=check_login).grid(row=2, column=1)

def signup_window():
    # Function to open the login window based on user selection

    # Get the selected option
    selection = option.get()

    if selection==1:
        main.destroy()
        import customer_signup
    else:
        main.destroy()
        import seller_signup

main.geometry('500x338+300+25')
main.resizable(False,False)
# Add radio buttons to select login option
back_ground_image=ImageTk.PhotoImage(file="C:\\Users\\Anil\\OneDrive\\Pictures\\Screenshots\\111112.png") #variable for background image
back_ground_label=Label(main,image=back_ground_image)
back_ground_label.place(x=0,y=0)
option = IntVar()
customer_radio = Radiobutton(main, text="Customer",font=('Microsoft Yahei UI Light',20,'bold'), variable=option, value=1)
seller_radio = Radiobutton(main, text="Seller",font=('Microsoft Yahei UI Light',20,'bold'), variable=option, value=2)
customer_radio.place(x=100,y=40)
seller_radio.place(x=100,y=110)

# Add a login button to open the login window
login_button = Button(main, text="Login",font=('Microsoft Yahei UI Light',20,'bold'), command=login_window)
login_button.place(x=100,y=180)
signup_button = Button(main, text="signup",font=('Microsoft Yahei UI Light',20,'bold'), command=signup_window)
signup_button.place(x=100,y=250)

class seller:
    def __init__(self,seller_id):
        self.sell_win=Tk()
        self.seller_id=seller_id
        sell_win=self.sell_win

        def product():
            import product
        def sold_on_date():
            try:
                local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
                connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
                cursor = connector.cursor()
                date=date_entry.get()
                # Execute the query
                cursor.execute("SELECT COUNT(product_id), date_added FROM Cart_item WHERE purchased='Y' AND date_added = :1 GROUP BY(date_added)", [date])
                results = cursor.fetchall()
        
                # Create the table
                table = ttk.Treeview(sell_win, columns=('count', 'date_added'))
                table.heading('count', text='Count')
                table.heading('date_added', text='Date Added')
        
                # Insert the query results into the table
                for row in results:
                    table.insert('', 'end', values=row)
        
                table.pack()
        
                connector.commit()
                cursor.close()
                connector.close()

            except Exception as e:
                print(e)
                msg.showerror("Error", "Failed to retrieve sold product count on date.")

        # Function to execute SQL queries for removing a seller and updating product quantity
        def remove():
            try:
                local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
                connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
                cursor = connector.cursor()

                # Delete the seller with the specified ID
                cursor.execute("delete from seller where seller_id =:1",(self.seller_id,))

                # Update the quantity of products with no seller
                cursor.execute("update product set quantity = 0 where seller_id is NULL")

                connector.commit()
                cursor.close()
                connector.close()

                # Show success message
                msg.showinfo("Success", "Seller removed and product quantity updated.")

            except Exception as e:
                print(e)
                msg.showerror("Error", "Failed to remove seller.")

        # Create "remove" button
        remove_btn = Button(sell_win, text='Remove', command=remove)
        remove_btn.pack()
        date_label = Label(sell_win, text='Date:')
        date_label.pack()
        date_entry = Entry(sell_win)
        date_entry.pack()
        sold_btn=Button(sell_win, text='Sold on Date', command=sold_on_date)
        sold_btn.pack()
        product_btn=Button(sell_win, text='Product', command=product)
        product_btn.pack()

        sell_win.mainloop()

class customer:
    def __init__(self,cust_id):

        self.cust_win = Tk()
        
        cust_win=self.cust_win

        def add_to_cart():
            import cart_item
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
                    cursor.execute("""
                        delete from cart_item where (product_id=:1 and Cart_id in (
                            select cart_id from customer where customer_id=:2
                        ))
                    """,(pid_entry.get(),self.cust_id))
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
                query = """
                    select product_id, color, cost, seller_id from product where (type=:1 and p_size=:2 and gender=:3 and quantity>0)
                """
                cursor.execute(query,(p_type,p_size,gender))
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
                    select product_id,Quantity_wished from Cart_item where (purchased='Y' and Cart_id in (select Cart_id from customer where Customer_id=:1))
                """
                cursor.execute(query,(self.cust_id,))
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
                cursor.execute("""
                    select * from product where product_id in(
                        select product_id from Cart_item where (Cart_id in (
                            select Cart_id from Customer where Customer_id=:1
                        ))
                    and purchased='Y')
                """,(self.cust_id,))
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
                treeview['columns'] = ('Product ID', 'Product Name', 'Description', 'Size')

                # Format the columns
                treeview.column('#0', width=0, stretch=NO)
                treeview.column('Product ID', width=100)
                treeview.column('Product Name', width=100)
                treeview.column('Description', width=100)
                treeview.column('Size', width=100)

                # Add column headings
                treeview.heading('#0', text='', anchor=CENTER)
                treeview.heading('Product ID', text='Product ID')
                treeview.heading('Product Name', text='Product Name')
                treeview.heading('Description', text='Description')
                treeview.heading('Size', text='Size')

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
        addtocart_btn = Button(cust_win, text='Add to cart', command=add_to_cart)
        addtocart_btn.pack()
        self.cust_id=cust_id
        cust_win.mainloop()
main.mainloop()
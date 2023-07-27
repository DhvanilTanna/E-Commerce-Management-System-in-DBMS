from tkinter import *
from tkinter import messagebox as msg
import cx_Oracle

# Define function to insert cart items into the database
def add_to_cart():
    # Get the values entered in the entry fields
    cart_id = cart_id_entry.get()
    product_id = product_id_entry.get()
    quantity_wished = quantity_wished_entry.get()
    date_added = date_added_entry.get()
    purchased = purchased_entry.get()
    
    # Connect to the database
    local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
    connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
    cursor=connector.cursor()
    
    # Insert the cart item into the cart_item table
    cursor.execute("INSERT INTO cart_item (cart_id, product_id, quantity_wished, date_added, purchased) VALUES (:1, :2, :3, :4, :5)", 
                   (cart_id, product_id, quantity_wished, date_added, purchased))
    connector.commit()
    cursor.close()
    connector.close()
    # Display a message box indicating that the item was added to the cart
    msg.showinfo("Success", "Item added to cart!")
    
# Create the window and entry fields
cart_item_window = Tk()

cart_item_window.title("Cart Item")
cart_item_window.geometry("250x200")

cart_id_label = Label(cart_item_window, text="Cart ID:")
cart_id_label.grid(row=0, column=0)
cart_id_entry = Entry(cart_item_window)
cart_id_entry.grid(row=0, column=1)

product_id_label = Label(cart_item_window, text="Product ID:")
product_id_label.grid(row=1, column=0)
product_id_entry = Entry(cart_item_window)
product_id_entry.grid(row=1, column=1)

quantity_wished_label = Label(cart_item_window, text="Quantity Wished:")
quantity_wished_label.grid(row=2, column=0)
quantity_wished_entry = Entry(cart_item_window)
quantity_wished_entry.grid(row=2, column=1)

date_added_label = Label(cart_item_window, text="Date Added:")
date_added_label.grid(row=3, column=0)
date_added_entry = Entry(cart_item_window)
date_added_entry.grid(row=3, column=1)

purchased_label = Label(cart_item_window, text="Purchased:")
purchased_label.grid(row=4, column=0)
purchased_entry = Entry(cart_item_window)
purchased_entry.grid(row=4, column=1)

# Create the button to add the cart item to the database
add_to_cart_button = Button(cart_item_window, text="Add to Cart", command=add_to_cart)
add_to_cart_button.grid(row=5, column=0, columnspan=2)

cart_item_window.mainloop()
from tkinter import *
from tkinter import messagebox as msg
import cx_Oracle

# create the main window
product_window = Tk()
product_window.title("Add Product")
product_window.geometry("300x300")

# create the form labels and entry fields
product_id_lbl = Label(product_window, text="Product ID:")
product_id_lbl.grid(row=0,column=0)
product_id_entry = Entry(product_window)
product_id_entry.grid(row=0,column=1)

type_lbl = Label(product_window, text="Type:")
type_lbl.grid(row=1,column=0)
type_entry = Entry(product_window)
type_entry.grid(row=1,column=1)

color_lbl = Label(product_window, text="Color:")
color_lbl.grid(row=2,column=0)
color_entry = Entry(product_window)
color_entry.grid(row=2,column=1)

age_group_lbl = Label(product_window, text="Age Group:")
age_group_lbl.grid(row=3,column=0)
age_group_entry = Entry(product_window)
age_group_entry.grid(row=3,column=1)

size_lbl = Label(product_window, text="Size:")
size_lbl.grid(row=4,column=0)
size_entry = Entry(product_window)
size_entry.grid(row=4,column=1)

gender_lbl = Label(product_window, text="Gender:")
gender_lbl.grid(row=5,column=0)
gender_entry = Entry(product_window)
gender_entry.grid(row=5,column=1)

commission_lbl = Label(product_window, text="Commission:")
commission_lbl.grid(row=6,column=0)
commission_entry = Entry(product_window)
commission_entry.grid(row=6,column=1)

cost_lbl = Label(product_window, text="Cost:")
cost_lbl.grid(row=7,column=0)
cost_entry = Entry(product_window)
cost_entry.grid(row=7,column=1)

quantity_lbl = Label(product_window, text="Quantity:")
quantity_lbl.grid(row=8,column=0)
quantity_entry = Entry(product_window)
quantity_entry.grid(row=8,column=1)

seller_id_lbl = Label(product_window, text="Seller ID:")
seller_id_lbl.grid(row=9,column=0)
seller_id_entry = Entry(product_window)
seller_id_entry.grid(row=9,column=1)

# create the submit button
def add_product():
    # retrieve the values from the entry fields
    product_id = product_id_entry.get()
    type = type_entry.get()
    color = color_entry.get()
    age_group = age_group_entry.get()
    size = size_entry.get()
    gender = gender_entry.get()
    commission = commission_entry.get()
    cost = cost_entry.get()
    quantity = quantity_entry.get()
    seller_id = seller_id_entry.get()
    
    # insert the values into the product table in the database
    local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
    connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
    cursor=connector.cursor()
    cursor.execute("INSERT INTO product VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)",(product_id, type, color, size, gender, commission, cost, quantity, seller_id))
    connector.commit()
    cursor.close()
    connector.close()
    
    # show a message box to indicate success
    msg.showinfo("Success", "Product added successfully.")
    
submit_btn = Button(product_window, text="Add Product", command=add_product)
submit_btn.grid(row=10,column=1)

# start the main event loop
product_window.mainloop()
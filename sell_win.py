from tkinter import *
from tkinter import messagebox as msg
from PIL import ImageTk
import cx_Oracle
import tkinter.ttk as ttk

sell_win = Tk()

# Function to execute SQL queries for removing a seller and updating product quantity
def remove():
    try:
        local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
        connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
        cursor = connector.cursor()
        
        # Delete the seller with the specified ID
        cursor.execute("delete from seller where seller_id = 'sid100'")
        
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

sell_win.mainloop()
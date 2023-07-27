from tkinter import *
from tkinter import messagebox as msg
from PIL import ImageTk
import cx_Oracle
from email.message import EmailMessage as emsg

def signup_action():
    # Write the action to be performed when the Signup button is clicked
    # This can include retrieving the values entered in the Entry widgets and performing database operations, email sending, etc.
    # For example, you can retrieve the values entered in the Entry widgets using the get() method of the Entry widget:
    seller_id = seller_id_entry.get()
    seller_password = seller_pass_entry.get()
    seller_con_password=seller_con_pass_entry.get()
    seller_name = seller_name_entry.get()
    seller_address = seller_address_entry.get()
    
    if not seller_id or not seller_password or not seller_name or not seller_address:
        msg.showerror("Error", "Please fill all the fields")
    elif seller_password != seller_con_password:
        msg.showerror("Error","Password does not match.")
    else:
        local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
        connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
        cursor=connector.cursor()

        query='select seller_id from seller where seller_id=:1' #:1 etle niche tuple ma pelu aaya email aavse
        cursor.execute(query,(seller_id,))
        recieve=cursor.fetchall() #aanu try catch karvanu se

        if len(recieve)!=0:
            msg.showerror("WARNING","Seller id is already used once\nTry with other Seller id")
        else:
            cursor.execute('insert into seller(seller_id,s_pass,name,address) values(:1,:2,:3,:4)',(seller_id,seller_password,seller_name,seller_address))
            
            msg.showinfo("Congratulation",'You are Succefully Registered')
            connector.commit()
            cursor.close()
            connector.close()

# Create the main window
seller_window = Tk()

seller_window.title("Seller")
seller_window.geometry('300x200+300+25')
seller_window.resizable(False,False)
# Add radio buttons to select login option
back_ground_image=ImageTk.PhotoImage(file="C:\\Users\\Anil\\OneDrive\\Pictures\\Screenshots\\111112.png") #variable for background image
back_ground_label=Label(seller_window,image=back_ground_image)
back_ground_label.place(x=0,y=0)

# Create the Labels and Entry widgets for seller ID
seller_id_label = Label(seller_window, text="Seller ID:")
seller_id_entry = Entry(seller_window)

# Create the Labels and Entry widgets for seller password
seller_pass_label = Label(seller_window, text="Seller Password:")
seller_pass_entry = Entry(seller_window, show="*")

seller_con_pass_label = Label(seller_window, text="Seller Confirm Password:")
seller_con_pass_entry = Entry(seller_window, show="*")

# Create the Labels and Entry widgets for seller name
seller_name_label = Label(seller_window, text="Seller Name:")
seller_name_entry = Entry(seller_window)

# Create the Labels and Entry widgets for seller address
seller_address_label = Label(seller_window, text="Seller Address:")
seller_address_entry = Entry(seller_window)

# Create the Signup button
signup_button = Button(seller_window, text="Signup", command=signup_action)

# Add the widgets to the window using the grid layout manager
seller_id_label.grid(row=0, column=0)
seller_id_entry.grid(row=0, column=1)

seller_pass_label.grid(row=1, column=0)
seller_pass_entry.grid(row=1, column=1)

seller_con_pass_label.grid(row=2, column=0)
seller_con_pass_entry.grid(row=2, column=1)

seller_name_label.grid(row=3, column=0)
seller_name_entry.grid(row=3, column=1)

seller_address_label.grid(row=4, column=0)
seller_address_entry.grid(row=4, column=1)

signup_button.grid(row=5, column=1)

# Start the main event loop
seller_window.mainloop()


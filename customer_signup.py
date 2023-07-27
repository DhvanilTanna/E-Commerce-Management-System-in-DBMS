from tkinter import *
from tkinter import messagebox as msg
from PIL import ImageTk
import cx_Oracle
from email.message import EmailMessage as emsg

signup_window = Tk()

signup_window.title("Sign Up")
signup_window.geometry('300x200+300+25')
signup_window.resizable(False,False)
# Add radio buttons to select login option
back_ground_image=ImageTk.PhotoImage(file="C:\\Users\\Anil\\OneDrive\\Pictures\\Screenshots\\111112.png") #variable for background image
back_ground_label=Label(signup_window,image=back_ground_image)
back_ground_label.place(x=0,y=0)

# signup_window.geometry("400x300")

customer_id_entry = Entry(signup_window)
c_pass_entry = Entry(signup_window, show="*")
c_con_pass_entry = Entry(signup_window, show="*")
name_entry = Entry(signup_window)
address_entry = Entry(signup_window)
phoneno_entry = Entry(signup_window)
pincode_entry = Entry(signup_window)
cart_id_entry = Entry(signup_window)

Label(signup_window, text="Customer ID: ").grid(row=0)
customer_id_entry.grid(row=0, column=1)
Label(signup_window, text="Password: ").grid(row=1)
c_pass_entry.grid(row=1, column=1)
Label(signup_window, text="Confirm Password: ").grid(row=2)
c_con_pass_entry.grid(row=2, column=1)
Label(signup_window, text="Name: ").grid(row=3)
name_entry.grid(row=3, column=1)
Label(signup_window, text="Address: ").grid(row=4)
address_entry.grid(row=4, column=1)
Label(signup_window, text="Phone Number: ").grid(row=5)
phoneno_entry.grid(row=5, column=1)
Label(signup_window, text="Pin Code: ").grid(row=6)
pincode_entry.grid(row=6, column=1)
Label(signup_window, text="Cart ID: ").grid(row=7)
cart_id_entry.grid(row=7, column=1)

signup_button = Button(signup_window, text="Signup")

signup_button.grid(row=8, column=1)

def signup():
    # Get the values from the entry fields
    customer_id = customer_id_entry.get()
    name = name_entry.get()
    address = address_entry.get()
    phoneno = phoneno_entry.get()
    pincode = pincode_entry.get()
    password = c_pass_entry.get()
    con_password = c_con_pass_entry.get()
    cart_id = cart_id_entry.get()
    
    # Validate the inputs
    if not customer_id or not name or not address or not phoneno or not pincode or not password or not cart_id or not con_password:
        msg.showerror("Error", "Please fill all the fields")
    elif password != con_password:
        msg.showerror("Error","Password does not match.")
    else:
        local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
        connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
        cursor=connector.cursor()

        query='select customer_id from customer where customer_id=:1' #:1 etle niche tuple ma pelu aaya email aavse
        cursor.execute(query,(customer_id,))
        recieve=cursor.fetchall() #aanu try catch karvanu se

        query='select cart_id from customer where cart_id=:1' #:1 etle niche tuple ma pelu aaya email aavse
        cursor.execute(query,(cart_id,))
        recieve1=cursor.fetchall() #aanu try catch karvanu se
        if len(recieve)!=0:
            msg.showerror("WARNING","Customer id is already used once\nTry with other customer id")
        elif len(recieve1)!=0:
            msg.showerror("WARNING","Cart id is already used once\nTry with other cart id")
        else:
            cursor.execute('insert into customer(CUSTOMER_ID,C_PASS, NAME,ADDRESS, PINCODE, PHONE_NUMBER_S, CART_ID) values(:1,:2,:3,:4,:5,:6,:7)',(customer_id,password,name,address,pincode,phoneno,cart_id))
            
            msg.showinfo("Congratulation",'You are Succefully Registered')
            connector.commit()
            cursor.close()
            connector.close()

signup_button.config(command=signup)

signup_window.mainloop()

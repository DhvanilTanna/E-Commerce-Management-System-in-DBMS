from tkinter import *
from tkinter import messagebox as msg
import cx_Oracle

payment_window = Tk()

def calculate():
    local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
    connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
    mycursor=connector.cursor()

    mycursor.execute("select sum(quantity_wished * cost) total_payable from product p join cart_item c on p.product_id=c.product_id where c.product_id in (select product_id from cart_item where cart_id in(select Cart_id from customer where customer_id=:1) and purchased='Y')",(customer_id_entry.get(),))
    result = mycursor.fetchone()[0]

    mycursor.execute("update payment set total_amount =:1 where customer_id =:2",(result,customer_id_entry.get()))

    Label(payment_window,text="Amount:").grid(row=9, column=0)
    Label(payment_window,text=str(result)).grid(row=9, column=1)

    connector.commit()
    mycursor.close()
    connector.close()

def fetch_bill():
    # payment_window.destroy()
    # import fetch
    
    fetch_window = Toplevel(payment_window)

    def fetch():
        local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
        connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
        mycursor=connector.cursor()

        paymentdata=payment_id_entry.get()
        mycursor.execute("SELECT * FROM Payment where Payment_Id=:1",(paymentdata,))
        payment=mycursor.fetchone()
        
        if not payment:
            msg.showerror("Error", "Payment not found.")
            return

        mycursor.execute("SELECT Product_id, Quantity_wished FROM Cart_item WHERE Cart_id=:1", (payment[4],))
        cart_items = mycursor.fetchall()

        # Create a new window to display the bill details
        bill_window = Toplevel(fetch_window)
        bill_window.title("Bill Details")

        # Add labels to display payment details
        Label(bill_window, text="Payment ID: " + str(payment[0])).grid(row=0, column=0)
        Label(bill_window, text="Payment Date: " + str(payment[1])).grid(row=1, column=0)
        Label(bill_window, text="Payment Type: " + str(payment[2])).grid(row=2, column=0)
        Label(bill_window, text="Customer ID: " + str(payment[3])).grid(row=3, column=0)
        Label(bill_window, text="Cart ID: " + str(payment[4])).grid(row=4, column=0)
        Label(bill_window, text="Total Amount: " + str(payment[5])).grid(row=5, column=0)
        Label(bill_window, text="").grid(row=6, column=0)

        # Add labels to display cart items
        Label(bill_window, text="Products in Cart:").grid(row=7, column=0)
        Label(bill_window, text="").grid(row=8, column=0)
        for item in cart_items:
            mycursor.execute("SELECT * FROM Product WHERE Product_id=:1", (item[0],))
            product = mycursor.fetchone()
            Label(bill_window, text="Product ID: " + str(product[0])).grid()
            Label(bill_window, text="Type: " + str(product[1])).grid()
            Label(bill_window, text="Color: " + str(product[2])).grid()
            Label(bill_window, text="Size: " + str(product[3])).grid()
            Label(bill_window, text="Gender: " + str(product[4])).grid()
            Label(bill_window, text="Cost: " + str(product[6])).grid()
            Label(bill_window, text="Quantity: " + str(item[1])).grid()
            Label(bill_window, text="Commission: " + str(product[5])).grid()
            Label(bill_window, text="").grid()

        connector.commit()
        mycursor.close()
        connector.close()



    fetch_window.title("Fetch Bill")

    payment_id_label = Label(fetch_window, text="Payment ID:")
    payment_id_label.grid(row=0, column=0)
    payment_id_entry = Entry(fetch_window)
    payment_id_entry.grid(row=0, column=1)

    # Create the button to process the payment
    fetch_button = Button(fetch_window, text="Fetch", command=fetch)
    fetch_button.grid(row=1,column=1)

    fetch_window.mainloop()

# Define function to insert payment details into the database
def add_payment():
    # Get the values entered in the entry fields
    payment_id = payment_id_entry.get()
    payment_date = payment_date_entry.get()
    payment_type = payment_type_entry.get()
    total_amount = total_amount_entry.get()
    customer_id = customer_id_entry.get()
    cart_id = cart_id_entry.get()
    
    # Connect to the database
    local_host = cx_Oracle.makedsn('jd', '1521', 'XE') 
    connector = cx_Oracle.connect('SYSTEM', 'admin', local_host)
    cursor=connector.cursor()
    
    # Insert the payment details into the payment table
    cursor.execute("INSERT INTO payment (payment_id, payment_date, payment_type, total_amount, customer_id, cart_id) VALUES (:1, :2, :3, :4, :5, :6)", (payment_id, payment_date, payment_type, total_amount, customer_id, cart_id))
    connector.commit()
    cursor.close()
    connector.close()
    
    # Display a message box indicating that the payment was processed
    msg.showinfo("Success", "Payment processed!")
    
# Create the window and entry fields

payment_window.title("Payment")
payment_window.geometry("250x200")

payment_id_label = Label(payment_window, text="Payment ID:")
payment_id_label.grid(row=0, column=0)
payment_id_entry = Entry(payment_window)
payment_id_entry.grid(row=0, column=1)

payment_date_label = Label(payment_window, text="Payment Date:")
payment_date_label.grid(row=1, column=0)
payment_date_entry = Entry(payment_window)
payment_date_entry.grid(row=1, column=1)

payment_type_label = Label(payment_window, text="Payment Type:")
payment_type_label.grid(row=2, column=0)
payment_type_entry = Entry(payment_window)
payment_type_entry.grid(row=2, column=1)

total_amount_label = Label(payment_window, text="Total Amount:")
total_amount_label.grid(row=3, column=0)
total_amount_entry = Entry(payment_window)
total_amount_entry.grid(row=3, column=1)

customer_id_label = Label(payment_window, text="Customer ID:")
customer_id_label.grid(row=4, column=0)
customer_id_entry = Entry(payment_window)
customer_id_entry.grid(row=4, column=1)

cart_id_label = Label(payment_window, text="Cart ID:")
cart_id_label.grid(row=5, column=0)
cart_id_entry = Entry(payment_window)
cart_id_entry.grid(row=5, column=1)

# Create the button to process the payment
proceed_button = Button(payment_window, text="Proceed", command=add_payment)
proceed_button.grid(row=6, column=0, columnspan=2)

fetch_button=Button(payment_window,text="Fetch Bill",command=fetch_bill)
fetch_button.grid(row=7,column=0,columnspan=2)

cal_btn=Button(payment_window,text="Calculate",command=calculate)
cal_btn.grid(row=8,column=0,columnspan=2)

payment_window.mainloop()
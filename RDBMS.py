from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_no INTEGER PRIMARY KEY AUTOINCREMENT,
        fries REAL,
        meals REAL,
        burger REAL,
        pizza REAL,
        cheese_burger REAL,
        drinks REAL,
        cost REAL,
        service_charge REAL,
        tax REAL,
        total REAL
    )
    ''')
    conn.commit()
    conn.close()

setup_database()

root = Tk()
root.geometry("900x700+100+50")
root.resizable(0, 0)
root.title("Restaurant Management System")

background_image = Image.open("/image.jpg")
background_image = background_image.resize((900, 700), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Load and resize the button image
btn_image = background_image.resize((150, 50), Image.LANCZOS)  # Adjust size as needed
btn_photo = ImageTk.PhotoImage(btn_image)

# Create Canvas and set background image
canvas = Canvas(root, width=900, height=700)
canvas.pack(fill=BOTH, expand=YES)
canvas.create_image(0, 0, anchor=NW, image=background_photo)

# Create a frame to hold other widgets on top of the canvas
frame = Frame(canvas, bg='white', bd=5)
frame.place(relwidth=1, relheight=1)

# Create a Canvas inside the frame to set background image for the frame
frame_canvas = Canvas(frame, width=900, height=700)
frame_canvas.place(relwidth=1, relheight=1)
frame_canvas.create_image(0, 0, anchor=NW, image=background_photo)

# Create header and content frames
header_frame = ttk.Frame(frame, width=900, height=100, relief=SUNKEN)
header_frame.pack(side=TOP, fill=X)

content_frame = ttk.Frame(frame, width=900, height=600, relief=SUNKEN)
content_frame.pack(expand=True, padx=20, pady=20)

localtime = time.asctime(time.localtime(time.time()))

lblinfo = ttk.Label(header_frame, text="Restaurant Management System", font=('aria', 30, 'bold'), foreground="cyan", background="#003366", padding=15)
lblinfo.pack(side=TOP, fill=X)

lbltime = ttk.Label(header_frame, text=localtime, font=('aria', 18), foreground="light blue", background="#003366", padding=10)
lbltime.pack(side=TOP, fill=X)

x = 1

def calculate_totals():
    try:
        cof = float(Fries.get() or 0)
        colfries = float(Meals.get() or 0)
        cob = float(Burger.get() or 0)
        cofi = float(Pizza.get() or 0)
        cochee = float(Cheese_burger.get() or 0)
        codr = float(Drinks.get() or 0)

        costoffries = cof * 25
        costofmeals = colfries * 40
        costofburger = cob * 35
        costofpizza = cofi * 30
        costofcheeseburger = cochee * 50
        costofdrinks = codr * 35

        costofmeal = costoffries + costofmeals + costofburger + costofpizza + costofcheeseburger + costofdrinks
        PayTax = costofmeal * 0.10
        Ser_Charge = costofmeal / 99
        Service = "Rs. " + str('%.2f' % Ser_Charge)
        OverAllCost = "Rs. " + str('%.2f' % (PayTax + costofmeal + Ser_Charge))
        PaidTax = "Rs. " + str('%.2f' % PayTax)

        Service_Charge.set(Service)
        cost.set("Rs. " + str('%.2f' % costofmeal))
        Tax.set(PaidTax)
        Subtotal.set("Rs. " + str('%.2f' % costofmeal))
        Total.set(OverAllCost)

        return cof, colfries, cob, cofi, cochee, codr, costofmeal, Ser_Charge, PayTax

    except ValueError:
        # Handle the error if conversion fails
        return None

def save_order():
    global x
    result = calculate_totals()
    if result is None:
        return  # Skip saving if there's an error

    cof, colfries, cob, cofi, cochee, codr, costofmeal, Ser_Charge, PayTax = result

    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        # Insert data without specifying order_no (it will be auto-generated)
        cursor.execute('''
        INSERT INTO orders (fries, meals, burger, pizza, cheese_burger, drinks, cost, service_charge, tax, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cof, colfries, cob, cofi, cochee, codr, costofmeal, Ser_Charge, PayTax, PayTax + costofmeal + Ser_Charge))

        conn.commit()
        conn.close()

        x += 1

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def show_orders():
    order_window = Toplevel(root)
    order_window.geometry("600x400")
    order_window.title("Order Data")

    Label(order_window, text="Order Data", font=('aria', 18, 'bold')).pack()

    text_widget = Text(order_window, wrap='word')
    text_widget.pack(expand=1, fill='both')

    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()

        for order in orders:
            text_widget.insert(END, f"Order No: {order[0]}\n"
                                    f"Fries: {order[1]}\n"
                                    f"Meals: {order[2]}\n"
                                    f"Burger: {order[3]}\n"
                                    f"Pizza: {order[4]}\n"
                                    f"Cheese Burger: {order[5]}\n"
                                    f"Drinks: {order[6]}\n"
                                    f"Cost: {order[7]}\n"
                                    f"Service Charge: {order[8]}\n"
                                    f"Tax: {order[9]}\n"
                                    f"Total: {order[10]}\n\n")

        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def display_database():
    db_window = Toplevel(root)
    db_window.geometry("800x400")
    db_window.title("Order Database")

    # Create Treeview widget
    tree = ttk.Treeview(db_window, columns=("Order No", "Fries", "Meals", "Burger", "Pizza", "Cheese Burger", "Drinks", "Cost", "Service Charge", "Tax", "Total"), show='headings')

    # Define the column headings and their properties
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    tree.pack(expand=True, fill='both')

    # Add the scrollbar
    scrollbar = ttk.Scrollbar(db_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        # Clear the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Fetch all orders from the database
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()

        # Insert fetched data into the Treeview
        for order in orders:
            tree.insert("", "end", values=order)

        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def create_rounded_button(master, text, command, **kwargs):
    btn = ttk.Button(master, text=text, command=command, **kwargs)
    btn.configure(style="TButton")
    return btn

def quit_app():
    root.destroy()

def reset_fields():
    j.set("")
    Fries.set("")
    Meals.set("")
    Burger.set("")
    Pizza.set("")
    Cheese_burger.set("")
    Drinks.set("")
    cost.set("")
    Service_Charge.set("")
    Tax.set("")
    Subtotal.set("")
    Total.set("")

def create_rounded_entry(master, textvariable, **kwargs):
    entry = ttk.Entry(master, textvariable=textvariable, **kwargs)
    entry.configure(style="TEntry")
    return entry

def display_price_list():
    roo = Tk()
    roo.geometry("400x220+0+0")
    roo.title("Price List")
    Label(roo, font=('aria', 16, 'bold'), text="ITEM", fg="Pale Turquoise1", bd=5).grid(row=0, column=0)
    Label(roo, font=('aria', 16, 'bold'), text="______________", fg="black", anchor=W).grid(row=0, column=2)
    Label(roo, font=('aria', 16, 'bold'), text="PRICE", fg="Pale Turquoise1", anchor=W).grid(row=0, column=3)
    items = [("Fries", 25), ("Meals", 40), ("Burger", 35), ("Pizza", 30), ("Cheese Burger", 50), ("Drinks", 35)]
    for i, (item, price) in enumerate(items, start=1):
        Label(roo, font=('aria', 14, 'bold'), text=item, fg="lavender").grid(row=i, column=0, sticky=W)
        Label(roo, font=('aria', 14, 'bold'), text="__________", fg="black", anchor=W).grid(row=i, column=2)
        Label(roo, font=('aria', 14, 'bold'), text=f"Rs.{price}", fg="misty rose").grid(row=i, column=3)
    roo.mainloop()

def create_image_button(master, image, command, bg_color='white', active_bg_color='lightgray', **kwargs):
    return Button(master, image=image, command=command, borderwidth=1, bg=bg_color, activebackground=active_bg_color, **kwargs)

# Variables
j = StringVar()
Fries = StringVar()
Meals = StringVar()
Burger = StringVar()
Pizza = StringVar()
Subtotal = StringVar()
Total = StringVar()
Service_Charge = StringVar()
Drinks = StringVar()
Tax = StringVar()
cost = StringVar()
Cheese_burger = StringVar()

# Widgets
lblreference = ttk.Label(content_frame, text="Order No.", foreground="white", padding=15)
lblreference.grid(row=0, column=0, sticky=W)
txtreference = create_rounded_entry(content_frame, textvariable=j)
txtreference.grid(row=0, column=1, padx=15, pady=10)

lblfries = ttk.Label(content_frame, text="Fries", foreground="white", padding=15)
lblfries.grid(row=1, column=0, sticky=W)
txtfries = create_rounded_entry(content_frame, textvariable=Fries)
txtfries.grid(row=1, column=1, padx=15, pady=10)

lblLargefries = ttk.Label(content_frame, text="Meals", foreground="white", padding=15)
lblLargefries.grid(row=2, column=0, sticky=W)
txtLargefries = create_rounded_entry(content_frame, textvariable=Meals)
txtLargefries.grid(row=2, column=1, padx=15, pady=10)

lblburger = ttk.Label(content_frame, text="Burger", foreground="white", padding=15)
lblburger.grid(row=3, column=0, sticky=W)
txtburger = create_rounded_entry(content_frame, textvariable=Burger)
txtburger.grid(row=3, column=1, padx=15, pady=10)

lblPizza = ttk.Label(content_frame, text="Pizza", foreground="white", padding=15)
lblPizza.grid(row=4, column=0, sticky=W)
txtPizza = create_rounded_entry(content_frame, textvariable=Pizza)
txtPizza.grid(row=4, column=1, padx=15, pady=10)

lblCheese_burger = ttk.Label(content_frame, text="Cheese burger", foreground="white", padding=15)
lblCheese_burger.grid(row=5, column=0, sticky=W)
txtCheese_burger = create_rounded_entry(content_frame, textvariable=Cheese_burger)
txtCheese_burger.grid(row=5, column=1, padx=15, pady=10)

lblDrinks = ttk.Label(content_frame, text="Drinks", foreground="white", padding=15)
lblDrinks.grid(row=0, column=2, sticky=W)
txtDrinks = create_rounded_entry(content_frame, textvariable=Drinks)
txtDrinks.grid(row=0, column=3, padx=15, pady=10)

lblcost = ttk.Label(content_frame, text="Cost", foreground="white", padding=15)
lblcost.grid(row=1, column=2, sticky=W)
txtcost = create_rounded_entry(content_frame, textvariable=cost)
txtcost.grid(row=1, column=3, padx=15, pady=10)

lblService_Charge = ttk.Label(content_frame, text="Service Charge", foreground="white", padding=15)
lblService_Charge.grid(row=2, column=2, sticky=W)
txtService_Charge = create_rounded_entry(content_frame, textvariable=Service_Charge)
txtService_Charge.grid(row=2, column=3, padx=15, pady=10)

lblTax = ttk.Label(content_frame, text="Tax", foreground="white", padding=15)
lblTax.grid(row=3, column=2, sticky=W)
txtTax = create_rounded_entry(content_frame, textvariable=Tax)
txtTax.grid(row=3, column=3, padx=15, pady=10)

lblSubtotal = ttk.Label(content_frame, text="Subtotal", foreground="white", padding=15)
lblSubtotal.grid(row=4, column=2, sticky=W)
txtSubtotal = create_rounded_entry(content_frame, textvariable=Subtotal)
txtSubtotal.grid(row=4, column=3, padx=15, pady=10)

lblTotal = ttk.Label(content_frame, text="Total", foreground="white", padding=15)
lblTotal.grid(row=5, column=2, sticky=W)
txtTotal = create_rounded_entry(content_frame, textvariable=Total)
txtTotal.grid(row=5, column=3, padx=15, pady=10)

btnTotal = create_rounded_button(content_frame, text="TOTAL", command=save_order)
btnTotal.grid(row=6, column=0, padx=15, pady=15)

btnreset = create_rounded_button(content_frame, text="RESET", command=reset_fields)
btnreset.grid(row=6, column=1, padx=15, pady=15)

btnexit = create_rounded_button(content_frame, text="EXIT", command=quit_app)
btnexit.grid(row=6, column=2, padx=15, pady=15)

btnShowOrders = create_rounded_button(content_frame, text="SHOW ORDERS", command=show_orders)
btnShowOrders.grid(row=7, column=0, columnspan=4, padx=15, pady=15, sticky=W+E)

btnprice = create_rounded_button(content_frame, text="PRICE", command=display_price_list)
btnprice.grid(row=6, column=3, padx=15, pady=15)

btnDisplayDB = create_rounded_button(content_frame, text="DISPLAY DATABASE", command=display_database)
btnDisplayDB.grid(row=8, column=0, columnspan=4, padx=15, pady=15, sticky=W+E)

root.mainloop()

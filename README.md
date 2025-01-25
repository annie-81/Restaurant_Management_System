# Restaurant Database Management System

## Overview

The Restaurant Database Management System is a comprehensive solution to manage restaurant orders efficiently. It allows users to input orders, calculate totals, save order details to a SQLite database, and retrieve order history. The application is developed using Python and utilizes the Tkinter library for the graphical user interface (GUI).

##Features

- Order Management:

Input various menu items like fries, meals, burgers, pizza, cheese burgers, and drinks.

Automatically calculate totals, including service charges and taxes.

- Database Integration:

Save order details to a SQLite database.

Retrieve and display all orders.

- User Interface:

Intuitive GUI with separate sections for data entry, order processing, and visualization.

Buttons to reset fields, display orders, and show the price list.

- Price List:

A pop-up window displays the current prices of menu items.

## Technologies Used

- Programming Language: Python

- GUI Framework: Tkinter

- Database: SQLite

- Image Processing: PIL (Pillow library)

## Installation and Setup

- Clone the Repository:

git clone <repository-link>
cd Restaurant_Management_System

- Install Dependencies:
Ensure you have Python 3.x installed. Install the required libraries using:

pip install pillow

- Run the Application:
Execute the following command:

python RDBMS.py

- Database Setup:
The application automatically creates the database (restaurant.db) and the required table upon the first run.

## How to Use

- Launch the application.  

- Enter the quantities of menu items.  

- Click TOTAL to calculate the costs.  

- Use SHOW ORDERS to view saved orders or DISPLAY DATABASE for a tabular view.   

- Reset fields using RESET or quit using EXIT.  

- View prices with the PRICE button.

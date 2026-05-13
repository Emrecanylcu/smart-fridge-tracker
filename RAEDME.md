 # Smart Fridge Nutrition Assistant

Smart Fridge Nutrition Assistant is a Python desktop application developed to track fridge inventory, monitor food freshness, and provide basic nutrition awareness suggestions.

The main goal of this project is to help users see what products they have in their fridge, how much is left, when products may expire, and what products can be suggested based on recent consumption habits.

## Features

- Add food products to the fridge inventory
- Track product amount, unit, category and added date
- Show all products in a clear inventory table
- Search products by name
- Support both English and Turkish product names
- Consume or reduce product amount
- Add more amount to an existing product
- Delete products from the inventory
- Calculate freshness percentage
- Show remaining days before expiration
- Display product status:
  - Fresh
  - Consume Soon
  - Expired
- Show today’s priority products
- Generate weekly usage report
- Provide basic nutrition awareness suggestions
- Export inventory data to CSV
- Show product freshness graph
- Show category distribution graph
- Show weekly usage graph
- Show freshness overview graph
- Store inventory data with JSON

## Technologies Used

- Python
- Tkinter
- ttk Treeview
- JSON
- CSV
- Matplotlib
- datetime module

## Project Purpose

This project was developed as a portfolio project for learning and demonstrating Python desktop application development.

It focuses on:

- GUI development with Tkinter
- File-based data storage with JSON
- Inventory tracking logic
- Basic data analysis
- Freshness calculation
- Simple decision support logic
- Data visualization with Matplotlib

## How It Works

The user can add products such as fruits, vegetables, dairy products, meat, deli products and drinks to the fridge inventory.

Each product stores:

- Product name
- Category
- Amount
- Unit
- Added date
- Freshness percentage
- Remaining days
- Status

The application calculates freshness based on the product’s added date and default shelf life.

Example:

```text
apple → 21 days
milk → 7 days
strawberry → 4 days
chicken → 3 days
fish → 2 days

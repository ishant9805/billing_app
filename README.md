# Billing App

A desktop application built with PySide6 and MySQL to manage customer billing information. This application allows users to create bills, view existing bills, and manage customer details through a tabbed interface.

## Features
- **Create Bills**: Input customer details (name, email, phone) and bill information (amount, description) to generate new bills.
- **View Bills**: Display all bills in a read-only table with details like ID, customer ID, amount, description, and date.
- **View Customers**: Show all customers in a read-only table with their ID, name, email, and phone.
- **MySQL Integration**: Stores data in a local MySQL database with automatic table creation.
- **Tabbed Interface**: Three separate tabs for creating bills, viewing bills, and viewing customers.

## Prerequisites
- **Python**: Ensure Python is installed on your system.
- **MySQL Server**: A locally running MySQL server (e.g., MySQL Community Server).
- **Git**: For cloning the repository (optional).

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ishant9805/billing_app.git
cd billing_app
```

### 2. Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL
- Ensure MySQL is installed and running on your system.
- The application will automatically create a database named `billing_db` and the necessary tables (`customers` and `bills`) on first run.
- Note your MySQL username and password; you'll need them to run the app.

### 4. Configure the Application
- The script uses `root` as the default MySQL user. If you're using a different user, update the `user` field in `billing_app.py`, also update `host` and `port` if your's different:
  ```bash
    set HOST=localhost # Replace with your sql server host
    set PORT=3306 # Replace with your sql server port
    set USER=root # Replace with your sql server user
  ```

## Usage

### Running the Application
1. Use the provided batch file to run the app securely:
   ```bash
   setup.bat
   ```
2. When prompted, enter your MySQL password:
   ```
   Enter MySQL database password:
   ```
3. The application window will open with three tabs:
   - **Create Bill**: Fill in customer and bill details, then click "Create Bill".
   - **View Bills**: Displays all bills; click "Refresh" to update the list.
   - **View Customers**: Shows all customers; click "Refresh" to update.


## Project Structure
```
billing_app/
│
├── .gitignore      # Gitignore file
├── app.py       # Main Python script with the application logic
├── setup.bat      # Batch file to run the app with password prompt
├── requirements.txt      # Libraries you need
└── README.md            # This file
```

## Database Schema
- **customers**:
  - `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
  - `name` (VARCHAR(255))
  - `email` (VARCHAR(255))
  - `phone` (VARCHAR(20))
- **bills**:
  - `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
  - `customer_id` (INT, FOREIGN KEY references customers(id))
  - `amount` (FLOAT)
  - `description` (TEXT)
  - `date` (DATETIME)

## Contact
For issues or suggestions, open an issue on GitHub or contact `ishant9805` at `ishant9805@gmail.com`.

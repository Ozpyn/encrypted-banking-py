import json
import tkinter as tk
from tkinter import messagebox
import getpass

# File path for user data
USER_DATA_FILE = "db.json"

# Load user data from JSON file
def load_user_data():
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

# Save user data to JSON file
def save_user_data(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Load user data
users = load_user_data()

# Function to handle CLI login
def cli_login():
    print("Welcome to the CLI Bank Simulator!")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if username in users and users[username]["password"] == password:
        print("Login successful!")
        cli_account_menu(username)
    else:
        print("Login failed!")

# CLI account menu
def cli_account_menu(username):
    while True:
        print("\nAccount Menu:")
        print("1. View Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            print(f"Current Balance: ${users[username]['balance']}")
        elif choice == "2":
            amount = float(input("Enter amount to deposit: "))
            users[username]['balance'] += amount
            save_user_data(users)
            print(f"Deposited ${amount}. New Balance: ${users[username]['balance']}")
        elif choice == "3":
            amount = float(input("Enter amount to withdraw: "))
            if amount <= users[username]['balance']:
                users[username]['balance'] -= amount
                save_user_data(users)
                print(f"Withdrew ${amount}. New Balance: ${users[username]['balance']}")
            else:
                print("Insufficient funds!")
        elif choice == "4":
            print("Logged out!")
            break
        else:
            print("Invalid choice!")

# Function to handle GUI login
def gui_login():
    username = entry_username.get()
    password = entry_password.get()

    if username in users and users[username]["password"] == password:
        messagebox.showinfo("Login", "Login successful!")
        gui_account_menu(username)
    else:
        messagebox.showerror("Login", "Login failed!")

# GUI account menu
def gui_account_menu(username):
    login_frame.pack_forget()
    account_frame.pack()

    label_balance.config(text=f"Current Balance: ${users[username]['balance']}")

    def deposit():
        amount = float(entry_amount.get())
        users[username]['balance'] += amount
        save_user_data(users)
        label_balance.config(text=f"Current Balance: ${users[username]['balance']}")
        entry_amount.delete(0, tk.END)

    def withdraw():
        amount = float(entry_amount.get())
        if amount <= users[username]['balance']:
            users[username]['balance'] -= amount
            save_user_data(users)
            label_balance.config(text=f"Current Balance: ${users[username]['balance']}")
        else:
            messagebox.showerror("Error", "Insufficient funds!")
        entry_amount.delete(0, tk.END)

    button_deposit.config(command=deposit)
    button_withdraw.config(command=withdraw)

# Setting up the GUI
def setup_gui():
    global app, entry_username, entry_password, login_frame, account_frame
    global label_balance, entry_amount, button_deposit, button_withdraw

    app = tk.Tk()
    app.title("Bank Simulator")

    # Login Frame
    login_frame = tk.Frame(app)
    login_frame.pack(padx=10, pady=10)

    label_username = tk.Label(login_frame, text="Username:")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(login_frame)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_password = tk.Label(login_frame, text="Password:")
    label_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    button_login = tk.Button(login_frame, text="Login", command=gui_login)
    button_login.grid(row=2, columnspan=2, pady=10)

    # Account Frame
    account_frame = tk.Frame(app)

    label_balance = tk.Label(account_frame, text="Current Balance: $0")
    label_balance.grid(row=0, columnspan=2, padx=5, pady=5)

    label_amount = tk.Label(account_frame, text="Amount:")
    label_amount.grid(row=1, column=0, padx=5, pady=5)
    entry_amount = tk.Entry(account_frame)
    entry_amount.grid(row=1, column=1, padx=5, pady=5)

    button_deposit = tk.Button(account_frame, text="Deposit")
    button_deposit.grid(row=2, column=0, padx=5, pady=5)
    button_withdraw = tk.Button(account_frame, text="Withdraw")
    button_withdraw.grid(row=2, column=1, padx=5, pady=5)

    # Exit button
    button_exit = tk.Button(account_frame, text="Exit", command=app.destroy)
    button_exit.grid(row=3, columnspan=2, pady=10)

# Function to choose interface
def choose_interface():
    print("Select interface:")
    print("1. CLI")
    print("2. GUI")
    choice = input("Enter your choice: ")

    if choice == "1":
        cli_login()
    elif choice == "2":
        try:
            setup_gui()
            app.mainloop()
        except tk.TclError:
            print("GUI is not supported in this environment. Falling back to CLI.")
            cli_login()
    else:
        print("Invalid choice!")

# Choose interface
choose_interface()

from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Generate random 4 letters, 2 numbers, and 2 symbols for a password.
    password_letters = [choice(letters) for _ in range(4)]
    password_numbers = [choice(numbers) for _ in range(2)]
    password_symbols = [choice(symbols) for _ in range(2)]
    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    # Reflect password in GUI.
    password_entry.insert(0, password)
    # Copy password to clipboard for easy pasting.
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0:
        messagebox.showerror(title="Head's up!", message=f"Website is empty!")
    elif len(email) == 0:
        messagebox.showerror(title="Head's up!", message=f"Email is empty!")
    elif len(password) == 0:
        messagebox.showerror(title="Head's up!", message=f"Password is empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Creating new file.
                json.dump(new_data, data_file, indent=4)
        else:
            # Password update by deleting old website details and replacing with new one.
            if website in data:
                del data[website]
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH FUNCTION ------------------------------- #
def find_password():
    website = website_entry.get().title()
    if len(website) == 0:
        messagebox.showerror(title="Head's up!", message="Website is empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title=website, message="No details for the website exists.")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {email} \n Password: {password}")
                # Automatically copy password to clipboard for easy pasting.
                pyperclip.copy(password)
            else:
                messagebox.showinfo(title=website, message="Website is not in the list.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(120, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_text = Label(text="Website: ")
website_text.grid(column=0, row=1)

website_entry = Entry(width=31)
website_entry.grid(column=1, row=1, padx=5, pady=5)
website_entry.focus()

search_button = Button(text="Search", width=12, border=3, command=find_password)
search_button.grid(column=2, row=1, padx=5, pady=5)

username_text = Label(text="Email/Username: ")
username_text.grid(column=0, row=2)

email_entry = Entry(width=49, highlightthickness=1)
email_entry.grid(column=1, row=2, columnspan=2, padx=5, pady=5)
email_entry.insert(0, "justpythonthings@gmail.com")

password_text = Label(text="Password: ")
password_text.grid(column=0, row=3)

password_entry = Entry(width=31)
password_entry.grid(column=1, row=3, padx=5, pady=5)

password_button = Button(text="Generate Password", width=14, font=("Arial", 7), border=3, command=generate_password)
password_button.grid(column=2, row=3, padx=5, pady=5)

add_button = Button(text="Add", width=41, border=3, command=save)
add_button.grid(column=1, row=4, columnspan=2, padx=5, pady=5)

window.mainloop()
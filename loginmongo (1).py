import os
import hashlib
import jwt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from project.homepage import HomePage
from pymongo import MongoClient

with open("D:/Let's Code/python projects/myfolder/private.pem", "rb") as f:
    jwt_private_key = RSA.import_key(f.read())
with open("D:/Let's Code/python projects/myfolder/public.pem", "rb") as f:
    jwt_public_key = RSA.import_key(f.read())

# Set the JWT secret key
jwt_secret_key = jwt_private_key

# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017")
db = client["users5"]
users_collection = db["users"]

# Create the users collection if it doesn't exist
users_collection.create_index("username", unique=True)


def create_default_user():

    salt = os.urandom(16).hex()

    # Define the default username and password
    default_username = "admin"
    default_password = "password123"

    # Concatenate the salt and password
    salted_password = salt + default_password

    # Hash the salted password using SHA256
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

    # Encrypt the password using RSA public key
    rsa_key = jwt_private_key
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_password = cipher_rsa.encrypt(default_password.encode()).hex()

    try:
        # Insert the user into the collection
        users_collection.insert_one({
            "username": default_username,
            "salt": salt,
            "encrypted_password": encrypted_password,
            "rsa_private_key": rsa_key.export_key().decode()
        })
        print("Default user created.")
    except:
        print("Default user already exists.")


def decrypt_password(private_key, encrypted_password):
    # Decrypt the password using RSA private key
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    decrypted_password = cipher_rsa.decrypt(
        bytes.fromhex(encrypted_password)).decode()
    return decrypted_password


def encrypt_password(public_key, password):
    # Export the public key as a string
    rsa_public_key_pem = public_key.export_key().decode()

    # Import the public key from the PEM-encoded string
    rsa_key = RSA.import_key(rsa_public_key_pem)

    # Encrypt the password using the RSA public key
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_password = cipher_rsa.encrypt(password.encode()).hex()
    return encrypted_password


def generate_jwt_token(username):
    # Get the PEM-encoded private key
    rsa_private_key_pem = jwt_private_key.export_key().decode()

    # Create the payload for the JWT token
    payload = {"username": username}

    # Generate the JWT token using the PEM-encoded private key
    token = jwt.encode(payload, rsa_private_key_pem, algorithm="RS256")
    return token


def verify_jwt_token(token):
    # Load the RSA public key for verifying the JWT token
    rsa_public_key = RSA.import_key(jwt_public_key)

    try:
        # Verify and decode the JWT token using the RSA public key
        decoded_token = jwt.decode(token, rsa_public_key, algorithms=["RS256"])
        return decoded_token
    except jwt.InvalidTokenError:
        return None


def login():
    
    username = username_entry.get()
    password = password_entry.get()

    # Retrieve the RSA private key and encrypted password for the entered username
    result = users_collection.find_one(
        {"username": username}, {"rsa_private_key": 1, "encrypted_password": 1})

    if result:
        private_key, encrypted_password = result["rsa_private_key"], result["encrypted_password"]

        decrypted_password = decrypt_password(private_key, encrypted_password)

        if password == decrypted_password:
            # Password is correct, generate JWT token
            jwt_token = generate_jwt_token(username)
            # login_message.config(text="Login Successful", fg="green")
            print("JWT Token:", jwt_token)
            login_frame.pack_forget()
            HomePage(root)
            logout_frame.pack()

        # mainloop()
        else:
            # Incorrect password entered
            login_message.config(text="Incorrect Password", fg="red")
    else:
        # User not found
        login_message.config(text="User Not Found", fg="red")


def forgot_password():
    username = username_entry.get()

    # Retrieve the user with the entered username
    result = users_collection.find_one(
        {"username": username}, {"_id": 0, "encrypted_password": 1})

    if result:

        new_password = os.urandom(8).hex()

        encrypted_password = encrypt_password(jwt_public_key, new_password)

        users_collection.update_one({"username": username}, {
                                    "$set": {"encrypted_password": encrypted_password}})

        reset_message.config(text=f"New Password: {new_password}", fg="green")
    else:
        reset_message.config(text="User Not Found", fg="red")


def update_password():
    new_password = new_password_entry.get()

    if new_password:
        username = username_entry.get()

        # Retrieve the RSA private key and encrypted password for the entered username
        result = users_collection.find_one(
            {"username": username}, {"rsa_private_key": 1, "encrypted_password": 1})

        if result:
            private_key, encrypted_password = result["rsa_private_key"], result["encrypted_password"]

            # Decrypt the password using the RSA private key
            decrypted_password = decrypt_password(
                private_key, encrypted_password)

            if new_password == decrypted_password:
                # New password matches the current password
                password_reset_message.config(
                    text="New password cannot be the same as the current password", fg="red")
            else:
                # Encrypt the new password using the RSA public key
                encrypted_new_password = encrypt_password(
                    jwt_public_key, new_password)

                # Update the encrypted password in the database
                users_collection.update_one({"username": username}, {
                                            "$set": {"encrypted_password": encrypted_new_password}})
                password_reset_message.config(
                    text="Password Reset Successful", fg="green")
                show_login_frame()
        else:
            password_reset_message.config(text="User Not Found", fg="red")
    else:
        password_reset_message.config(text="Enter New Password", fg="red")


def logout():
    # Hide the password frame and show the login frame
    password_frame.pack_forget()
    logout_frame.pack_forget()
    show_login_frame()


def show_login_frame():
    login_frame.pack()
    passcode_frame.pack_forget()
    password_frame.pack_forget()


def show_loggedin_frame():
    login_frame.pack_forget()
    passcode_frame.pack_forget()
    password_frame.pack_forget()
    logout_frame.pack()


def show_passcode_frame():
    login_frame.pack_forget()
    passcode_frame.pack()
    password_frame.pack_forget()
    logout_frame.pack_forget()


def show_password_frame():
    login_frame.pack_forget()
    passcode_frame.pack_forget()
    password_frame.pack()
    logout_frame.pack_forget()


def confirm_passcode():
    passcode = passcode_entry.get()
    if passcode == "123456":
        show_password_frame()
    else:
        passcode_message.config(text="Incorrect Passcode", fg="red")


# Create the main Tkinter window
root = tk.Tk()
BG_COLOR = '#0F054C'
FONT_COLOR = '#F6F6F6'
BTN_COLOR = "#61CE70"

root.geometry("400x300")
root.title("Login Page")
root['bg'] = BG_COLOR
# root.title("Password Reset")

# Create frames for each screen
login_frame = tk.Frame(root, bg=BG_COLOR)
passcode_frame = tk.Frame(root, bg=BG_COLOR)
password_frame = tk.Frame(root, bg=BG_COLOR)
logout_frame = tk.Frame(root, bg=BG_COLOR)


logout_button = tk.Button(logout_frame, bg=BTN_COLOR,
                          fg=FONT_COLOR, text="Logout", command=logout)
logout_button.pack(pady=10)

root_directory = os.getcwd()

print('root_dir', root_directory)
top_image = os.path.join(root_directory, "project",
                         "folderframes", "imgs", "top.png")
hamb_image = os.path.join(root_directory, "project",
                          "folderframes", "imgs", "hamburger.png")

top_image_path = top_image.replace("\\", "/")
pil_img = Image.open(str(top_image_path))
image = tk.PhotoImage(file=str(top_image_path))
canvas = tk.Canvas(login_frame, background='#F6F6F6',
                   height=pil_img.height, width=pil_img.width, highlightthickness=0)
canvas.create_image(0, 0, anchor="nw", image=image)
canvas.image = image
print(canvas.image.width)
canvas.pack()


username_label = tk.Label(login_frame, bg=BG_COLOR,
                          fg=FONT_COLOR, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_frame, width=20)
username_entry.pack(pady=5)
password_label = tk.Label(login_frame, bg=BG_COLOR,
                          fg=FONT_COLOR, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_frame, show="*", width=20)
password_entry.pack(pady=5)
login_button = tk.Button(login_frame, bg=BTN_COLOR,
                         fg=FONT_COLOR, text="Login", command=login)
login_button.pack(pady=10)
login_message = tk.Label(login_frame, bg=BG_COLOR, fg=FONT_COLOR, text="")
login_message.pack()
forgot_password_button = tk.Button(
    login_frame, text="Forgot Password", command=show_passcode_frame, bg=BTN_COLOR, fg=FONT_COLOR)
forgot_password_button.pack()
disclamer_label_left = tk.Label(root, bg=BG_COLOR, fg=FONT_COLOR,
                                text="Proprietry Technologies", anchor="w", wraplength=1000000)
disclamer_label_left.pack_propagate(False)
disclamer_label_left.pack(side="left", pady=(0, 5), anchor="sw", padx=5)
disclamer_label_right = tk.Label(root, bg=BG_COLOR, fg=FONT_COLOR,
                                 text="Powered by Envirya Projects Pvt. Ltd.", anchor="e", wraplength=1000000)
disclamer_label_right.pack_propagate(False)
disclamer_label_right.pack(side="right", pady=(0, 5), anchor="se", padx=5)
# Passcode screen
passcode_label = tk.Label(passcode_frame, bg=BG_COLOR,
                          fg=FONT_COLOR, text="Enter Passcode:")
passcode_label.pack()
passcode_entry = tk.Entry(passcode_frame, show="*", width=20)
passcode_entry.pack(pady=5)
confirm_passcode_button = tk.Button(
    passcode_frame, bg=BTN_COLOR, fg=FONT_COLOR, text="Confirm Passcode", command=confirm_passcode)
confirm_passcode_button.pack(pady=10)
passcode_message = tk.Label(
    passcode_frame, bg=BG_COLOR, fg=FONT_COLOR, text="")
passcode_message.pack()

# Password screen
new_password_label = tk.Label(
    password_frame, bg=BG_COLOR, fg=FONT_COLOR, text="New Password:")
new_password_label.pack()
new_password_entry = tk.Entry(password_frame, show="*", width=20)
new_password_entry.pack(pady=5)
update_password_button = tk.Button(
    password_frame, bg=BTN_COLOR, fg=FONT_COLOR, text="Update Password", command=update_password)
update_password_button.pack(pady=10)
password_reset_message = tk.Label(
    password_frame, bg=BG_COLOR, fg=FONT_COLOR, text="")
password_reset_message.pack()


show_login_frame()
# HomePage(root)

create_default_user()

root.mainloop()

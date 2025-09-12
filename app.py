import json
import os
from cryptography.fernet import Fernet

DATA_FILE = "data.json"
KEY_FILE = "secret.key"

# Generate encryption key if it doesn't exist
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

# Load the encryption key
def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

# Encrypt a message
def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

# Decrypt a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

# Load data from file
def load_data(key):
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            encrypted_data = json.load(f)
        data = {}
        for k, v in encrypted_data.items():
            data[k] = decrypt_message(v.encode(), key)
        return data
    except Exception as e:
        print("Error loading data:", e)
        return {}

# Save data to file (encrypted)
def save_data(data, key):
    encrypted_data = {}
    for k, v in data.items():
        encrypted_data[k] = encrypt_message(v, key).decode()
    with open(DATA_FILE, "w") as f:
        json.dump(encrypted_data, f, indent=4)

# Add new data entry
def add_data(key):
    data = load_data(key)
    field = input("Enter field name (e.g., 'password', 'API key'): ")
    value = input(f"Enter value for '{field}': ")
    data[field] = value
    save_data(data, key)
    print(f"{field} saved securely!\n")

# View stored data
def view_data(key):
    data = load_data(key)
    if not data:
        print("No data found.\n")
        return
    print("=== Stored Data ===")
    for k, v in data.items():
        print(f"{k}: {v}")
    print("===================\n")

# Main menu
def main():
    generate_key()
    key = load_key()
    while True:
        print("=== Secure Data Handling ===")
        print("1. Add new data")
        print("2. View stored data")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_data(key)
        elif choice == "2":
            view_data(key)
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()

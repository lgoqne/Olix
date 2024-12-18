import os
import json
from cryptography.fernet import Fernet
from getpass import getpass

PASSWORD_FILE = 'passwords.json'
KEY_FILE = 'secret.key'

# Function to generate and save a key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

# Function to load the encryption key
def load_key():
    return open(KEY_FILE, 'rb').read()

# Function to encrypt a password
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

# Function to decrypt a password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()

# Function to save passwords to a file
def save_passwords(passwords):
    with open(PASSWORD_FILE, 'w') as f:
        json.dump(passwords, f)

# Function to load passwords from a file
def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to add a new password
def add_password(account, password, key):
    passwords = load_passwords()
    encrypted_password = encrypt_password(password, key)
    passwords[account] = encrypted_password.decode()
    save_passwords(passwords)
    print(f"Password for {account} added successfully.")

# Function to retrieve a password
def retrieve_password(account, key):
    passwords = load_passwords()
    if account in passwords:
        encrypted_password = passwords[account].encode()
        return decrypt_password(encrypted_password, key)
    else:
        print(f"No password found for account: {account}")
        return None

# Main function to run the password manager
def main():
    if not os.path.exists(KEY_FILE):
        print("Encryption key not found. Generating a new key...")
        generate_key()
    
    key = load_key()

    while True:
        print("\n--- Password Manager ---")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Quit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            account = input("Enter the account name (e.g., website or app name): ")
            password = getpass("Enter the password: ")
            add_password(account, password, key)

        elif choice == '2':
            account = input("Enter the account name: ")
            password = retrieve_password(account, key)
            if password:
                print(f"Password for {account}: {password}")

        elif choice == '3':
            break

if __name__ == "__main__":
    main()

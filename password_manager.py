# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/

# Copyright 2025 emanoyhl and emanoyhl.net find me at github.com/emanoyhl 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import random
import string
from cryptography.fernet import Fernet
from getpass import getpass

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json'):
        self.key_file = key_file
        self.data_file = data_file
        self.load_key()
        self.load_data()

    def load_key(self):
        """Load the encryption key."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                self.key = file.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(self.key)

        self.fernet = Fernet(self.key)

    def load_data(self):
        """Load stored passwords."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def save_data(self):
        """Save passwords to file."""
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def encrypt_password(self, password):
        """Encrypt a password."""
        return self.fernet.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        """Decrypt a password."""
        return self.fernet.decrypt(encrypted_password.encode()).decode()

    def add_password(self, website, password):
        """Add a new password."""
        encrypted_password = self.encrypt_password(password)
        self.data[website] = encrypted_password
        self.save_data()
        print(f"Password for {website} saved.")

    def retrieve_password(self, website):
        """Retrieve a password."""
        if website in self.data:
            encrypted_password = self.data[website]
            return self.decrypt_password(encrypted_password)
        else:
            print("Website not found.")

    def generate_password(self, length=12):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def autofill(self, website):
        """Display the password for autofill."""
        password = self.retrieve_password(website)
        if password:
            print(f"Autofill for {website}: {password}")

def main():
    pm = PasswordManager()

    while True:
        print("\n1. Add Password")
        print("2. Retrieve Password")
        print("3. Generate Password")
        print("4. Autofill")
        print("5. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            website = input("Enter website: ")
            password = getpass("Enter password (or leave blank to generate): ")
            if not password:
                password = pm.generate_password()
                print(f"Generated password: {password}")
            pm.add_password(website, password)

        elif choice == '2':
            website = input("Enter website: ")
            print(f"Password: {pm.retrieve_password(website)}")

        elif choice == '3':
            length = int(input("Enter password length: "))
            print(f"Generated password: {pm.generate_password(length)}")

        elif choice == '4':
            website = input("Enter website: ")
            pm.autofill(website)

        elif choice == '5':
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

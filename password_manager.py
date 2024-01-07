from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, master_password, storage_file='passwords.json'):
        self.master_password = master_password.encode()
        self.storage_file = storage_file
        self.key = self._generate_key()

    def _generate_key(self):
        kdf = Fernet.generate_key()
        key = Fernet(kdf)
        return key

    def _load_passwords(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'rb') as file:
                data = file.read()
                decrypted_data = Fernet(self.key).decrypt(data)
                return json.loads(decrypted_data)
        else:
            return {}

    def _save_passwords(self, passwords):
        with open(self.storage_file, 'wb') as file:
            encrypted_data = Fernet(self.key).encrypt(json.dumps(passwords).encode())
            file.write(encrypted_data)

    def add_password(self, website, username, password):
        passwords = self._load_passwords()
        passwords[website] = {'username': username, 'password': password}
        self._save_passwords(passwords)

    def get_password(self, website):
        passwords = self._load_passwords()
        return passwords.get(website, None)

if __name__ == "__main__":
    master_password = input("Enter your master password: ")

    password_manager = PasswordManager(master_password)

    # Example: Adding passwords
    password_manager.add_password('example.com', 'user123', 'securepassword123')
    password_manager.add_password('testsite.com', 'admin', 'strongpassword456')

    # Example: Retrieving passwords
    website = input("Enter the website to retrieve the password: ")
    stored_password = password_manager.get_password(website)

    if stored_password:
        print(f"Username: {stored_password['username']}")
        print(f"Password: {stored_password['password']}")
    else:
        print("Password not found.")

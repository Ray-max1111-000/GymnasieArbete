import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey

class PasswordManagerCore:
    def __init__(self):
        self.cipher = None
        self.initialized = False
        
    def initialize_encryption(self, master_password: str):
        """Initialize encryption system with master password"""
        if not master_password or len(master_password) < 12:
            raise ValueError("Master password must be at least 12 characters")
            
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        
        with open("encryption.key", "wb") as f:
            f.write(salt + key)
            
        self.cipher = Fernet(key)
        self.initialized = True

    def load_encryption(self, master_password: str):
        """Load existing encryption system"""
        try:
            with open("encryption.key", "rb") as f:
                data = f.read()
                salt = data[:16]
                stored_key = data[16:]
                
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            derived_key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
            
            if derived_key != stored_key:
                raise InvalidKey("Invalid master password")
                
            self.cipher = Fernet(derived_key)
            self.initialized = True
        except FileNotFoundError:
            raise RuntimeError("Encryption system not initialized")

    def save_password_entry(self, entry: dict):
        """Save encrypted password entry"""
        if not self.initialized:
            raise RuntimeError("Encryption system not initialized")
            
        if not all(key in entry for key in ["website", "username", "password"]):
            raise ValueError("Invalid entry format")
            
        encrypted_password = self.cipher.encrypt(entry["password"].encode()).decode()
        
        try:
            with open("passwords.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            
        data.append({
            "website": entry["website"],
            "username": entry["username"],
            "password": encrypted_password
        })
        
        with open("passwords.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_passwords(self):
        """Load and decrypt all passwords"""
        if not self.initialized:
            raise RuntimeError("Encryption system not initialized")
            
        try:
            with open("passwords.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
        for entry in data:
            entry["password"] = self.cipher.decrypt(entry["password"].encode()).decode()
            
        return data
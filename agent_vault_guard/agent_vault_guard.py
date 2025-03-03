import os
import json
import random
import string
from cryptography.fernet import Fernet
from uagents import Agent, Context, Model

# Query Model for Password Actions
class VaultQuery(Model):
    action: str
    user_name: str
    application: str = None
    password: str = None
    upper: int = 0
    lower: int = 0
    digits: int = 0
    special: int = 0
    sender_address: str 

# Response Model
class VaultResponse(Model):
    status: str
    message: str

# Function to load or generate encryption key
def load_or_generate_key():
    key_file = "vault_key.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key

key = load_or_generate_key()
cipher = Fernet(key)

# Function to load user vault
def load_vault(user_name):
    file_path = f"{user_name}_vault.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}

# Function to save user vault
def save_vault(user_name, vault):
    file_path = f"{user_name}_vault.json"
    with open(file_path, "w") as file:
        json.dump(vault, file, indent=4)

# Function to generate a strong password
def generate_password(upper, lower, digits, special):
    length = upper + lower + digits + special
    if length <= 0:
        return "Invalid password length."

    char_sets = (
        (string.ascii_uppercase * upper) +
        (string.ascii_lowercase * lower) +
        (string.digits * digits) +
        (string.punctuation * special)
    )

    password = ''.join(random.sample(char_sets, length))
    return password

# Server Agent Setup
vaultGuardAgent = Agent(
    name="VaultGuard",
    port=5080,
    endpoint="http://localhost:5080/submit",
    seed="vault_guard_seed"
)

@vaultGuardAgent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"Vault Guard Agent started at {ctx.agent.address}")

@vaultGuardAgent.on_message(model=VaultQuery)
async def handle_vault_request(ctx: Context, sender: str, msg: VaultQuery):
    vault = load_vault(msg.user_name)

    if msg.action == "generate":
        password = generate_password(msg.upper, msg.lower, msg.digits, msg.special)
        response = VaultResponse(status="success", message=password)
    
    elif msg.action == "store":
        vault[msg.application] = cipher.encrypt(msg.password.encode()).decode()
        save_vault(msg.user_name, vault)
        response = VaultResponse(status="success", message=f"Password stored for {msg.application}.")

    elif msg.action == "retrieve":
        encrypted_password = vault.get(msg.application)
        if encrypted_password:
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            response = VaultResponse(status="success", message=decrypted_password)
        else:
            response = VaultResponse(status="error", message="No password found.")

    elif msg.action == "delete":
        if msg.application in vault:
            del vault[msg.application]
            save_vault(msg.user_name, vault)
            response = VaultResponse(status="success", message=f"Password for {msg.application} deleted.")
        else:
            response = VaultResponse(status="error", message="Application not found.")

    else:
        response = VaultResponse(status="error", message="Invalid action.")

    await ctx.send(sender, response)

if __name__ == "__main__":
    vaultGuardAgent.run()

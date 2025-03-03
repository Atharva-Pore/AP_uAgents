![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)  ![domain:security](https://img.shields.io/badge/security-3D8BD3)  ![domain:cybersecurity](https://img.shields.io/badge/cybersecurity-3D8BD3)  ![domain:password-management](https://img.shields.io/badge/password%20management-3D8BD3)  ![domain:encryption](https://img.shields.io/badge/encryption-3D8BD3)  ![domain:vault](https://img.shields.io/badge/vault-3D8BD3)  ![domain:decentralized](https://img.shields.io/badge/decentralized-3D8BD3)  ![domain:uAgents](https://img.shields.io/badge/uAgents-3D8BD3)  ![domain:privacy](https://img.shields.io/badge/privacy-3D8BD3)  

# Vault Guard Agent

**Description**:  
Vault Guard Agent is a robust, AI-powered password manager built with the uAgents framework. It securely generates, stores, retrieves, and deletes passwords through encrypted, user-specific vaults. This decentralized solution ensures your credentials remain safe and accessible only to you.

---

## Data Models

**Input Data Model (Vault Query Model)**
```python
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
```

**Output Data Model (Vault Response Model)**
```python
class VaultResponse(Model):
    status: str
    message: str
```

---

## Features

- **Generate Secure Passwords**  
  Create strong passwords with a customizable mix of uppercase letters, lowercase letters, digits, and special characters.

- **Store Passwords Securely**  
  Encrypt and save passwords in a dedicated user vault using the `cryptography` library.

- **Retrieve Stored Passwords**  
  Decrypt and access passwords securely on demand.

- **Delete Stored Passwords**  
  Remove passwords for specific applications from your vault.

---

## Components

### Vault Guard Agent (Server)
- **Responsibilities**:  
  Handles encryption/decryption of passwords, manages user vault files, and processes actions (generate, store, retrieve, delete) via secure agent communication.
- **Encryption**:  
  Utilizes AES encryption from the `cryptography` library to ensure data security.

### Vault Client Agent
- **Responsibilities**:  
  Provides a command-line interface for users to interact with the Vault Guard Agent. It sends requests based on user input and displays responses.
- **Communication**:  
  Uses uAgents for decentralized and secure messaging between the client and the server.

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Required packages:
  ```bash
  pip install uagents cryptography
  ```

### Running the Vault Guard Agent (Server)
```bash
python vault_guard.py
```

### Running the Vault Client Agent (Client)
```bash
python vault_client.py
```

---

## Client Code

Below is the client code that can be used to communicate with the Vault Guard Agent. Simply copy and run it to interact with your password vault.

```python
import sys
from uagents import Agent, Context, Model

# Define Query and Response Models
class VaultQuery(Model):
    action: str
    user_name: str
    application: str = None
    password: str = None
    upper: int = 0
    lower: int = 0
    digits: int = 0
    special: int = 0
    sender_address: str  # Added sender_address to the query model

class VaultResponse(Model):
    status: str
    message: str

# Client Agent Setup
clientAgent = Agent(
    name="VaultClient",
    port=5070,
    endpoint="http://localhost:5070/submit",
    seed="vault_client_seed"
)

action: str = ''
usr_name: str = ''
application_name: str = ''
password: str = ''
upper: int = 0
lower: int = 0
digits: int = 0
special: int = 0
Choice: int = 0

# Server Agent Address
SERVER_AGENT_ADDRESS = "agent1qtdavl5drwswuvksjemruszu60gu7n4nvmk3kkfl9tev7qfh3cw7xwdsfuk"

@clientAgent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Client Agent {ctx.agent.name} started at {ctx.agent.address}')

    if Choice == "1":
        # Store password
        message = VaultQuery(
            action="store", 
            user_name=usr_name, 
            application=application_name, 
            password=password, 
            sender_address=ctx.agent.address
        )
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application_name}")
    
    elif Choice == "2":
        # Retrieve password
        message = VaultQuery(
            action="retrieve", 
            user_name=usr_name, 
            application=application_name, 
            sender_address=ctx.agent.address
        )
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application_name}")

    elif Choice == "3":
        # Delete password
        message = VaultQuery(
            action="delete", 
            user_name=usr_name, 
            application=application_name, 
            sender_address=ctx.agent.address
        )
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application_name}")

    elif Choice == "4":
        # Generate and store password
        message = VaultQuery(
            action="generate", 
            user_name=usr_name, 
            application=application_name, 
            upper=upper, 
            lower=lower, 
            digits=digits, 
            special=special, 
            sender_address=ctx.agent.address
        )
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application_name}")
    elif Choice == "5":
        # Exit program
        print("Exiting...")
        sys.exit(-1)
    else:
        print("Invalid choice, please try again.")
    
@clientAgent.on_message(model=VaultResponse)
async def handle_response(ctx: Context, sender: str, msg: VaultResponse):
    ctx.logger.info(f"Response from {sender}: {msg.message}")
    print("Response:", msg.message)
    
def prepare_query(Action: str = None, 
                  UserName: str = None, 
                  AppName: str = None,
                  Password: str = None,
                  Upper: int = None,
                  Lower: int = None,
                  Digits: int = None,
                  Special: int = None,
                  choice: int = None) -> None:
    """
    Sets the global variables.

    Parameters:
        @action: str 
        @usr_name: str
        @application_name: str
        @password: str
        @upper: int
        @lower: int
        @digits: int
        @special: int
        @choice: int
    """
    global action 
    global usr_name 
    global application_name 
    global password 
    global upper 
    global lower
    global digits 
    global special
    global Choice

    action = Action
    usr_name = UserName
    application_name = AppName
    password = Password
    upper = Upper
    lower = Lower
    digits = Digits
    special = Special
    Choice = choice
    
# Run the client agent
if __name__ == "__main__":
    """Prompt user for a single action choice."""
    print("\nOptions:")
    print("1. Store Password")
    print("2. Retrieve Password")
    print("3. Delete Password")
    print("4. Generate and Store Password")
    print("5. Exit")
    choice = input("Choose an option: ").strip()        

    if choice == "1":
        # Store password
        user_name = input("Enter your username: ").strip()
        application = input("Enter application/website name: ").strip()
        password = input("Enter password: ").strip()
        prepare_query(UserName=user_name,
                      AppName=application,
                      Password=password,
                      choice=choice)
    
    elif choice == "2":
        # Retrieve password
        user_name = input("Enter your username: ").strip()
        application = input("Enter application/website name: ").strip()
        prepare_query(UserName=user_name,
                      AppName=application,
                      choice=choice)

    elif choice == "3":
        # Delete password
        user_name = input("Enter your username: ").strip()
        application = input("Enter application/website name: ").strip()
        prepare_query(UserName=user_name,
                      AppName=application,
                      choice=choice)

    elif choice == "4":
        # Generate and store password
        user_name = input("Enter your username: ").strip()
        application = input("Enter application/website name: ").strip()
        upper = int(input("Number of uppercase letters: "))
        lower = int(input("Number of lowercase letters: "))
        digits = int(input("Number of digits: "))
        special = int(input("Number of special characters: "))
        prepare_query(UserName=user_name,
                      AppName=application,
                      Upper=upper,
                      Lower=lower,
                      Digits=digits,
                      Special=special,
                      choice=choice)

    elif choice == "5":
        # Exit program
        print("Exiting...")
        sys.exit(-1)
    else:
        print("Invalid choice, please try again.")
    clientAgent.run()
```

---

## Security Measures

- **Encryption**:  
  All passwords are encrypted using AES encryption provided by the `cryptography` library.

- **User-Specific Vaults**:  
  Each user’s credentials are stored in a dedicated, encrypted vault file.

- **Decentralized Communication**:  
  Secure message passing is handled via the uAgents framework.

---

## Future Enhancements

- Multi-user authentication.
- Integration with cloud-based vault storage.
- Development of a user-friendly graphical interface (GUI).

---
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
        message = VaultQuery(action="store", 
                             user_name=usr_name, 
                             application=application_name, 
                             password=password, 
                             sender_address=ctx.agent.address)
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application}")
    
    elif Choice == "2":
        # Retrieve password
        message = VaultQuery(action="retrieve", 
                             user_name=usr_name, application=application_name, 
                             sender_address=ctx.agent.address)
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application}")

    elif Choice == "3":
        # Delete password
        message = VaultQuery(action="delete", 
                             user_name=usr_name, 
                             application=application_name, 
                             sender_address=ctx.agent.address)
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application}")

    elif Choice == "4":
        # Generate and store password
        message = VaultQuery(action="generate", 
                             user_name=usr_name, 
                             application=application_name, 
                             upper=upper, 
                             lower=lower, 
                             digits=digits, 
                             special=special, 
                             sender_address=ctx.agent.address)
        await ctx.send(SERVER_AGENT_ADDRESS, message)
        ctx.logger.info(f"Request sent to Vault Guard: {message.action} - {application}")
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

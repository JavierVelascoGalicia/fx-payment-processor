
from fastapi import FastAPI
from wallets_api.controllers.user_controller import user_controller
from wallets_api.controllers.wallet_controller import wallet_controller
from wallets_api.database import create_all_tables

# Initialize the root application
app = FastAPI()
create_all_tables()

app.include_router(user_controller)
app.include_router(wallet_controller)

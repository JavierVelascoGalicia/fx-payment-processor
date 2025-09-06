
from fastapi import FastAPI
from wallets_api.controllers.user_controller import user_controller

# Initialize the root application
app = FastAPI()

app.include_router(user_controller)

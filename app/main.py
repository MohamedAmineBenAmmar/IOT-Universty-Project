from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.sensor.routers import sensor_routes
from tests import test_routes

# Init the fastAPI app
app = FastAPI()

# registering the modules routers
app.include_router(sensor_routes.router)
app.include_router(test_routes.router)

# Configuring CORSMiddleware
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
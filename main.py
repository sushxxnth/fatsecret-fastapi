import httpx
import os
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# FatSecret API credentials
CLIENT_ID = os.getenv("FATSECRET_CLIENT_ID")
CLIENT_SECRET = os.getenv("FATSECRET_CLIENT_SECRET")
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"

# Function to get OAuth 2.0 access token
async def get_access_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        response.raise_for_status()  # Raise an error if request fails
        return response.json()["access_token"]

# API endpoint to search for food items
@app.get("/search_food/")
async def search_food(query: str, access_token: str = Depends(get_access_token)):
    url = "https://platform.fatsecret.com/rest/server.api"
    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json"
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()  # Ensure request was successful
        return response.json()


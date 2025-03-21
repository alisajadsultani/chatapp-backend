import os
from fastapi import FastAPI, WebSocket
from supabase import create_client

app = FastAPI()

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

# Fetch Display Name API
@app.get("/get_display_name/{email}")
async def get_display_name(email: str):
    response = supabase.table("users").select("display_name").eq("email", email).execute()
    if response.data:
        return {"display_name": response.data[0]["display_name"]}
    return {"display_name": "Unknown"}

# WebSocket for real-time chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")

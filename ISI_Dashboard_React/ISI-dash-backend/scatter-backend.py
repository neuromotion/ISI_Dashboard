from fastapi import FastAPI, WebSocket
import asyncio
import time
import json
import numpy as np

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            x = [1,2,3]
            y = (np.sin(time.time()) * np.ones(3)).tolist()
            message = {"x":x,"y":y}
            await websocket.send_text(json.dumps(message))
            await asyncio.sleep(1/15) 
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
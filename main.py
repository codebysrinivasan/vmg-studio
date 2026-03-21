from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import uvicorn
import os
import base64
import logging

# Setup basic logging to see errors in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS so your frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI session (IsNet is best for general products)
try:
    session = new_session("isnet-general-use")
except Exception as e:
    logger.error(f"Failed to load AI model: {e}")
    session = None

@app.get("/")
async def serve_home():
    # Looks for index.html in the same folder as main.py
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"error": "index.html not found on server"}, status_code=404)

@app.post("/remove-bg-multiple")
async def remove_bg_multiple(files: list[UploadFile] = File(...)):
    processed_images = []
    
    for file in files:
        try:
            input_data = await file.read()
            
            # AI Processing with professional matting settings
            output_data = remove(
                input_data,
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )
            
            # Encode to Base64 to send back to the browser
            base64_image = base64.b64encode(output_data).decode('utf-8')
            processed_images.append({
                "filename": file.filename,
                "data": f"data:image/png;base64,{base64_image}"
            })
            
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {e}")
            continue
            
    return JSONResponse(content={"images": processed_images})

if __name__ == "__main__":
    # Get port from environment (Render uses 10000 by default)
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

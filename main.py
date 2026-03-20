import os
import uvicorn
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import PIL.Image as Image

app = FastAPI(title="RedPepper AI Engine")

# Enable CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI session once to save memory
# This uses the 'isnet-general-use' model you saw in your logs
session = new_session("isnet-general-use")

# 1. Background Removal Endpoint
@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Read uploaded image
        input_image = await file.read()
        
        # Process image with rembg
        # alpha_matting=True helps with the "White-on-White" scenarios you mentioned
        output_image = remove(
            input_image, 
            session=session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10
        )
        
        # Return the processed image as a PNG stream
        return StreamingResponse(io.BytesIO(output_image), media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Serve Frontend
# Ensure your index.html is inside a folder named 'static'
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    if os.path.exists("static/index.html"):
        return FileResponse('static/index.html')
    return {"message": "RedPepper AI Engine is Running. Upload index.html to /static to see the UI."}

if __name__ == "__main__":
    # CRITICAL: Render requires binding to the 'PORT' environment variable
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

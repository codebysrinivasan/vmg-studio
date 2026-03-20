import os
import uvicorn
import io
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from typing import List

app = FastAPI(title="RedPepper AI Engine")

# Enable CORS for VMG frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI session (downloads ~179MB on first boot)
session = new_session("isnet-general-use")

@app.post("/remove-bg-multiple")
async def remove_bg_multiple(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        try:
            input_image = await file.read()
            
            # High-precision Alpha Matting for white-on-white products
            output_image = remove(
                input_image, 
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10
            )
            
            # Convert to Base64 for the HTML Gallery
            base64_img = base64.b64encode(output_image).decode('utf-8')
            results.append({
                "filename": file.filename,
                "data": f"data:image/png;base64,{base64_img}"
            })
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            continue
            
    return {"images": results}

@app.get("/")
async def read_index():
    # Looks for index.html in the same root folder
    index_path = os.path.join(os.getcwd(), "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found. Ensure it is in the root directory."}

if __name__ == "__main__":
    # This automatically picks up Render's default (10000)
    # or falls back to 10000 if nothing is set.
    port = int(os.environ.get("PORT", 10000))
    
    # host MUST be 0.0.0.0 for Render to see the app
    uvicorn.run(app, host="0.0.0.0", port=port)

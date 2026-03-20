from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import uvicorn
import io
import os
import base64

app = FastAPI()
base_path = os.path.dirname(os.path.abspath(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI session once for speed
session = new_session("isnet-general-use")

@app.get("/")
async def serve_home():
    html_path = os.path.join(base_path, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"error": "index.html not found in the current directory."}

@app.post("/remove-bg-multiple")
async def remove_bg_multiple(files: list[UploadFile] = File(...)):
    processed_images = []
    for file in files:
        try:
            input_data = await file.read()
            # Professional settings for clean edges
            output_data = remove(
                input_data, 
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )
            
            # Convert to base64 to send in JSON
            base64_image = base64.b64encode(output_data).decode('utf-8')
            processed_images.append({
                "filename": file.filename,
                "data": f"data:image/png;base64,{base64_image}"
            })
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            
    return JSONResponse(content={"images": processed_images})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8501)
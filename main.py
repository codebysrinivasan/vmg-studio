import os
import uvicorn
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from typing import List

app = FastAPI(title="RedPepper AI Engine")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize session (lightweight default model)
session = new_session()

# Max file size (5MB per image)
MAX_FILE_SIZE = 5 * 1024 * 1024

@app.post("/remove-bg-multiple")
async def remove_bg_multiple(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        try:
            input_image = await file.read()

            # 🔴 File size check (VERY IMPORTANT for Render)
            if len(input_image) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename} is too large (max 5MB allowed)"
                )

            # ✅ Background removal (lightweight)
            output_image = remove(input_image, session=session)

            # Convert to Base64
            base64_img = base64.b64encode(output_image).decode("utf-8")

            results.append({
                "filename": file.filename,
                "data": f"data:image/png;base64,{base64_img}"
            })

        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            continue

    if not results:
        raise HTTPException(status_code=500, detail="No images processed")

    return {"images": results}


@app.get("/")
async def read_index():
    index_path = os.path.join(os.getcwd(), "index.html")

    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {"error": "index.html not found. Put it in root folder."}


# ✅ Render-compatible startup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

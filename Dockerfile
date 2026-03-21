# 1. Use a Python image that includes essential build tools
FROM python:3.9-slim

# 2. Install system libraries required for OpenCV and rembg
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /code

# 4. Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. PRE-DOWNLOAD THE AI MODEL 
# This prevents the app from hanging on the first upload
RUN python -c "from rembg import new_session; new_session('isnet-general-use')"

# 6. Copy all your project files (app.py, index.html, etc.)
COPY . .

# 7. Start the app using the Port Render provides
# We use 0.0.0.0 so it is accessible from the internet
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]

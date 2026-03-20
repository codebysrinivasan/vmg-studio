# 1. Use Python 3.10 (more stable for your current library versions)
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /code

# 3. Install OpenCV & AI dependencies (CRITICAL for rembg)
# Without these, your app will fail to start on Render.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy and install requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy your main.py and index.html (Root files)
COPY . .

# 6. Start the RedPepper Engine
CMD ["python", "main.py"]

FROM python:3.9-slim

# Install system dependencies with updated package names
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Pre-download the AI model
RUN python -c "from rembg import new_session; new_session('isnet-general-use')"

COPY . .

# Render uses port 10000 by default
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

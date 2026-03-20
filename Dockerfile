# 1. Use Python 3.10
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /code

# 3. Copy and install requirements 
# (opencv-python-headless handles the graphics libraries now)
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Copy your main.py and index.html
COPY . .

# 5. Start the engine on port 4000
CMD ["python", "main.py"]

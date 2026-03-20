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

# 5. OPEN THE DEFAULT RENDER PORT
EXPOSE 10000

# 6. Start the engine
CMD ["python", "main.py"]

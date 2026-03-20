FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create a folder for the HTML file
COPY . .

# Run the app
CMD ["python", "main.py"]
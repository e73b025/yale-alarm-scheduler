FROM python:3.8

# Set working dir
WORKDIR /app

# Copy over files
COPY . .

# Install dependenices
RUN pip install -r requirements.txt

# Run the script
CMD python run.py
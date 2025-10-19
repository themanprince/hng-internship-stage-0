# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the image
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will listen on
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

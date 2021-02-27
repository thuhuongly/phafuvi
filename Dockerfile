FROM python:3.8-slim-buster

# Install Python dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the codebase into the image
COPY ./app /app
WORKDIR /app
ENV DASH_DEBUG_MODE True # False
EXPOSE 8050
CMD ["python", "app.py"]
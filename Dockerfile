FROM python:3.10-slim
  
ENV PYTHONDONTWRITEBYTECODE 1  
ENV PYTHONUNBUFFERED 1  

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uvicorn
RUN pip install --no-cache-dir psycopg2-binary

WORKDIR /src  
COPY ./src /src
COPY ./requirments.txt ./requirments.txt 
  
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirments.txt
EXPOSE 8000
CMD ["uvicorn", "new_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
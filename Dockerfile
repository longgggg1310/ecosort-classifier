FROM python:3.10-slim

ENV APP_DIR=/app/backend
ENV PORT=30000

RUN apt-get update && apt-get install -y \
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_DIR}

COPY backend/requirements.txt ${APP_DIR}/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ${APP_DIR}

EXPOSE ${PORT}
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]

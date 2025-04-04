FROM python:3.10-slim


RUN apt-get update && apt-get install -y \
        libgl1\
        libgl1-mesa-glx \ 
        libglib2.0-0 -y && \
        rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY backend /app



ENV MODEL_PATH /app/models/model.h5

# Port will be exposed, for documentation only
EXPOSE 30000

# Disable pip cache to shrink the image size a little bit,
# since it does not need to be re-installed
RUN pip install python-dotenv
RUN pip install -r requirements.txt 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]

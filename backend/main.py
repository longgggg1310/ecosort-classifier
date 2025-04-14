from fastapi import FastAPI, File, UploadFile, HTTPException
import datetime
import uvicorn
import shutil
import os
from PIL import Image

from utils import predict_normal, zeroshot

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from loguru import logger
import socket
from contextlib import closing
from opentelemetry.sdk.trace.sampling import ALWAYS_ON
from starlette.types import ASGIApp
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanExporterGRPC,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.trace.status import Status, StatusCode


app = FastAPI()


# Get configuration from environment variables
OTLP_GRPC_ENDPOINT = "jaeger-jaeger.tracing.svc.cluster.local:4317"


# Setting up Jaeger tracing
def setting_jaeger(app: ASGIApp, log_correlation: bool = True) -> None:
    try:
        tracer = TracerProvider(
            resource=Resource.create({SERVICE_NAME: "trash-detection"})
        )
        trace.set_tracer_provider(tracer)

        otlp_exporter = OTLPSpanExporter(
            endpoint=OTLP_GRPC_ENDPOINT,
            insecure=True,  # Nếu Jaeger không bật TLS (mặc định là không)
        )
        logger.info(f"Configuring OTLP exporter with endpoint: {OTLP_GRPC_ENDPOINT}")
        logger.info(f"Configuring OTLP exporter with endpoint: {OTLP_GRPC_ENDPOINT}")
        tracer.add_span_processor(BatchSpanProcessor(otlp_exporter))

        if log_correlation:
            LoggingInstrumentor().instrument(set_logging_format=True)
        FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
        logger.info("Jaeger instrumentation completed successfully")
    except Exception as e:
        logger.error(f"Failed to set up Jaeger instrumentation: {str(e)}")
        raise


setting_jaeger(app)
tracer = trace.get_tracer(__name__)


@app.get("/health")
async def check_health():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ("jpg", "jpeg", "png"):
            raise HTTPException(status_code=400, detail="Invalid file extension.")

        upload_path = f"/tmp/{datetime.datetime.now().timestamp()}.png"

        # Bắt đầu trace cho toàn bộ quá trình xử lý
        with tracer.start_as_current_span("predict-process") as process_span:
            process_span.set_attribute("file.name", file.filename)
            process_span.set_attribute("file.type", file.content_type)
            process_span.set_attribute("upload.path", upload_path)

            with tracer.start_as_current_span("save-upload-file"):
                with open(upload_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

            with tracer.start_as_current_span("model-inference") as infer_span:
                predicted_value, predicted_accuracy = predict_normal(upload_path)
                infer_span.set_attribute("model.output", predicted_value)
                infer_span.set_attribute("model.confidence", float(predicted_accuracy))

        return {
            "path": upload_path,
            "predicted_value": predicted_value,
            "predicted_accuracy": predicted_accuracy,
        }

    except Exception as e:
        # Tạo trace cho error nếu muốn theo dõi riêng
        with tracer.start_as_current_span("predict-error") as error_span:
            error_span.record_exception(e)
            error_span.set_status(Status(StatusCode.ERROR, str(e)))

        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed.")


@app.post("/predict_test")
async def predict_zeroshot(file: UploadFile = File(...)):
    try:
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ("jpg", "jpeg", "png"):
            raise HTTPException(status_code=400, detail="Invalid file extension.")

        upload_path = f"/tmp/{datetime.datetime.now().timestamp()}.png"

        # Bắt đầu trace cho toàn bộ quá trình xử lý
        with tracer.start_as_current_span("predict-process-zero-shot") as process_span:
            process_span.set_attribute("file.name", file.filename)
            process_span.set_attribute("file.type", file.content_type)
            process_span.set_attribute("upload.path", upload_path)

            # Trace việc lưu file
            with tracer.start_as_current_span("save-upload-file") as save_span:
                save_span.set_attribute("upload_path", upload_path)
                with open(upload_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

            # Trace inference cho zero-shot model
            with tracer.start_as_current_span("run-zero-shot-inference") as infer_span:
                predicted_value, predicted_accuracy = zeroshot(upload_path)
                infer_span.set_attribute("inference.result", predicted_value)
                infer_span.set_attribute(
                    "inference.confidence", float(predicted_accuracy)
                )

            process_span.set_status(Status(StatusCode.OK))

        return {
            "path": upload_path,
            "predicted_value": predicted_value,
            "predicted_accuracy": predicted_accuracy,
        }

    except Exception as e:
        # Tạo trace cho error nếu muốn theo dõi riêng
        with tracer.start_as_current_span("predict-error-zero-shot") as error_span:
            error_span.record_exception(e)
            error_span.set_status(Status(StatusCode.ERROR, str(e)))

        logger.error(f"Zero-shot prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Zero-shot prediction failed.")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True
    )

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import personas
import boto3
import logging

# This MUST be here — without it logger.info() is silently suppressed
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_tables():
    """
    Creates DynamoDB tables on startup if they don't exist.
    Safe to call multiple times — skips tables that already exist.
    """
    client = boto3.client(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.DYNAMODB_ENDPOINT,
    )

    tables = [
        {
            "TableName": "Personas",
            "KeySchema": [
                {"AttributeName": "persona_id", "KeyType": "HASH"}
            ],
            "AttributeDefinitions": [
                {"AttributeName": "persona_id", "AttributeType": "S"}
            ],
            "BillingMode": "PAY_PER_REQUEST",
        },
        {
            "TableName": "Users",
            "KeySchema": [
                {"AttributeName": "user_id", "KeyType": "HASH"}
            ],
            "AttributeDefinitions": [
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            "BillingMode": "PAY_PER_REQUEST",
        },
    ]

    for table_config in tables:
        try:
            client.create_table(**table_config)
            logger.info(f"✓ Created table: {table_config['TableName']}")
        except client.exceptions.ResourceInUseException:
            logger.info(f"→ Table already exists: {table_config['TableName']}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs BEFORE the app starts accepting requests
    logger.info("Starting up — creating DynamoDB tables...")
    create_tables()
    yield
    # Runs AFTER the app shuts down (cleanup goes here)
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

# CORS — allows Next.js frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    personas.router,
    prefix=f"{settings.API_V1_PREFIX}/personas",
    tags=["personas"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
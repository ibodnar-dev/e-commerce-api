from fastapi import FastAPI

from app.api.routes.products import router as products_router

app = FastAPI(
    title="E-Commerce API",
    description="e-commerce REST API",
    version="1.0.0",
)

app.include_router(products_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

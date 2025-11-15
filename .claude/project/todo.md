# Project TODO

## Architecture Improvements
- [ ] Refactor to use `api/v1/routes/` structure for API versioning
  - Move `app/api/routes/` → `app/api/v1/routes/`
  - Create `app/api/v1/__init__.py` with version router: `APIRouter(prefix="/api/v1")`
  - Update main.py to include v1 router
  - Update any imports referencing the old routes path
  - Consider creating `app/api/router.py` to aggregate all API versions
  - Example pattern from real projects: `v1_router.include_router(products_router, prefix="/products")`

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict
import traceback
import os

from input_parser import parse_user_input_flexible
from body_measurements import compute_body_measurements
from llm_service import generate_outfit_pipeline, log_parser_output
from sanzo_wada_colors import get_current_season
from prompts import VALID_BODY_TYPES

app = FastAPI(
    title="AI Fashion Outfit Generator",
    version="4.0.0",
    description="Semantic search-based outfit generation with real product database"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class GenerateOutfitRequest(BaseModel):
    """Request model for outfit generation endpoint."""
    user_message: str = Field(..., description="Natural language style description")
    body_type: str = Field(..., description="Body type from dropdown")
    user_name: str = Field(default="User", description="Optional user name")


class ProductLinks(BaseModel):
    """Product URLs for each outfit piece."""
    top: Optional[str] = None
    pants: Optional[str] = None
    shoe: Optional[str] = None
    layer: Optional[str] = None


class GenerateOutfitResponse(BaseModel):
    """Response model with outfit details and product links."""
    outfit_description: str
    image_url: Optional[str] = None
    styling_tips: str
    measurements: Dict
    user_data: Dict
    season: str
    product_links: ProductLinks
    formatted_response: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint - API status."""
    return {
        "status": "online",
        "version": "4.0.0",
        "model": "GPT-4o-mini + Flux",
        "features": [
            "Semantic style extraction",
            "Real product database",
            "3D mannequin generation",
            "Clothing overlay",
            "Product link integration"
        ],
        "endpoints": ["/generate-outfit", "/health", "/docs"]
    }


@app.get("/health")
async def health_check():

    # Check database connection
    db_status = "not checked"
    try:
        from backend.database import dbconn
        conn, cur = dbconn.connect()
        db_status = "connected"
        dbconn.disconnect(conn, cur)
    except Exception as e:
        db_status = f"error: {str(e)[:50]}"

    return {
        "status": "healthy",
        "model": "gpt-4o-mini",
        "api_keys": {
            "openai": "configured" if os.getenv("OPENAI_API_KEY") else "missing",
            "together": "configured" if os.getenv("TOGETHER_API_KEY") else "⚠missing"
        },
        "database": db_status,
        "current_season": get_current_season()
    }


@app.post("/generate-outfit", response_model=GenerateOutfitResponse)
async def generate_outfit(request: GenerateOutfitRequest):

    #message parsing + check body_type + all fields

    try:
        user_data = parse_user_input_flexible(
            request.user_message,
            fallback_body_type=request.body_type
        )
        user_data["body_type"] = request.body_type

        log_parser_output(request.user_message, user_data)

        if user_data["body_type"] not in VALID_BODY_TYPES:
            raise ValueError(f"Invalid body type '{user_data['body_type']}'")

        required_fields = ["height", "weight", "age", "sex"]
        for field in required_fields:
            if user_data.get(field) is None:
                raise ValueError(f"Missing required field: {field}")

        measurements = compute_body_measurements(
            height=user_data["height"],
            weight=user_data["weight"],
            sex=user_data["sex"]
        )

        result = generate_outfit_pipeline(user_data)

        if not result or "outfit_description" not in result:
            raise ValueError("Outfit generation failed - no description returned")

        season = get_current_season()
        season_name = "Fall/Winter" if season == "FW" else "Spring/Summer"

        # clothing extract
        product_links = result.get('product_links', {})

        return GenerateOutfitResponse(
            outfit_description=result["outfit_description"],
            image_url=result.get("image_url"),
            styling_tips=result.get("styling_tips", ""),
            measurements=measurements,
            user_data=user_data,
            season=season_name,
            product_links=ProductLinks(
                top=product_links.get('top'),
                pants=product_links.get('pants'),
                shoe=product_links.get('shoe'),
                layer=product_links.get('layer')
            ),
            formatted_response=result.get("formatted_response", "")
        )

    except ValueError as e:
        print(f"\nValueError: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail={
                "error": str(e),
                "type": "ValueError",
                "message": "Please check your input data"
            }
        )
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "message": "Internal server error"
            }
        )


@app.get("/test-db")
async def test_database():
    try:
        from backend.database import dbread

        # Test
        filters = {'gender': 'man', 'brand': 'zara', 'style': 'casual'}
        results = dbread.query(filters)

        return {
            "status": "success",
            "filters": filters,
            "results_count": len(results),
            "sample_items": results[:3] if results else []
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "path": str(request.url)}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "type": type(exc).__name__,
            "path": str(request.url)
        }
    )


# =============================================================================
# STARTUP
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("STARTING AI FASHION OUTFIT GENERATOR")
    print("=" * 60)
    print("Features:")
    print("Semantic style extraction")
    print("Real product database queries")
    print("3D mannequin generation")
    print("Clothing overlay rendering")
    print("Product link integration")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
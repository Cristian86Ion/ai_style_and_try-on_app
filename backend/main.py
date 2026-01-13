from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import traceback
import os

from input_parser import parse_user_input_flexible
from body_measurements import compute_body_measurements
from llm_service import generate_outfit_pipeline
from sanzo_wada_colors import get_current_season
from prompts import VALID_BODY_TYPES

app = FastAPI(
    title="AI Fashion Outfit Generator",
    version="1.6.7",
    description="Outfit generation with real products + AI-generated shoes"
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


class OutfitItem(BaseModel):
    """Individual clothing item from database."""
    id: str
    brand: str
    category: str
    colors: List[str]
    price_eur: str
    url: Optional[str] = None
    style: str


class AIShoe(BaseModel):
    description: str
    colors: List[str]
    style: str
    is_ai_generated: bool = True


class ProductLinks(BaseModel):
    """Product URLs for clothing pieces (NO shoes - they're AI generated)."""
    top: Optional[str] = None
    pants: Optional[str] = None
    layer: Optional[str] = None


class SelectedItems(BaseModel):
    """Selected outfit items - clothing from DB, no shoes."""
    top: Optional[Dict[str, Any]] = None
    pants: Optional[Dict[str, Any]] = None
    layer: Optional[Dict[str, Any]] = None


class GenerateOutfitResponse(BaseModel):
    """Response model with outfit details, product links, and AI shoe."""
    outfit_description: str
    image_url: Optional[str] = None
    styling_tips: str
    measurements: Dict
    user_data: Dict
    season: str
    product_links: ProductLinks
    selected_items: Optional[SelectedItems] = None
    ai_shoe: Optional[Dict[str, Any]] = None  # AI generated shoe


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "1.0.0",
        "model": "GPT-5-mini + Flux",
        "features": [
            "Real clothing from database",
            "AI-generated shoes (style-matched)",
            "3D mannequin generation",
            "Clothing overlay rendering",
            "Product link integration (clothing only)"
        ],
        "endpoints": ["/generate-outfit", "/health", "/docs"]
    }


@app.get("/health")
async def health_check():
    """Health check with system status."""
    return {
        "status": "healthy",
        "model": "gpt-5-mini",
        "api_keys": {
            "openai": "configured" if os.getenv("OPENAI_API_KEY") else "missing",
            "together": "configured" if os.getenv("TOGETHER_API_KEY") else "missing"
        },
        "current_season": get_current_season(),
        "shoe_source": "AI Generated"
    }


@app.post("/generate-outfit", response_model=GenerateOutfitResponse)
async def generate_outfit(request: GenerateOutfitRequest):
    """
    Main endpoint: Generate outfit from user input.
    Clothing from real database, shoes AI-generated.
    """

    try:
        # Parse user input
        user_data = parse_user_input_flexible(
            request.user_message,
            fallback_body_type=request.body_type
        )
        user_data["body_type"] = request.body_type

        # Validate body type
        if user_data["body_type"] not in VALID_BODY_TYPES:
            raise ValueError(f"Invalid body type '{user_data['body_type']}'")

        # Validate required fields
        required_fields = ["height", "weight", "age", "sex"]
        for field in required_fields:
            if user_data.get(field) is None:
                raise ValueError(f"Missing required field: {field}")

        # Calculate measurements
        measurements = compute_body_measurements(
            height=user_data["height"],
            weight=user_data["weight"],
            sex=user_data["sex"]
        )

        # Generate outfit through pipeline
        result = generate_outfit_pipeline(user_data)

        if not result or "outfit_description" not in result:
            raise ValueError("Outfit generation failed - no description returned")

        # Get season
        season = get_current_season()
        season_name = "Fall/Winter" if season == "FW" else "Spring/Summer"

        # Extract product links (NO shoes)
        product_links = result.get('product_links', {})

        # Get selected items (NO shoes)
        selected = result.get('selected_items', {})

        # Get AI shoe
        ai_shoe = result.get('ai_shoe')

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
                layer=product_links.get('layer')
            ),
            selected_items=SelectedItems(
                top=selected.get('top'),
                pants=selected.get('pants'),
                layer=selected.get('layer')
            ),
            ai_shoe=ai_shoe
        )

    except ValueError as e:
        print(f"\n❌ ValueError: {e}")
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
        print(f"\n Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "message": "Internal server error"
            }
        )


@app.get("/test-local")
async def test_local_store():
    """Test local JSON store loading."""
    try:
        from local.local_store import load_all_items

        items = load_all_items()

        # Count by category
        categories = {}
        for item in items:
            cat = item.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "status": "success",
            "total_items": len(items),
            "categories": categories,
            "sample_items": items[:3] if items else [],
            "note": "Shoes are AI-generated, not from database"
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
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "path": str(request.url)}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors."""
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
    print("STARTING AI FASHION OUTFIT GENERATOR v5.0")
    print("=" * 60)
    print("Features:")
    print("Real clothing from database (tops, pants, layers)")
    print("AI-generated shoes (style-matched)")
    print("3D mannequin generation")
    print("Clothing overlay rendering")
    print("Product links for real items")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
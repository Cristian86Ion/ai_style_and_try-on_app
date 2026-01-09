from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import traceback
import os

from input_parser import parse_user_input_flexible
from body_measurements import compute_body_measurements
from llm_service import generate_outfit_pipeline
from sanzo_wada_colors import get_two_color_palettes, get_current_season

app = FastAPI(
    title="AI Fashion Outfit Generator",
    description="Generate personalized outfit recommendations with AI",
    version="2.0.0"
)

# CORS middleware - allows frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class GenerateOutfitRequest(BaseModel):
    """Request model for outfit generation"""
    user_message: str = Field(
        ...,
        description="User input in flexible format",
        example="male, 180, 75, 28, 43, athletic, nike-adidas, style: casual sporty"
    )
    body_type: str = Field(
        ...,
        description="Body type from dropdown (slim/athletic/average/muscular/stocky/plus-size)"
    )
    user_name: str = Field(
        default="User",
        description="User name for logging"
    )


class GenerateOutfitResponse(BaseModel):
    """Response model with outfit, image, tips, and measurements"""
    outfit_description: str
    image_url: Optional[str] = None
    styling_tips: str
    alternative_palette: str
    measurements: dict
    user_data: dict
    season: str
    formatted_response: str  # Includes outfit + tips + measurements


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "✅ online",
        "service": "AI Fashion Outfit Generator",
        "version": "2.0.0",
        "endpoints": {
            "generate": "/generate-outfit",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Detailed health check with service status"""

    # Check API keys
    openai_status = "✅ configured" if os.getenv("OPENAI_API_KEY") else "❌ missing"
    together_status = "✅ configured" if os.getenv("TOGETHER_API_KEY") else "⚠️ missing (images disabled)"

    return {
        "status": "healthy",
        "services": {
            "input_parser": "ok",
            "body_measurements": "ok",
            "llm_service": "ok",
            "sanzo_wada_colors": "ok",
            "fit_rules": "ok"
        },
        "api_keys": {
            "openai": openai_status,
            "together": together_status
        },
        "current_season": get_current_season()
    }


@app.post("/generate-outfit", response_model=GenerateOutfitResponse)
async def generate_outfit(request: GenerateOutfitRequest):
    """
    Main endpoint: Generate personalized outfit with AI.

    Flow:
    1. Parse user input (flexible format: "sex, height, weight, age, shoe, body_type, brands, style: description")
    2. Override body_type with dropdown value from ProfileModal
    3. Calculate body measurements using anthropometric formulas
    4. Generate outfit description with GPT-4 (color palette, fit rules, age-appropriate)
    5. Compile Flux prompt and generate outfit visualization (gray humanoid figure)
    6. Generate styling tips with alternative color palette
    7. Return complete response with measurements
    """

    try:
        # =================================================================
        # STEP 1: Parse and validate user input
        # =================================================================
        print(f"\n{'=' * 70}")
        print(f"🔥 NEW REQUEST from: {request.user_name}")
        print(f"{'=' * 70}")
        print(f"📝 Input: {request.user_message[:100]}...")
        print(f"🏷️  Body type (dropdown): {request.body_type}")

        # Use flexible parser with body_type as fallback
        user_data = parse_user_input_flexible(
            request.user_message,
            fallback_body_type=request.body_type
        )

        # CRITICAL: Override with dropdown selection
        user_data['body_type'] = request.body_type

        print(f"\n✅ PARSED DATA:")
        print(f"   Sex: {user_data['sex'].upper()}")
        print(f"   Height: {user_data['height']}cm")
        print(f"   Weight: {user_data['weight']}kg")
        print(f"   Age: {user_data['age']}yo")
        print(f"   Shoe: EU {user_data['shoe_size']}")
        print(f"   Body Type: {user_data['body_type']}")
        print(f"   Style: {user_data['style_description'][:60]}...")
        print(f"   Brands: {', '.join(user_data.get('favorite_brands', ['None']))}")

        # Validate body type
        valid_body_types = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]
        if user_data['body_type'] not in valid_body_types:
            raise ValueError(
                f"Invalid body type '{user_data['body_type']}'. "
                f"Must be one of: {', '.join(valid_body_types)}"
            )

        # =================================================================
        # STEP 2: Calculate body measurements
        # =================================================================
        print(f"\n{'=' * 70}")
        print(f"📏 CALCULATING BODY MEASUREMENTS")
        print(f"{'=' * 70}")

        try:
            measurements = compute_body_measurements(
                height=user_data['height'],
                weight=user_data['weight'],
                sex=user_data['sex']
            )

            print(f"\n✅ MEASUREMENTS CALCULATED:")
            print(f"   Chest: {measurements['chest_circumference']}cm")
            print(f"   Waist: {measurements['waist_circumference']}cm")
            print(f"   Hips: {measurements['hip_circumference']}cm")
            print(f"   Leg Length: {measurements['leg_length']}cm")
            print(f"   Arm Length: {measurements['arm_length']}cm")
            print(f"   Shoulder/Hip Ratio: {measurements['shoulder_hip_ratio']}")
            print(f"   BMI: {measurements['bmi']}")

        except Exception as e:
            print(f"\n❌ ERROR calculating measurements: {e}")
            traceback.print_exc()
            raise HTTPException(
                status_code=400,
                detail=f"Failed to calculate body measurements: {str(e)}"
            )

        # =================================================================
        # STEP 3: Generate outfit pipeline (GPT + Flux + Tips)
        # =================================================================
        print(f"\n{'=' * 70}")
        print(f"🎨 GENERATING OUTFIT WITH AI")
        print(f"{'=' * 70}")

        try:
            result = generate_outfit_pipeline(user_data)

            if not result or "outfit_description" not in result:
                raise ValueError("Outfit generation returned invalid result")

            print(f"\n✅ OUTFIT GENERATION COMPLETE:")
            print(f"   Description: {result['outfit_description'][:100]}...")
            print(f"   Image: {'✅ Generated' if result.get('image_url') else '⚠️  Skipped'}")
            print(f"   Tips: {result['styling_tips'][:60]}...")

        except Exception as e:
            print(f"\n❌ ERROR in outfit generation pipeline: {e}")
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate outfit: {str(e)}"
            )

        # =================================================================
        # STEP 4: Get alternative color palette
        # =================================================================
        print(f"\n{'=' * 70}")
        print(f"🎨 GENERATING ALTERNATIVE PALETTE")
        print(f"{'=' * 70}")

        try:
            style_keywords = user_data.get("style_description", "").lower().split()[:5]
            _, alternative_palette = get_two_color_palettes(style_keywords)

            # Format without hex codes (color names only)
            alt_colors = alternative_palette.get("colors", [])
            color_names = [
                color.split(" (#")[0] if " (#" in color else color
                for color in alt_colors
            ]
            alternative_palette_str = (
                f"{alternative_palette.get('name', 'Alternative Palette')}: "
                f"{', '.join(color_names[:3])}"
            )

            print(f"✅ Alternative Palette: {alternative_palette_str}")

        except Exception as e:
            print(f"⚠️  Error getting alternative palette: {e}")
            alternative_palette_str = "Neutral Palette: Gray, White, Black"

        # =================================================================
        # STEP 5: Prepare final response
        # =================================================================
        print(f"\n{'=' * 70}")
        print(f"📦 PREPARING RESPONSE")
        print(f"{'=' * 70}")

        # Get formatted response (includes measurements)
        formatted_response = result.get("formatted_response", "")

        # Get current season
        season = get_current_season()
        season_name = "Fall/Winter" if season == "FW" else "Spring/Summer"

        print(f"\n✅ RESPONSE READY")
        print(f"   Season: {season_name}")
        print(f"   Formatted: {'✅' if formatted_response else '❌'}")
        print(f"{'=' * 70}\n")

        # =================================================================
        # STEP 6: Return complete response
        # =================================================================
        return GenerateOutfitResponse(
            outfit_description=result["outfit_description"],
            image_url=result.get("image_url"),
            styling_tips=result["styling_tips"],
            alternative_palette=alternative_palette_str,
            measurements=result["measurements"],
            user_data=user_data,
            season=season_name,
            formatted_response=formatted_response
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise

    except ValueError as e:
        # Handle validation errors
        print(f"\n❌ VALIDATION ERROR:")
        print(f"   {str(e)}")
        traceback.print_exc()

        raise HTTPException(
            status_code=400,
            detail={
                "error": str(e),
                "type": "ValidationError",
                "message": "Invalid input data provided. Check your format."
            }
        )

    except Exception as e:
        # Handle all other unexpected errors
        print(f"\n❌ UNEXPECTED ERROR:")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "message": "An unexpected error occurred. Check server logs for details."
            }
        )


# =============================================================================
# STARTUP & SHUTDOWN EVENTS
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Print startup message with configuration info"""

    print("\n" + "=" * 70)
    print("👔 AI FASHION OUTFIT GENERATOR - Backend Server v2.0")
    print("=" * 70)
    print(f"\n✅ Server running on http://127.0.0.1:8000")
    print(f"📚 API docs: http://127.0.0.1:8000/docs")
    print(f"🔍 Health check: http://127.0.0.1:8000/health")

    # Check environment variables
    print("\n🔑 ENVIRONMENT CHECK:")
    openai_key = os.getenv("OPENAI_API_KEY")
    together_key = os.getenv("TOGETHER_API_KEY")

    if openai_key:
        print(f"   ✅ OPENAI_API_KEY: Set ({openai_key[:8]}...{openai_key[-4:]})")
    else:
        print(f"   ❌ OPENAI_API_KEY: NOT SET - Outfit generation will fail!")
        print(f"      → Add OPENAI_API_KEY to your .env file")

    if together_key:
        print(f"   ✅ TOGETHER_API_KEY: Set ({together_key[:8]}...{together_key[-4:]})")
    else:
        print(f"   ⚠️  TOGETHER_API_KEY: NOT SET - Image generation disabled")
        print(f"      → Add TOGETHER_API_KEY to .env for image generation")

    # Current season
    season = get_current_season()
    season_name = "Fall/Winter (Sep-Feb)" if season == "FW" else "Spring/Summer (Mar-Aug)"
    print(f"\n🌍 CURRENT SEASON: {season_name}")

    print("\n📋 REQUIRED .env FILE:")
    print("   OPENAI_API_KEY=sk-...")
    print("   TOGETHER_API_KEY=... (optional)")

    print(f"\n🚀 Ready to generate outfits!")
    print(f"👋 Press CTRL+C to stop")
    print("=" * 70 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\n" + "=" * 70)
    print("👋 Server shutting down...")
    print("=" * 70 + "\n")


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return {
        "error": "Not Found",
        "message": f"The endpoint {request.url.path} does not exist",
        "available_endpoints": {
            "root": "/",
            "health": "/health",
            "generate": "/generate-outfit (POST)",
            "docs": "/docs"
        }
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    print(f"\n❌ INTERNAL SERVER ERROR:")
    print(f"   Path: {request.url.path}")
    print(f"   Error: {str(exc)}")
    traceback.print_exc()

    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred. Check server logs for details.",
        "type": type(exc).__name__,
        "path": request.url.path
    }


# =============================================================================
# ADDITIONAL UTILITY ENDPOINTS
# =============================================================================

@app.get("/valid-body-types")
async def get_valid_body_types():
    """Get list of valid body types for frontend dropdown"""
    return {
        "body_types": [
            {"value": "slim", "label": "Slim", "description": "Lean build, minimal body fat"},
            {"value": "athletic", "label": "Athletic", "description": "Toned, moderate muscle definition"},
            {"value": "average", "label": "Average", "description": "Balanced proportions"},
            {"value": "muscular", "label": "Muscular", "description": "Heavily developed muscles"},
            {"value": "stocky", "label": "Stocky", "description": "Solid, compact build"},
            {"value": "plus-size", "label": "Plus Size", "description": "Fuller figure with curves"}
        ]
    }


@app.get("/current-season")
async def get_season_info():
    """Get current fashion season information"""
    season = get_current_season()

    if season == "FW":
        return {
            "season": "FW",
            "name": "Fall/Winter",
            "months": "September - February",
            "description": "Layering season with coats, sweaters, boots",
            "fabrics": ["wool", "cashmere", "leather", "denim"],
            "outerwear": "Required"
        }
    else:
        return {
            "season": "SS",
            "name": "Spring/Summer",
            "months": "March - August",
            "description": "Light, breathable fabrics and minimal layering",
            "fabrics": ["linen", "cotton", "silk", "chambray"],
            "outerwear": "Optional"
        }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True  # Auto-reload on code changes during development
    )
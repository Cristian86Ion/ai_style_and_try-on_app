from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import traceback
import sys

from input_parser import parse_user_input_flexible
from body_measurements import compute_body_measurements
from llm_service import generate_outfit_pipeline
from sanzo_wada_colors import get_two_color_palettes, format_color_palette_for_prompt

app = FastAPI(
    title="AI Fashion Outfit Generator",
    description="Generate personalized outfit recommendations with AI",
    version="1.0.0"
)

# CORS middleware - CRITICAL for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["http://localhost:3000", "https://yourdomain.com"]
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
        description="User input (flexible format)",
        example="male, 180, 70, 30, 43, athletic, nike, style: relaxed sporty"
    )
    body_type: str = Field(..., description="Body type from ProfileModal")
    user_name: str = Field(..., description="User name from ProfileModal")


class GenerateOutfitResponse(BaseModel):
    """Response model with outfit, image, and tips"""
    outfit_description: str
    image_url: Optional[str] = None
    styling_tips: str
    alternative_palette: str
    measurements: dict
    user_data: dict
    season: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "✅ online",
        "service": "AI Fashion Outfit Generator",
        "version": "1.0.0",
        "endpoints": ["/generate-outfit", "/health"]
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "input_parser": "ok",
            "body_measurements": "ok",
            "llm_service": "ok",
            "sanzo_wada": "ok",
            "fit_rules": "ok"
        }
    }


@app.post("/generate-outfit", response_model=GenerateOutfitResponse)
async def generate_outfit(request: GenerateOutfitRequest):
    """
    Main endpoint: Generate outfit with image and tips.

    Flow:
    1. Parse user input (flexible format)
    2. Override body_type with ProfileModal value
    3. Calculate body measurements
    4. Generate outfit description (GPT-4)
    5. Generate outfit image (Flux.1)
    6. Generate styling tips (50 words max, COLOR NAMES ONLY)
    7. Return alternative color palette suggestion
    """

    try:
        # =====================================================================
        # STEP 1: Parse user input (flexible)
        # =====================================================================
        print(f"\n{'=' * 60}")
        print(f"🔥 New request from: {request.user_name}")
        print(f"   Body type: {request.body_type}")
        print(f"   Message: {request.user_message[:80]}...")

        # Use flexible parser with body_type from ProfileModal as fallback
        user_data = parse_user_input_flexible(
            request.user_message,
            fallback_body_type=request.body_type
        )

        # CRITICAL: Override body_type with ProfileModal value
        user_data['body_type'] = request.body_type

        print(f"✅ Parsed: SEX={user_data['sex'].upper()}, {user_data['height']}cm, "
              f"{user_data['weight']}kg, {user_data['body_type']}")
        print(f"   First word of message: '{request.user_message.split(',')[0].strip()}'")

        # Validate body type
        valid_body_types = ["slim", "athletic", "average", "muscular", "stocky", "plus-size"]
        if user_data['body_type'] not in valid_body_types:
            raise ValueError(
                f"Invalid body type: {user_data['body_type']}. Must be one of: {', '.join(valid_body_types)}")

        # =====================================================================
        # STEP 2: Calculate body measurements
        # =====================================================================
        print(f"📏 Calculating body measurements...")

        try:
            measurements = compute_body_measurements(
                height=user_data['height'],
                weight=user_data['weight'],
                sex=user_data['sex']
            )
            print(f"✅ Measurements: chest={measurements['chest_circumference']}cm, "
                  f"waist={measurements['waist_circumference']}cm, "
                  f"hips={measurements['hip_circumference']}cm")
        except Exception as e:
            print(f"❌ Error calculating measurements: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to calculate body measurements: {str(e)}"
            )

        # =====================================================================
        # STEP 3: Generate outfit pipeline (GPT + Flux + Tips)
        # =====================================================================
        print(f"🎨 Generating outfit with AI...")

        try:
            result = generate_outfit_pipeline(user_data, measurements)

            if not result or "outfit_description" not in result:
                raise ValueError("Outfit generation returned invalid result")

            print(f"✅ Outfit generated successfully")

            if result.get("image_url"):
                print(f"✅ Image: {result['image_url'][:50]}...")
            else:
                print(f"⚠️ Image generation failed or skipped")

        except Exception as e:
            print(f"❌ Error in outfit generation pipeline: {e}")
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate outfit: {str(e)}"
            )

        # =====================================================================
        # STEP 4: Get alternative color palette (for tips)
        # =====================================================================
        try:
            style_keywords = user_data.get("style_description", "").lower().split()[:5]
            _, alternative_palette = get_two_color_palettes(style_keywords)

            # Format without hex codes (color names only)
            alt_colors = alternative_palette.get("colors", [])
            color_names = [color.split(" (#")[0] if " (#" in color else color for color in alt_colors]
            alternative_palette_str = f"{alternative_palette.get('name', 'Alternative Palette')}: {', '.join(color_names[:3])}"

            print(f"✅ Alternative palette: {alternative_palette_str}")
        except Exception as e:
            print(f"⚠️ Error getting alternative palette: {e}")
            alternative_palette_str = "Neutral Palette: Gray, White, Black"

        print(f"{'=' * 60}\n")

        # =====================================================================
        # STEP 5: Return response
        # =====================================================================
        return GenerateOutfitResponse(
            outfit_description=result["outfit_description"],
            image_url=result.get("image_url"),
            styling_tips=result["styling_tips"],
            alternative_palette=alternative_palette_str,
            measurements=measurements,
            user_data=user_data,
            season=alternative_palette.get("season", "N/A")
        )

    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise

    except ValueError as e:
        # Handle validation errors
        print(f"\n❌ Validation Error:")
        print(f"   {str(e)}")
        traceback.print_exc()

        raise HTTPException(
            status_code=400,
            detail={
                "error": str(e),
                "type": "ValidationError",
                "message": "Invalid input data provided."
            }
        )

    except Exception as e:
        # Handle all other errors
        print(f"\n❌ Unexpected Error in generate_outfit:")
        print(f"   {str(e)}")
        print(f"   Type: {type(e).__name__}")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "message": "An unexpected error occurred while generating the outfit. Please check server logs for details."
            }
        )


# =============================================================================
# STARTUP MESSAGE
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Print startup message with configuration info"""
    import os

    print("\n" + "=" * 60)
    print("🎨 AI FASHION OUTFIT GENERATOR - Backend Server")
    print("=" * 60)
    print(f"\n✅ Server running on http://127.0.0.1:8000")
    print(f"📚 API docs: http://127.0.0.1:8000/docs")
    print(f"🔍 Health check: http://127.0.0.1:8000/health")

    # Check environment variables
    print("\n🔑 Environment Check:")
    openai_key = os.getenv("OPENAI_API_KEY")
    together_key = os.getenv("TOGETHER_API_KEY")

    if openai_key:
        print(f"   ✅ OPENAI_API_KEY: Set ({openai_key[:8]}...)")
    else:
        print(f"   ❌ OPENAI_API_KEY: NOT SET - Outfit generation will fail!")

    if together_key:
        print(f"   ✅ TOGETHER_API_KEY: Set ({together_key[:8]}...)")
    else:
        print(f"   ⚠️  TOGETHER_API_KEY: NOT SET - Image generation disabled")

    print("\n⚠️  Make sure your .env file contains:")
    print("   - OPENAI_API_KEY (required)")
    print("   - TOGETHER_API_KEY (optional, for images)")
    print("\n📝 Press CTRL+C to stop\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\n" + "=" * 60)
    print("👋 Server shutting down...")
    print("=" * 60 + "\n")


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return {
        "error": "Not Found",
        "message": f"The endpoint {request.url.path} does not exist",
        "available_endpoints": ["/", "/health", "/generate-outfit"]
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    print(f"\n❌ Internal Server Error:")
    print(f"   {str(exc)}")
    traceback.print_exc()

    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred. Check server logs for details.",
        "type": type(exc).__name__
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
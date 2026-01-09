from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import traceback
import os

from input_parser import parse_user_input_flexible
from body_measurements import compute_body_measurements
from llm_service import generate_outfit_pipeline, log_parser_output
from sanzo_wada_colors import get_two_color_palettes, get_current_season
from prompts import VALID_BODY_TYPES

app = FastAPI(title="AI Fashion Outfit Generator", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Pydantic models
# ==========================================
class GenerateOutfitRequest(BaseModel):
    user_message: str = Field(..., description="Flexible user input")
    body_type: str = Field(..., description="Dropdown body type override")
    user_name: str = Field(default="User")


class GenerateOutfitResponse(BaseModel):
    outfit_description: str
    image_url: Optional[str] = None
    styling_tips: str
    alternative_palette: str
    measurements: dict
    user_data: dict
    season: str
    formatted_response: str


# ==========================================
# Endpoints
# ==========================================
@app.get("/")
async def root():
    return {
        "status": "✅ online",
        "version": "3.0.0",
        "model": "GPT-5-mini",
        "endpoints": ["/generate-outfit", "/health", "/docs"]
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "gpt-5-mini",
        "api_keys": {
            "openai": "✅ configured" if os.getenv("OPENAI_API_KEY") else "❌ missing",
            "together": "✅ configured" if os.getenv("TOGETHER_API_KEY") else "⚠️ missing"
        },
        "current_season": get_current_season()
    }


@app.post("/generate-outfit", response_model=GenerateOutfitResponse)
async def generate_outfit(request: GenerateOutfitRequest):
    try:
        # Parse user input
        user_data = parse_user_input_flexible(
            request.user_message,
            fallback_body_type=request.body_type
        )
        user_data["body_type"] = request.body_type

        # Show parser output in terminal
        log_parser_output(request.user_message, user_data)

        # Validate body type
        if user_data["body_type"] not in VALID_BODY_TYPES:
            raise ValueError(f"Invalid body type '{user_data['body_type']}'")

        # Validate required fields
        required_fields = ["height", "weight", "age"]
        for field in required_fields:
            if user_data.get(field) is None:
                raise ValueError(f"Missing required field: {field}")

        # Calculate measurements
        measurements = compute_body_measurements(
            height=user_data["height"],
            weight=user_data["weight"],
            sex=user_data["sex"]
        )

        # Generate outfit
        result = generate_outfit_pipeline(user_data)

        if not result or "outfit_description" not in result:
            raise ValueError("Outfit generation failed - no description returned")

        # Get alternative palette
        style_keywords = user_data.get("style_description", "").lower().split()[:5]
        _, alternative_palette = get_two_color_palettes(style_keywords)
        alt_colors = alternative_palette.get("colors", [])
        color_names = [c.split(" (#")[0] if " (#" in c else c for c in alt_colors]
        alternative_palette_str = f"{alternative_palette.get('name', 'Alternative')}: {', '.join(color_names[:3])}"

        # Get season
        season = get_current_season()
        season_name = "Fall/Winter" if season == "FW" else "Spring/Summer"

        return GenerateOutfitResponse(
            outfit_description=result["outfit_description"],
            image_url=result.get("image_url"),
            styling_tips=result.get("styling_tips", ""),
            alternative_palette=alternative_palette_str,
            measurements=measurements,
            user_data=user_data,
            season=season_name,
            formatted_response=result.get("formatted_response", "")
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
        print(f"\n❌ Unexpected Error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "message": "Internal server error"
            }
        )


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
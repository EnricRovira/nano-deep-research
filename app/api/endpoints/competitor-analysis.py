from fastapi import APIRouter
from fastapi import APIRouter, Request, HTTPException, Depends
import logging

from app.api.v1.responses.api_error import (
    APIError, 
    ValidationError, 
    ServiceError, 
    ContentModerationError
)

from app.api.v1.requests import CompetitorAnalysisRequest
from app.api.v1.responses.responses import CompetitorAnalysisResponse
from app.api.services.manager import ResearchManager

competitor_analysis_router = APIRouter(prefix="/competitor-analysis")

dict_response_codes: dict[int|str, dict] = {
    400: {"model": APIError, "description": "Invalid parameters in the request",},
    401: {"model": APIError, "description": "Unauthorized",},
    403: {"model": APIError, "description": "Content Moderation system",},
    413: {"model": APIError, "description": "Image is larger than 10Mib",},
    500: {"model": APIError, "description": "Internal server error",},
}


##############################
#                            #
#                            #
#   Generate Recommendations #
#                            #
#                            #
##############################
@competitor_analysis_router.post(
    "/generate-competitor-analysis",
    response_model=CompetitorAnalysisResponse,
    tags=["Competitor Analysis"],
    summary="Generate competitor analysis",
    description="Returns competitor analysis",
    responses=dict_response_codes,
)
async def api_generate_competitor_analysis(
    request: Request,
    content: CompetitorAnalysisRequest,
) -> CompetitorAnalysisResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    logging.info(f"Request ID: {request_id} - Generating competitor analysis")
    
    try:
        # Initialize agent
        manager = ResearchManager()
        
        # Generate competitor analysis
        result = await manager.run(content.query)
        
        # Check result
        if not result:
            raise ServiceError(
                detail="Failed to generate recommendations",
                error_code="GENERATION_FAILED"
            )
            
        logging.info(f"Request ID: {request_id} - Successfully generated recommendations")
        return result
        
    except ValidationError:
        # Re-raise validation errors
        raise
    except ContentModerationError:
        # Re-raise content moderation errors
        raise
    except ServiceError:
        # Re-raise service errors
        raise
    except Exception as e:
        logging.error(f"Request ID: {request_id} - Error generating recommendations: {str(e)}", exc_info=True)
        raise ServiceError(
            detail="Failed to generate recommendations",
            error_code="GENERATION_ERROR",
            additional_info={"error": str(e)}
        )



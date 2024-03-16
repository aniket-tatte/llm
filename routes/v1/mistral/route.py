from fastapi import APIRouter, Depends, Request
from fastapi.security.api_key import APIKey
from auth.main import get_api_key
from utils.rate_limit import limiter
from service.ollama.service import getCompletionResponse

router = APIRouter()

@router.get("/completion")
@limiter.limit("5 per minute", key_func=lambda request: request.headers.get("access_token"))
async def completion(request: Request, api_key: APIKey = Depends(get_api_key)):
    response = getCompletionResponse(
        prompt = ''
    )
    return {"message": "This is the completion endpoint for Mistral in version 1"}

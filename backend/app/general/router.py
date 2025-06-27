# backend/app/general/router.py
from fastapi import APIRouter, Depends, HTTPException
from .schemas import PromptRequest, PromptResponse
from .service import GeneralPurposeService, general_service

router = APIRouter(
    prefix="/general",
    tags=["General Purpose AI"]
)

@router.post("/prompt", response_model=PromptResponse)
async def handle_general_prompt(
    request: PromptRequest,
    service: GeneralPurposeService = Depends(lambda: general_service)
):
    try:
        answer = service.get_llm_response(request.prompt)
        return PromptResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
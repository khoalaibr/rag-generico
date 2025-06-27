# backend/app/rag/router.py
from fastapi import APIRouter, Depends, HTTPException
from .schemas import QueryRequest, QueryResponse
from .service import RAGService, rag_service

router = APIRouter(
    prefix="/rag",
    tags=["RAG Query"]
)

@router.post("/query", response_model=QueryResponse)
async def query_rag(
    request: QueryRequest,
    service: RAGService = Depends(lambda: rag_service)
):
    try:
        answer = service.answer_query(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
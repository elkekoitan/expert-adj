"""
Expert Advisor endpoints
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List

router = APIRouter()


@router.post("/upload")
async def upload_ea(file: UploadFile = File(...)):
    """
    Upload Expert Advisor file
    """
    # Validate file extension
    allowed_extensions = [".ex4", ".ex5", ".mq4", ".mq5"]
    file_ext = f".{file.filename.split('.')[-1]}" if '.' in file.filename else ""

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"
        )

    return {
        "message": "EA upload successful",
        "filename": file.filename,
        "size": file.size,
        "status": "processing"
    }


@router.get("/")
async def list_eas():
    """
    List all Expert Advisors
    """
    return {
        "eas": [],
        "total": 0
    }


@router.get("/{ea_id}")
async def get_ea(ea_id: str):
    """
    Get Expert Advisor details
    """
    return {
        "id": ea_id,
        "name": "Sample EA",
        "status": "TBD"
    }


@router.delete("/{ea_id}")
async def delete_ea(ea_id: str):
    """
    Delete Expert Advisor
    """
    return {"message": f"EA {ea_id} deleted"}


@router.get("/{ea_id}/parameters")
async def get_ea_parameters(ea_id: str):
    """
    Get EA parameters schema
    """
    return {
        "ea_id": ea_id,
        "parameters": []
    }

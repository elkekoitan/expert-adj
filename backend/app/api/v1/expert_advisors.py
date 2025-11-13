"""
Expert Advisor endpoints
"""

import hashlib
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from uuid import UUID, uuid4

from app.core.database import get_db
from app.services.ea_analyzer import analyze_ea_file
from app.services.ea_service import EAService
from app.services.s3 import S3Service, get_s3_service
from app.utils.mql_parser import extract_parameters_from_mql, generate_parameter_summary
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/upload")
async def upload_ea(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    description: Optional[str] = None,
    version: str = "1.0",
    db: AsyncSession = Depends(get_db),
    s3_service: S3Service = Depends(get_s3_service),
    # current_user = Depends(get_current_user)
):
    """
    Upload Expert Advisor file and extract parameters

    Supports:
    - .mq4, .mq5 (source files - extracts parameters)
    - .ex4, .ex5 (compiled files - stores only)

    Returns:
    - EA metadata
    - Extracted parameters (for source files)
    - Upload status
    """
    # Validate file extension
    allowed_extensions = [".ex4", ".ex5", ".mq4", ".mq5"]
    file_ext = f".{file.filename.split('.')[-1]}" if "." in file.filename else ""

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}",
        )

    # Determine platform and if source is present
    platform = "MT4" if file_ext in [".ex4", ".mq4"] else "MT5"
    is_source = file_ext in [".mq4", ".mq5"]

    # Read file content
    content = await file.read()

    # Calculate file hash
    file_hash = hashlib.sha256(content).hexdigest()

    # Extract parameters if source file
    parameters = []
    parameter_summary = {}

    if is_source:
        try:
            content_str = content.decode("utf-8", errors="ignore")
            parameters = extract_parameters_from_mql(content_str)
            parameter_summary = generate_parameter_summary(parameters)
        except Exception as e:
            # If parsing fails, log but don't fail upload
            print(f"Parameter extraction failed: {str(e)}")
            parameter_summary = {"error": str(e)}

    # TODO: Save to database (ExpertAdvisor, EAVersion, EAParameter)
    # TODO: Upload file to MinIO/S3

    ea_name = name or file.filename.rsplit(".", 1)[0]

    return {
        "message": "EA upload successful",
        "ea": {
            "name": ea_name,
            "description": description,
            "platform": platform,
            "filename": file.filename,
            "file_size": len(content),
            "file_hash": file_hash,
            "has_source": is_source,
        },
        "parameters": {
            "extracted": len(parameters),
            "summary": parameter_summary,
            "details": parameters[:10]
            if len(parameters) > 10
            else parameters,  # Return first 10
        },
        "status": "success",
    }


@router.get("/")
async def list_eas():
    """
    List all Expert Advisors
    """
    return {"eas": [], "total": 0}


@router.get("/{ea_id}")
async def get_ea(ea_id: str):
    """
    Get Expert Advisor details
    """
    return {"id": ea_id, "name": "Sample EA", "status": "TBD"}


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
    return {"ea_id": ea_id, "parameters": []}


@router.post("/analyze")
async def analyze_ea(
    file: UploadFile = File(...),
):
    """
    Analyze Expert Advisor file (compiled .ex4/.ex5 or source .mq4/.mq5)

    Returns:
    - Metadata (name, version, platform)
    - Detected parameters
    - Trading logic analysis
    - Risk assessment
    - Optimization recommendations
    """
    # Validate file extension
    allowed_extensions = [".ex4", ".ex5", ".mq4", ".mq5"]
    file_ext = f".{file.filename.split('.')[-1]}" if "." in file.filename else ""

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}",
        )

    # Read file content
    content = await file.read()

    # Save to temporary file for analysis
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        # Analyze the EA
        analysis_results = analyze_ea_file(temp_path)

        # Add filename to results
        analysis_results["filename"] = file.filename
        analysis_results["file_size"] = len(content)

        return analysis_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Clean up temporary file
        try:
            Path(temp_path).unlink()
        except Exception:
            pass

"""
Expert Advisor Service Layer
Handles EA CRUD operations and business logic
"""

import hashlib
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expert_advisor import Dependency, EAParameter, EAVersion, ExpertAdvisor
from app.models.user import Organization, User
from app.services.s3 import S3Service
from app.utils.mql_parser import extract_parameters_from_mql, generate_parameter_summary

logger = logging.getLogger(__name__)


class EAService:
    """Expert Advisor service for business logic"""

    def __init__(self, db: AsyncSession, s3_service: S3Service):
        self.db = db
        self.s3 = s3_service

    async def create_ea(
        self,
        name: str,
        owner_id: UUID,
        platform: str,
        description: Optional[str] = None,
        organization_id: Optional[UUID] = None,
        tags: List[str] = None,
    ) -> ExpertAdvisor:
        """
        Create a new Expert Advisor record

        Args:
            name: EA name
            owner_id: User ID who owns this EA
            platform: MT4 or MT5
            description: Optional description
            organization_id: Optional organization ID
            tags: Optional tags list

        Returns:
            Created ExpertAdvisor object
        """
        ea = ExpertAdvisor(
            name=name,
            owner_id=owner_id,
            platform=platform,
            description=description,
            organization_id=organization_id,
            tags=tags or [],
        )

        self.db.add(ea)
        await self.db.commit()
        await self.db.refresh(ea)

        logger.info(f"Created EA: {ea.id} - {ea.name}")
        return ea

    async def upload_ea_file(
        self,
        file: UploadFile,
        owner_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        organization_id: Optional[UUID] = None,
        version: str = "1.0",
    ) -> Dict[str, Any]:
        """
        Upload EA file and extract parameters

        Args:
            file: Uploaded file
            owner_id: User ID
            name: EA name (uses filename if not provided)
            description: Optional description
            organization_id: Optional organization ID
            version: Version string

        Returns:
            Dictionary with EA info, parameters, and upload status
        """
        # Validate file extension
        filename = file.filename
        file_ext = f".{filename.split('.')[-1]}" if "." in filename else ""

        if file_ext not in [".ex4", ".ex5", ".mq4", ".mq5"]:
            raise ValueError(f"Invalid file extension: {file_ext}")

        # Determine platform and source presence
        platform = "MT4" if file_ext in [".ex4", ".mq4"] else "MT5"
        is_source = file_ext in [".mq4", ".mq5"]

        # Read file content
        content = await file.read()
        file_hash = hashlib.sha256(content).hexdigest()

        # Create EA record
        ea_name = name or filename.rsplit(".", 1)[0]
        ea = await self.create_ea(
            name=ea_name,
            owner_id=owner_id,
            platform=platform,
            description=description,
            organization_id=organization_id,
        )

        # Upload to S3
        file_type = "source" if is_source else "compiled"
        s3_key = self.s3.upload_ea_file(
            file_content=content,
            ea_id=str(ea.id),
            version=version,
            filename=filename,
            file_type=file_type,
        )

        if not s3_key:
            raise Exception("Failed to upload file to S3")

        # Create EA version
        ea_version = EAVersion(
            ea_id=ea.id,
            version=version,
            build_hash=file_hash,
            compiled_file_path=s3_key if not is_source else None,
            source_file_path=s3_key if is_source else None,
            source_present=is_source,
            compiled_at=datetime.utcnow().isoformat(),
        )

        self.db.add(ea_version)
        await self.db.commit()
        await self.db.refresh(ea_version)

        # Extract parameters if source file
        parameters = []
        parameter_summary = {}

        if is_source:
            try:
                content_str = content.decode("utf-8", errors="ignore")
                parameters = extract_parameters_from_mql(content_str)
                parameter_summary = generate_parameter_summary(parameters)

                # Save parameters to database
                for param in parameters:
                    db_param = EAParameter(
                        ea_version_id=ea_version.id,
                        name=param["name"],
                        parameter_type=param["parameter_type"],
                        default_value=param["default_value"],
                        description=param["description"],
                        min_value=param.get("min_value"),
                        max_value=param.get("max_value"),
                        step_value=param.get("step_value"),
                        enum_values=param.get("enum_values", []),
                        is_optimizable=param["is_optimizable"],
                    )
                    self.db.add(db_param)

                await self.db.commit()

            except Exception as e:
                logger.error(f"Parameter extraction failed: {e}")
                parameter_summary = {"error": str(e)}

        return {
            "ea": {
                "id": str(ea.id),
                "name": ea.name,
                "description": ea.description,
                "platform": ea.platform,
                "filename": filename,
                "file_size": len(content),
                "file_hash": file_hash,
                "has_source": is_source,
            },
            "version": {
                "id": str(ea_version.id),
                "version": ea_version.version,
                "build_hash": ea_version.build_hash,
            },
            "parameters": {
                "extracted": len(parameters),
                "summary": parameter_summary,
                "details": parameters[:20],  # Return first 20
            },
            "storage": {"s3_key": s3_key, "bucket": self.s3.bucket_name},
            "status": "success",
        }

    async def get_ea_by_id(self, ea_id: UUID) -> Optional[ExpertAdvisor]:
        """Get EA by ID"""
        result = await self.db.execute(
            select(ExpertAdvisor).where(ExpertAdvisor.id == ea_id)
        )
        return result.scalar_one_or_none()

    async def list_eas(
        self,
        owner_id: Optional[UUID] = None,
        organization_id: Optional[UUID] = None,
        platform: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ExpertAdvisor]:
        """List EAs with filters"""
        query = select(ExpertAdvisor).where(ExpertAdvisor.is_active == True)

        if owner_id:
            query = query.where(ExpertAdvisor.owner_id == owner_id)

        if organization_id:
            query = query.where(ExpertAdvisor.organization_id == organization_id)

        if platform:
            query = query.where(ExpertAdvisor.platform == platform)

        # TODO: Filter by tags (JSONB contains)

        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_ea_parameters(self, ea_version_id: UUID) -> List[EAParameter]:
        """Get all parameters for an EA version"""
        result = await self.db.execute(
            select(EAParameter).where(EAParameter.ea_version_id == ea_version_id)
        )
        return result.scalars().all()

    async def get_latest_version(self, ea_id: UUID) -> Optional[EAVersion]:
        """Get latest version of an EA"""
        result = await self.db.execute(
            select(EAVersion)
            .where(EAVersion.ea_id == ea_id)
            .order_by(EAVersion.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def download_ea_file(
        self, ea_version_id: UUID, file_type: str = "compiled"
    ) -> Optional[bytes]:
        """
        Download EA file from S3

        Args:
            ea_version_id: EA version ID
            file_type: 'compiled' or 'source'

        Returns:
            File content as bytes
        """
        result = await self.db.execute(
            select(EAVersion).where(EAVersion.id == ea_version_id)
        )
        ea_version = result.scalar_one_or_none()

        if not ea_version:
            return None

        s3_key = (
            ea_version.source_file_path
            if file_type == "source"
            else ea_version.compiled_file_path
        )

        if not s3_key:
            return None

        return self.s3.download_ea_file(s3_key)

    async def delete_ea(self, ea_id: UUID) -> bool:
        """
        Soft delete an EA (mark as inactive)

        Args:
            ea_id: EA ID

        Returns:
            True if successful
        """
        ea = await self.get_ea_by_id(ea_id)
        if not ea:
            return False

        ea.is_active = False
        await self.db.commit()

        logger.info(f"Deleted EA: {ea_id}")
        return True

    async def update_ea(
        self,
        ea_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[ExpertAdvisor]:
        """Update EA metadata"""
        ea = await self.get_ea_by_id(ea_id)
        if not ea:
            return None

        if name is not None:
            ea.name = name
        if description is not None:
            ea.description = description
        if tags is not None:
            ea.tags = tags

        await self.db.commit()
        await self.db.refresh(ea)

        return ea


# Dependency injection
def get_ea_service(db: AsyncSession, s3_service: S3Service) -> EAService:
    """FastAPI dependency for EA service"""
    return EAService(db, s3_service)

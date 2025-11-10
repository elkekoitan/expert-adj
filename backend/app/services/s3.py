"""
S3/MinIO Storage Service
"""

import hashlib
import logging
from datetime import datetime
from io import BytesIO
from typing import BinaryIO, Optional

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Service:
    """
    S3/MinIO file storage service for EA files and related assets
    """

    def __init__(self):
        """Initialize S3 client"""
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(signature_version="s3v4"),
            use_ssl=settings.S3_USE_SSL,
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    def init_buckets(self) -> bool:
        """
        Initialize S3 buckets if they don't exist

        Returns:
            True if successful
        """
        try:
            # Check if bucket exists
            self.client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket '{self.bucket_name}' already exists")
            return True
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                # Bucket doesn't exist, create it
                try:
                    self.client.create_bucket(Bucket=self.bucket_name)
                    logger.info(f"Created bucket '{self.bucket_name}'")
                    return True
                except ClientError as create_error:
                    logger.error(f"Failed to create bucket: {create_error}")
                    return False
            else:
                logger.error(f"Error checking bucket: {e}")
                return False

    def upload_ea_file(
        self,
        file_content: bytes,
        ea_id: str,
        version: str,
        filename: str,
        file_type: str = "compiled",
    ) -> Optional[str]:
        """
        Upload EA file to S3

        Args:
            file_content: File content as bytes
            ea_id: Expert Advisor ID
            version: Version string
            filename: Original filename
            file_type: 'compiled' or 'source'

        Returns:
            S3 object key (path) or None if failed
        """
        # Generate S3 key (path)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_hash = hashlib.sha256(file_content).hexdigest()[:8]
        s3_key = f"eas/{ea_id}/{version}/{file_type}/{timestamp}_{file_hash}_{filename}"

        try:
            # Upload file
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=self._get_content_type(filename),
                Metadata={
                    "ea_id": str(ea_id),
                    "version": version,
                    "file_type": file_type,
                    "original_filename": filename,
                    "upload_timestamp": timestamp,
                },
            )

            logger.info(f"Uploaded EA file: {s3_key}")
            return s3_key

        except ClientError as e:
            logger.error(f"Failed to upload EA file: {e}")
            return None

    def download_ea_file(self, s3_key: str) -> Optional[bytes]:
        """
        Download EA file from S3

        Args:
            s3_key: S3 object key (path)

        Returns:
            File content as bytes or None if failed
        """
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=s3_key)
            content = response["Body"].read()
            logger.info(f"Downloaded EA file: {s3_key}")
            return content

        except ClientError as e:
            logger.error(f"Failed to download EA file: {e}")
            return None

    def delete_ea_file(self, s3_key: str) -> bool:
        """
        Delete EA file from S3

        Args:
            s3_key: S3 object key (path)

        Returns:
            True if successful
        """
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"Deleted EA file: {s3_key}")
            return True

        except ClientError as e:
            logger.error(f"Failed to delete EA file: {e}")
            return False

    def list_ea_files(self, ea_id: str, version: Optional[str] = None) -> list:
        """
        List all files for an EA

        Args:
            ea_id: Expert Advisor ID
            version: Optional version filter

        Returns:
            List of S3 object keys
        """
        prefix = f"eas/{ea_id}/"
        if version:
            prefix += f"{version}/"

        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix
            )

            if "Contents" in response:
                return [obj["Key"] for obj in response["Contents"]]
            return []

        except ClientError as e:
            logger.error(f"Failed to list EA files: {e}")
            return []

    def get_file_url(self, s3_key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate presigned URL for file download

        Args:
            s3_key: S3 object key (path)
            expires_in: URL expiration time in seconds

        Returns:
            Presigned URL or None if failed
        """
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_key},
                ExpiresIn=expires_in,
            )
            return url

        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None

    def upload_optimization_result(
        self, optimization_id: str, result_data: bytes, filename: str
    ) -> Optional[str]:
        """
        Upload optimization result file

        Args:
            optimization_id: Optimization session ID
            result_data: Result file content
            filename: Filename

        Returns:
            S3 object key or None if failed
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        s3_key = f"optimizations/{optimization_id}/{timestamp}_{filename}"

        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=result_data,
                ContentType="application/octet-stream",
                Metadata={
                    "optimization_id": str(optimization_id),
                    "upload_timestamp": timestamp,
                },
            )

            logger.info(f"Uploaded optimization result: {s3_key}")
            return s3_key

        except ClientError as e:
            logger.error(f"Failed to upload optimization result: {e}")
            return None

    def upload_backtest_report(
        self, backtest_id: str, report_html: str
    ) -> Optional[str]:
        """
        Upload backtest HTML report

        Args:
            backtest_id: Backtest result ID
            report_html: HTML report content

        Returns:
            S3 object key or None if failed
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        s3_key = f"backtests/{backtest_id}/{timestamp}_report.html"

        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=report_html.encode("utf-8"),
                ContentType="text/html",
                Metadata={
                    "backtest_id": str(backtest_id),
                    "upload_timestamp": timestamp,
                },
            )

            logger.info(f"Uploaded backtest report: {s3_key}")
            return s3_key

        except ClientError as e:
            logger.error(f"Failed to upload backtest report: {e}")
            return None

    @staticmethod
    def _get_content_type(filename: str) -> str:
        """
        Determine content type based on file extension

        Args:
            filename: File name

        Returns:
            MIME type string
        """
        ext = filename.lower().split(".")[-1]
        content_types = {
            "ex4": "application/octet-stream",
            "ex5": "application/octet-stream",
            "mq4": "text/plain",
            "mq5": "text/plain",
            "html": "text/html",
            "json": "application/json",
            "csv": "text/csv",
        }
        return content_types.get(ext, "application/octet-stream")


# Global instance
s3_service = S3Service()


# Utility functions
def init_s3_buckets():
    """Initialize S3 buckets - call on startup"""
    return s3_service.init_buckets()


def get_s3_service() -> S3Service:
    """Dependency injection for FastAPI"""
    return s3_service

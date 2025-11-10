"""
Initialize MinIO/S3 buckets
Run this after starting MinIO service
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.s3 import s3_service


def main():
    """Initialize S3 buckets"""
    print("🗄️  Initializing MinIO/S3 buckets...")

    try:
        success = s3_service.init_buckets()

        if success:
            print(f"✅ Bucket '{s3_service.bucket_name}' initialized successfully!")
            print(f"   Endpoint: {s3_service.client._endpoint}")
            return 0
        else:
            print("❌ Failed to initialize buckets")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

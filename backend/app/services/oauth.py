"""
Google OAuth 2.0 Authentication Service
"""
from typing import Optional, Dict, Any
import httpx
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from app.core.config import settings


class GoogleOAuthService:
    """
    Google OAuth 2.0 service for authentication
    """

    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    def get_authorization_url(self, state: str) -> str:
        """
        Generate Google OAuth authorization URL with PKCE

        Args:
            state: Random state for CSRF protection

        Returns:
            Authorization URL
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join([
                "openid",
                "email",
                "profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ]),
            "state": state,
            "access_type": "offline",  # Request refresh token
            "prompt": "consent",  # Force consent screen to get refresh token
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from callback

        Returns:
            Token response dict with access_token, refresh_token, expires_in

        Raises:
            HTTPException: If token exchange fails
        """
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.GOOGLE_TOKEN_URL,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to exchange code for token: {str(e)}",
                )

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Get user information from Google

        Args:
            access_token: Google access token

        Returns:
            User info dict with email, name, picture, etc.

        Raises:
            HTTPException: If request fails
        """
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.GOOGLE_USERINFO_URL,
                    headers=headers,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to get user info: {str(e)}",
                )

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token

        Args:
            refresh_token: Google refresh token

        Returns:
            New token response

        Raises:
            HTTPException: If refresh fails
        """
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.GOOGLE_TOKEN_URL,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to refresh token: {str(e)}",
                )

    async def revoke_token(self, token: str) -> bool:
        """
        Revoke Google access or refresh token

        Args:
            token: Access or refresh token to revoke

        Returns:
            True if successful

        Raises:
            HTTPException: If revocation fails
        """
        revoke_url = "https://oauth2.googleapis.com/revoke"
        params = {"token": token}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(revoke_url, params=params)
                response.raise_for_status()
                return True
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to revoke token: {str(e)}",
                )

    def calculate_token_expiry(self, expires_in: int) -> datetime:
        """
        Calculate token expiration datetime

        Args:
            expires_in: Seconds until expiration

        Returns:
            Expiration datetime
        """
        return datetime.utcnow() + timedelta(seconds=expires_in)


# Global instance
google_oauth_service = GoogleOAuthService()

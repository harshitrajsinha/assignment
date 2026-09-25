import os
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient

# Set environment variables before importing modules that depend on them
os.environ["LLM_PROVIDER"] = "gemini"
os.environ["LLM_MODEL"] = "gemini-1.5-flash"

from models.requests import GenerateRequest, GenerateResponse
from routes.health import router as health_router


class TestGenerateRequestValidation:
    """Test GenerateRequest validation"""
    
    def test_valid_question_meets_requirements(self):
        """Test that valid question meets requirements"""
        valid_questions = [
            "What is 2 + 2?",  # short valid question
            "Explain quantum computing in detail",  # medium length
            "A" * 100,  # exactly 100 chars
        ]
        
        for question in valid_questions:
            request = GenerateRequest(question=question)
            assert request.question == question
    
    def test_empty_question_fails_validation(self):
        """Test that empty question fails validation"""
        with pytest.raises(ValidationError) as exc_info:
            GenerateRequest(question="")
        
        assert "at least 1 character" in str(exc_info.value).lower()
    
    def test_question_too_long_fails_validation(self):
        """Test that question exceeding max length fails validation"""
        too_long_question = "A" * 10001  # exceeds 10,000 char limit
        
        with pytest.raises(ValidationError) as exc_info:
            GenerateRequest(question=too_long_question)
        
        assert "at most 10000 character" in str(exc_info.value).lower()


class TestHealthEndpoint:
    """Test health endpoint"""
    
    def test_health_endpoint_returns_200_status(self):
        """Test that health endpoint returns 200 status"""
        from fastapi import FastAPI
        
        # Create a test app with the health router
        test_app = FastAPI()
        test_app.include_router(health_router, prefix="/api/v1", tags=["health"])
        
        client = TestClient(test_app)
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
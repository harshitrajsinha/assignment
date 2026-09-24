"""
Basic test script to verify LLM gateway functionality.
Run this after setting up your .env file with a valid OpenAI API key.
Make sure the gateway service is running before executing this script.
"""

import asyncio
import httpx

# Gateway URL - for local testing, use localhost
GATEWAY_URL = "http://localhost:8001"


async def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GATEWAY_URL}/api/v1/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        print("✓ Health endpoint working\n")


async def test_generate():
    """Test the generate endpoint."""
    print("Testing generate endpoint...")
    
    test_request = {
        "question": "What is 2 + 2?",
        "context": {"test": "basic"},
        "session_id": "test-session-123"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{GATEWAY_URL}/api/v1/generate",
            json=test_request
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "model_used" in data
        print("✓ Generate endpoint working\n")


async def main():
    """Run all tests."""
    print("=" * 50)
    print("LLM Gateway Basic Tests")
    print("=" * 50 + "\n")
    
    try:
        await test_health()
        await test_generate()
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
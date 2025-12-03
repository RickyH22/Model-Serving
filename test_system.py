#!/usr/bin/env python3
"""
Test script to verify all components work
"""

import requests
import subprocess
import time
import os

def test_api():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API Endpoints...")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        print("   ✅ Health check passed")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
    
    # Test predict endpoint
    print("\n2. Testing /predict endpoint...")
    try:
        payload = {"x1": 1.5, "x2": 2.3}
        response = requests.post(f"{base_url}/predict", json=payload)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        assert response.status_code == 200
        assert "score" in result
        assert "model_version" in result
        print("   ✅ Prediction endpoint passed")
    except Exception as e:
        print(f"   ❌ Prediction endpoint failed: {e}")
    
    # Test metrics endpoint
    print("\n3. Testing /metrics endpoint...")
    try:
        response = requests.get(f"{base_url}/metrics")
        print(f"   Status: {response.status_code}")
        print(f"   Response preview: {response.text[:200]}...")
        assert response.status_code == 200
        assert "model_predictions_total" in response.text
        assert "model_prediction_latency_seconds" in response.text
        print("   ✅ Metrics endpoint passed")
    except Exception as e:
        print(f"   ❌ Metrics endpoint failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All API tests completed!")

def test_batch_inference():
    """Test batch inference script"""
    print("\n🧪 Testing Batch Inference...")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["python", "batch_infer.py", "data/input.csv", "data/predictions.csv"],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0 and os.path.exists("data/predictions.csv"):
            print("✅ Batch inference test passed")
        else:
            print(f"❌ Batch inference test failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Batch inference test failed: {e}")

if __name__ == "__main__":
    print("🚀 Model Serving System Test Suite")
    print("=" * 60)
    print("\nMake sure the API is running before testing:")
    print("  uvicorn app.main:app --reload")
    print("\nPress Enter when ready...")
    input()
    
    test_api()
    test_batch_inference()
    
    print("\n" + "=" * 60)
    print("🎉 Testing complete!")

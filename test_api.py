#!/usr/bin/env python3
"""Simple test script for the API"""

import requests
import json

base_url = "http://localhost:8000"

print("=" * 60)
print("Testing Model Serving API")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing /health endpoint...")
try:
    response = requests.get(f"{base_url}/health", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   ✅ PASSED" if response.status_code == 200 else "   ❌ FAILED")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 2: Prediction
print("\n2. Testing /predict endpoint...")
try:
    payload = {"x1": 1.5, "x2": 2.3}
    response = requests.post(f"{base_url}/predict", json=payload, timeout=5)
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
    print("   ✅ PASSED" if response.status_code == 200 and "score" in result else "   ❌ FAILED")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

# Test 3: Metrics
print("\n3. Testing /metrics endpoint...")
try:
    response = requests.get(f"{base_url}/metrics", timeout=5)
    print(f"   Status: {response.status_code}")
    metrics_text = response.text
    print(f"   Response preview (first 300 chars):\n{metrics_text[:300]}")
    has_counter = "model_predictions_total" in metrics_text
    has_histogram = "model_prediction_latency_seconds" in metrics_text
    print(f"   Counter found: {has_counter}")
    print(f"   Histogram found: {has_histogram}")
    print("   ✅ PASSED" if response.status_code == 200 and has_counter and has_histogram else "   ❌ FAILED")
except Exception as e:
    print(f"   ❌ FAILED: {e}")

print("\n" + "=" * 60)
print("Testing Complete!")
print("=" * 60)

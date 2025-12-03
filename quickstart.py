#!/usr/bin/env python3
"""Quick start script - creates model and shows next steps"""

print("=" * 60)
print("Model Serving System - Quick Start")
print("=" * 60)

print("\n📦 Creating baseline model...")
try:
    import numpy as np
    import joblib
    import os
    
    # Simple 2-feature classifier
    from sklearn.linear_model import LogisticRegression
    
    np.random.seed(42)
    X = np.random.randn(1000, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/baseline.joblib')
    
    print(f"✅ Model created: models/baseline.joblib")
    print(f"   Accuracy: {model.score(X, y):.3f}")
    
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("   Run: pip install scikit-learn joblib numpy")

print("\n🚀 Next Steps:")
print("=" * 60)
print("\n1. Start the API server:")
print("   uvicorn app.main:app --reload")
print("\n2. Test in another terminal:")
print('   curl http://localhost:8000/health')
print('   curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\\"x1\\":1.5,\\"x2\\":2.3}"')
print('   curl http://localhost:8000/metrics')
print("\n3. Run batch inference:")
print("   python batch_infer.py data/input.csv data/predictions.csv")
print("\n4. Build Docker (optional):")
print("   docker build -t model-server:v1 .")
print("   docker run -p 8000:8000 model-server:v1")
print("\n" + "=" * 60)

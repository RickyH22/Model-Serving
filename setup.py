#!/usr/bin/env python3
"""
Setup script to create baseline model and test the system
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib
import os

def create_baseline_model():
    """Create and save a simple baseline model"""
    print("Creating baseline model...")
    
    # Generate synthetic training data
    np.random.seed(42)
    X = np.random.randn(1000, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    # Train model
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    # Save model
    joblib.dump(model, 'models/baseline.joblib')
    
    # Print model info
    print(f"✅ Model created and saved to models/baseline.joblib")
    print(f"   Training accuracy: {model.score(X, y):.3f}")
    print(f"   Model coefficients: {model.coef_}")
    
    return model

if __name__ == "__main__":
    create_baseline_model()
    print("\nSetup complete! You can now:")
    print("1. Run the API: uvicorn app.main:app --reload")
    print("2. Run batch inference: python batch_infer.py data/input.csv data/predictions.csv")
    print("3. Build Docker: docker build -t model-server:v1 .")

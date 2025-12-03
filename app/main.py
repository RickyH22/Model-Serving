from fastapi import FastAPI, Response
from pydantic import BaseModel
import joblib
import time
from app.metrics import prediction_counter, prediction_latency, get_metrics, CONTENT_TYPE_LATEST

app = FastAPI(title="Model Serving API", version="v1.0")

# Load model at startup
try:
    model = joblib.load("models/baseline.joblib")
except FileNotFoundError:
    print("Warning: Model not found. Creating dummy model...")
    from sklearn.linear_model import LogisticRegression
    import numpy as np
    # Create a simple dummy model
    X_dummy = np.random.randn(100, 2)
    y_dummy = (X_dummy[:, 0] + X_dummy[:, 1] > 0).astype(int)
    model = LogisticRegression()
    model.fit(X_dummy, y_dummy)
    joblib.dump(model, "models/baseline.joblib")

# Request/Response schemas
class PredictionRequest(BaseModel):
    x1: float
    x2: float

class PredictionResponse(BaseModel):
    score: float
    model_version: str

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Make a prediction"""
    start_time = time.time()
    
    # Prepare input
    features = [[request.x1, request.x2]]
    
    # Get prediction probability
    prediction_proba = model.predict_proba(features)[0]
    score = float(prediction_proba[1])  # Probability of positive class
    
    # Track metrics
    prediction_counter.inc()
    latency = time.time() - start_time
    prediction_latency.observe(latency)
    
    return PredictionResponse(
        score=score,
        model_version="v1.0"
    )

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=get_metrics(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

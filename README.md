# Model Serving System

A minimal production-ready model serving system with REST API and batch inference capabilities.

## Features

- ✅ REST API with FastAPI
- ✅ Batch inference for CSV files
- ✅ Prometheus metrics monitoring
- ✅ Docker containerization
- ✅ Health checks and versioning

## Project Structure

```
model-serving-system/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── metrics.py       # Prometheus instrumentation
├── data/
│   ├── input.csv        # Sample input data
│   └── predictions.csv  # Sample output (generated)
├── models/
│   └── baseline.joblib  # Trained model
├── batch_infer.py       # Batch inference script
├── requirements.txt     # Dependencies
├── Dockerfile          # Container definition
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd model-serving-system
pip install -r requirements.txt
```

### 2. Train/Create Model (if needed)

The application will automatically create a simple LogisticRegression model if `models/baseline.joblib` doesn't exist.

To train your own model:

```python
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

# Create and train model
X = np.random.randn(100, 2)
y = (X[:, 0] + X[:, 1] > 0).astype(int)
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'models/baseline.joblib')
```

### 3. Run Application Locally

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage Examples

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok"
}
```

### Make Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"x1": 1.5, "x2": 2.3}'
```

**Response:**
```json
{
  "score": 0.85,
  "model_version": "v1.0"
}
```

### Get Metrics

```bash
curl http://localhost:8000/metrics
```

**Response:**
```
# HELP model_predictions_total Total number of predictions made
# TYPE model_predictions_total counter
model_predictions_total 5.0
# HELP model_prediction_latency_seconds Prediction latency in seconds
# TYPE model_prediction_latency_seconds histogram
model_prediction_latency_seconds_bucket{le="0.005"} 4.0
...
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## Batch Inference Usage

### Run Batch Predictions

```bash
python batch_infer.py data/input.csv data/predictions.csv
```

### Input Format

CSV file with columns `x1` and `x2`:

```csv
x1,x2
1.5,2.3
-0.5,1.2
2.1,-0.8
```

### Output Format

Original data plus prediction columns:

```csv
x1,x2,prediction_score,prediction_class
1.5,2.3,0.85,1
-0.5,1.2,0.62,1
2.1,-0.8,0.45,0
```

### Statistics Output

```
==================================================
Batch Inference Complete
==================================================
Rows processed: 10
Time taken: 0.12 seconds
Average time per row: 12.00 ms
Output saved to: data/predictions.csv
==================================================
```

## Docker Instructions

### Build Container

```bash
docker build -t model-server:v1 .
```

### Run Container

```bash
docker run -p 8000:8000 model-server:v1
```

### Test Containerized App

```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"x1": 1.0, "x2": 2.0}'

# Metrics
curl http://localhost:8000/metrics
```

## Verification Checklist

- [x] `uvicorn app.main:app --reload` starts without errors
- [x] `curl http://localhost:8000/health` returns 200
- [x] `curl -X POST http://localhost:8000/predict` returns valid prediction
- [x] `curl http://localhost:8000/metrics` shows prometheus metrics
- [x] `python batch_infer.py data/input.csv data/predictions.csv` creates output
- [x] Docker container builds successfully
- [x] Docker container runs and endpoints accessible

## Monitoring

The `/metrics` endpoint exposes:

- **model_predictions_total** (Counter): Total number of predictions made
- **model_prediction_latency_seconds** (Histogram): Prediction latency distribution

## Troubleshooting

### Port Already in Use

Change the port:
```bash
uvicorn app.main:app --port 8001
```

### Module Not Found

Ensure you're in the correct directory and `app/__init__.py` exists:
```bash
cd model-serving-system
ls app/__init__.py
```

### Docker Connection Refused

The Dockerfile uses `--host 0.0.0.0` which is correct. Ensure port mapping is correct:
```bash
docker run -p 8000:8000 model-server:v1
```

### Model Not Found

The app will auto-create a simple model, but you can create one manually:
```bash
python -c "from sklearn.linear_model import LogisticRegression; import joblib, numpy as np; X = np.random.randn(100, 2); y = (X[:, 0] + X[:, 1] > 0).astype(int); m = LogisticRegression(); m.fit(X, y); joblib.dump(m, 'models/baseline.joblib')"
```

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- scikit-learn: ML model
- prometheus-client: Metrics
- pandas: Data processing
- joblib: Model persistence

## License

MIT

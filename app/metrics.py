from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Prometheus metrics
prediction_counter = Counter(
    'model_predictions_total',
    'Total number of predictions made'
)

prediction_latency = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency in seconds'
)

def get_metrics():
    """Return Prometheus metrics"""
    return generate_latest()

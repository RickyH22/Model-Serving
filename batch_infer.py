#!/usr/bin/env python3
"""
Batch Inference Script
Processes CSV files with trained model
"""

import sys
import time
import pandas as pd
import joblib

def batch_inference(input_path, output_path, model_path="models/baseline.joblib"):
    """
    Process batch predictions
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to save predictions CSV
        model_path: Path to trained model
    """
    start_time = time.time()
    
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} rows")
    
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    
    # Extract features
    features = df[['x1', 'x2']].values
    
    print("Generating predictions...")
    predictions = model.predict_proba(features)[:, 1]
    
    # Add predictions to dataframe
    df['prediction_score'] = predictions
    df['prediction_class'] = (predictions > 0.5).astype(int)
    
    # Save results
    df.to_csv(output_path, index=False)
    
    elapsed_time = time.time() - start_time
    
    print(f"\n{'='*50}")
    print(f"Batch Inference Complete")
    print(f"{'='*50}")
    print(f"Rows processed: {len(df)}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"Average time per row: {elapsed_time/len(df)*1000:.2f} ms")
    print(f"Output saved to: {output_path}")
    print(f"{'='*50}\n")
    
    return df

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python batch_infer.py <input.csv> <output.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        batch_inference(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

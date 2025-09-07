import pandas as pd
from networksecurity.pipeline.predict_pipeline import PredictPipeline

# Load test data
test_df = pd.read_csv('artifacts/test.csv')

# Get features (exclude Result column)
features = test_df.drop(columns=['Result'])

# Initialize prediction pipeline
predictor = PredictPipeline()

# Predict on first 20 samples
predictions = predictor.predict(features.head(20))

print("First 20 predictions:")
print(predictions)

# Check unique predictions
unique_preds = set(predictions)
print(f"\nUnique predictions: {unique_preds}")

# Check if all three classes are predicted
expected_classes = {-1, 0, 1}
if expected_classes.issubset(unique_preds):
    print("✅ Model predicts all three classes: -1, 0, 1")
else:
    print("❌ Model does not predict all three classes")
    print(f"Missing classes: {expected_classes - unique_preds}")

# Also check actual labels for comparison
actual_labels = test_df['Result'].head(20).values
print(f"\nActual labels: {actual_labels}")

# Count predictions per class
pred_counts = pd.Series(predictions).value_counts()
print(f"\nPrediction counts:\n{pred_counts}")

"""
Simple model training script without visualization dependencies
Train Random Forest model for water availability prediction
"""
import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from preprocess import load_and_preprocess_data

def train_model(dataset_path):
    """Train Random Forest model"""
    print("=" * 70)
    print("AQUAVISION AI - MODEL TRAINING")
    print("=" * 70)
    
    # Load and preprocess data
    print("\n📊 Loading and preprocessing data...")
    X_train, X_test, y_train, y_test, label_mappings, features, class_names = \
        load_and_preprocess_data(dataset_path)
    
    print(f"✅ Training samples: {len(X_train)}")
    print(f"✅ Testing samples: {len(X_test)}")
    print(f"✅ Features: {len(features)}")
    print(f"✅ Classes: {class_names}")
    
    # Train Random Forest
    print("\n🔄 Training Random Forest model...")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    clf.fit(X_train, y_train)
    print("✅ Model trained successfully")
    
    # Evaluate
    print("\n📊 Evaluating model...")
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*70}")
    print(f"MODEL PERFORMANCE")
    print(f"{'='*70}")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Cross-validation
    cv_scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
    print(f"Cross-validation: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Classification report
    print(f"\n{'='*70}")
    print("CLASSIFICATION REPORT")
    print(f"{'='*70}")
    print(classification_report(y_test, y_pred, target_names=class_names))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"{'='*70}")
    print("CONFUSION MATRIX")
    print(f"{'='*70}")
    print(cm)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n{'='*70}")
    print("TOP 10 IMPORTANT FEATURES")
    print(f"{'='*70}")
    print(feature_importance.head(10).to_string(index=False))
    
    # Water level thresholds
    thresholds = {
        "low_limit": 3.65,
        "medium_limit": 7.76
    }
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), "aquavision_model.joblib")
    payload = {
        "model": clf,
        "model_name": "Random Forest",
        "accuracy": accuracy,
        "label_mappings": label_mappings,
        "features": features,
        "class_names": class_names,
        "thresholds": thresholds,
        "trained_at": datetime.now().isoformat(),
        "feature_importance": feature_importance.to_dict('records')
    }
    
    joblib.dump(payload, model_path)
    print(f"\n{'='*70}")
    print(f"✅ Model saved to: {model_path}")
    print(f"{'='*70}")
    
    return payload

if __name__ == "__main__":
    # Path to dataset
    dataset_path = "../../groundwater-DATASET.csv"
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}")
        print("Please ensure the dataset file exists.")
        exit(1)
    
    # Train model
    result = train_model(dataset_path)
    
    print("\n" + "="*70)
    print("TRAINING COMPLETE!")
    print("="*70)
    print("\nYou can now start the backend server:")
    print("  cd ..")
    print("  python3 app.py")
    print("\nThe model will be automatically loaded on startup.")

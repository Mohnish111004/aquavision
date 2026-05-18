"""
Comparative ML Model Analysis
Train and compare multiple models: Random Forest, Decision Tree, XGBoost, SVM
"""
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️  XGBoost not installed. Install with: pip install xgboost")

from preprocess import load_and_preprocess_data

def train_and_compare_models(dataset_path, output_dir='../../output'):
    """
    Train multiple models and generate comparative analysis
    
    Returns:
        dict: Comparison results with metrics for each model
    """
    print("=" * 70)
    print("COMPARATIVE ML MODEL ANALYSIS")
    print("=" * 70)
    
    # Load and preprocess data
    print("\n📊 Loading and preprocessing data...")
    X_train, X_test, y_train, y_test, label_mappings, features, class_names = \
        load_and_preprocess_data(dataset_path)
    
    print(f"✅ Training samples: {len(X_train)}")
    print(f"✅ Testing samples: {len(X_test)}")
    print(f"✅ Features: {len(features)}")
    print(f"✅ Classes: {class_names}")
    
    # Define models to compare
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ),
        'Decision Tree': DecisionTreeClassifier(
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        ),
        'SVM': SVC(
            kernel='rbf',
            C=1.0,
            gamma='scale',
            probability=True,
            random_state=42
        )
    }
    
    # Add XGBoost if available
    if XGBOOST_AVAILABLE:
        models['XGBoost'] = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            eval_metric='mlogloss'
        )
    
    # Store results
    results = {}
    trained_models = {}
    
    print("\n" + "=" * 70)
    print("TRAINING MODELS")
    print("=" * 70)
    
    # Train and evaluate each model
    for model_name, model in models.items():
        print(f"\n🔄 Training {model_name}...")
        
        try:
            # Train model
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            
            # Store results
            results[model_name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'cv_mean': cv_mean,
                'cv_std': cv_std,
                'confusion_matrix': cm.tolist(),
                'predictions': y_pred.tolist(),
                'probabilities': y_pred_proba.tolist()
            }
            
            trained_models[model_name] = model
            
            print(f"✅ {model_name} trained successfully")
            print(f"   Accuracy: {accuracy:.4f}")
            print(f"   Precision: {precision:.4f}")
            print(f"   Recall: {recall:.4f}")
            print(f"   F1-Score: {f1:.4f}")
            print(f"   CV Score: {cv_mean:.4f} (+/- {cv_std:.4f})")
        
        except Exception as e:
            print(f"❌ Error training {model_name}: {str(e)}")
            results[model_name] = {'error': str(e)}
    
    # Find best model
    best_model_name = max(results, key=lambda x: results[x].get('accuracy', 0))
    best_accuracy = results[best_model_name]['accuracy']
    
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Accuracy: {best_accuracy:.4f}")
    
    # Generate visualizations
    print("\n📊 Generating comparison visualizations...")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Accuracy Comparison Bar Chart
    plt.figure(figsize=(12, 6))
    model_names = [name for name in results.keys() if 'error' not in results[name]]
    accuracies = [results[name]['accuracy'] for name in model_names]
    colors_list = ['#10b981' if name == best_model_name else '#3b82f6' for name in model_names]
    
    bars = plt.bar(model_names, accuracies, color=colors_list, alpha=0.8, edgecolor='black')
    plt.xlabel('Model', fontsize=12, fontweight='bold')
    plt.ylabel('Accuracy', fontsize=12, fontweight='bold')
    plt.title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    plt.ylim([0, 1.0])
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'model_accuracy_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Comprehensive Metrics Comparison
    plt.figure(figsize=(14, 8))
    metrics_data = []
    for name in model_names:
        metrics_data.append([
            results[name]['accuracy'],
            results[name]['precision'],
            results[name]['recall'],
            results[name]['f1_score']
        ])
    
    x = np.arange(len(model_names))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.bar(x - 1.5*width, [m[0] for m in metrics_data], width, label='Accuracy', color='#3b82f6')
    ax.bar(x - 0.5*width, [m[1] for m in metrics_data], width, label='Precision', color='#10b981')
    ax.bar(x + 0.5*width, [m[2] for m in metrics_data], width, label='Recall', color='#f59e0b')
    ax.bar(x + 1.5*width, [m[3] for m in metrics_data], width, label='F1-Score', color='#ef4444')
    
    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Comprehensive Model Metrics Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, 1.0])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'model_metrics_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Confusion Matrix for Best Model
    plt.figure(figsize=(10, 8))
    cm = np.array(results[best_model_name]['confusion_matrix'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Count'})
    plt.title(f'Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'best_model_confusion_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Visualizations saved to {output_dir}/")
    
    # Save comparison results
    comparison_data = {
        'timestamp': datetime.now().isoformat(),
        'best_model': best_model_name,
        'results': results,
        'class_names': class_names,
        'features': features
    }
    
    comparison_path = os.path.join(output_dir, 'model_comparison.joblib')
    joblib.dump(comparison_data, comparison_path)
    print(f"✅ Comparison data saved to {comparison_path}")
    
    # Save best model
    best_model_path = os.path.join(os.path.dirname(__file__), 'best_model.joblib')
    best_model_payload = {
        'model': trained_models[best_model_name],
        'model_name': best_model_name,
        'accuracy': best_accuracy,
        'label_mappings': label_mappings,
        'features': features,
        'class_names': class_names,
        'trained_at': datetime.now().isoformat()
    }
    joblib.dump(best_model_payload, best_model_path)
    print(f"✅ Best model saved to {best_model_path}")
    
    return comparison_data


if __name__ == "__main__":
    # Path to dataset
    dataset_path = "../../groundwater-DATASET.csv"
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}")
        print("Please ensure the dataset file exists.")
        exit(1)
    
    # Run comparison
    results = train_and_compare_models(dataset_path)
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - output/model_accuracy_comparison.png")
    print("  - output/model_metrics_comparison.png")
    print("  - output/best_model_confusion_matrix.png")
    print("  - output/model_comparison.joblib")
    print("  - backend/model/best_model.joblib")

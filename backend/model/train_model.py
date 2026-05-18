"""
AquaVision AI – Model Training Script
Run from the backend/ directory:
    python model/train_model.py
"""
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "..", "groundwater-DATASET.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "output")
MODEL_OUT = os.path.join(BASE_DIR, "model", "aquavision_model.joblib")

os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
sns.set_theme(style="whitegrid")


def preprocess():
    print("🚀 [1/5] Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    print(f"   Loaded {len(df):,} rows, {len(df.columns)} columns")

    df = df.sort_values(["state_name", "district_name", "station_name", "date"])
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["dayofyear"] = df["date"].dt.dayofyear

    def bin_level(val):
        if val <= 3.65:
            return 2   # High
        elif val <= 7.76:
            return 1   # Medium
        return 0       # Low

    df["water_avail"] = df["currentlevel"].apply(bin_level)
    df["next_water_avail"] = (
        df.groupby(["state_name", "district_name", "station_name"])["water_avail"]
        .shift(-1)
    )
    df = df.dropna(subset=["next_water_avail"]).copy()
    df["next_water_avail"] = df["next_water_avail"].astype(int)
    print(f"   Clean dataset: {len(df):,} rows")
    return df


def encode(df):
    print("\n🚀 [2/5] Encoding categorical features...")
    cats = ["state_name", "district_name", "basin", "sub_basin", "station_name", "source"]
    mappings = {}
    for col in cats:
        vals = sorted(df[col].dropna().unique())
        m = {v: i + 1 for i, v in enumerate(vals)}
        mappings[col] = {"mapping": m, "inverse": {i + 1: v for i, v in enumerate(vals)}}
        mappings[col]["inverse"][0] = "Unknown"
        df[col + "_encoded"] = df[col].map(m).fillna(0).astype(int)
    return df, mappings


def train(df, mappings):
    print("\n🚀 [3/5] Training models...")
    features = [
        "latitude", "longitude", "currentlevel", "level_diff",
        "year", "month", "day", "dayofyear",
        "state_name_encoded", "district_name_encoded",
        "basin_encoded", "sub_basin_encoded", "station_name_encoded"
    ]
    X, y = df[features], df["next_water_avail"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Random Forest (sampled)
    sample = min(200_000, len(X_train))
    idx = np.random.choice(X_train.index, size=sample, replace=False)
    rf = RandomForestClassifier(n_estimators=100, max_depth=16, min_samples_split=8,
                                random_state=42, n_jobs=-1)
    rf.fit(X_train.loc[idx], y_train.loc[idx])
    rf_acc = accuracy_score(y_test, rf.predict(X_test))
    print(f"   Random Forest accuracy: {rf_acc:.4f}")

    # HistGradientBoosting (full)
    hgb = HistGradientBoostingClassifier(max_iter=100, max_depth=12,
                                         learning_rate=0.1, random_state=42)
    hgb.fit(X_train, y_train)
    hgb_preds = hgb.predict(X_test)
    hgb_acc = accuracy_score(y_test, hgb_preds)
    print(f"   HistGradientBoosting accuracy: {hgb_acc:.4f}")

    best_name = "HistGradientBoosting" if hgb_acc >= rf_acc else "Random Forest"
    best_clf = hgb if hgb_acc >= rf_acc else rf
    best_preds = hgb_preds if hgb_acc >= rf_acc else rf.predict(X_test)
    print(f"   🏆 Best: {best_name} ({max(rf_acc, hgb_acc):.4f})")

    return best_name, best_clf, best_preds, y_test, rf, rf_acc, hgb_acc, features


def visualize(best_name, best_preds, y_test, rf, rf_acc, hgb_acc, features):
    print("\n🚀 [4/5] Generating visualizations...")

    # Accuracy comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(["Random Forest", "HistGradientBoosting"],
                  [rf_acc * 100, hgb_acc * 100],
                  color=["#4a5568", "#3182ce"], width=0.5)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1,
                f"{b.get_height():.2f}%", ha="center", weight="bold")
    ax.set_ylim(50, 100)
    ax.set_title("Model Accuracy Comparison", weight="bold")
    ax.set_ylabel("Accuracy (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "accuracy_comparison.png"), dpi=150)
    plt.close()

    # Feature importance
    imp = rf.feature_importances_
    idx = np.argsort(imp)[::-1]
    readable = [f.replace("_encoded", "").title() for f in features]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=imp[idx], y=[readable[i] for i in idx], palette="Blues_r", ax=ax)
    ax.set_title("Feature Importance (Random Forest)", weight="bold")
    ax.set_xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "feature_importance.png"), dpi=150)
    plt.close()

    # Confusion matrix
    cm = confusion_matrix(y_test, best_preds)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Low", "Medium", "High"],
                yticklabels=["Low", "Medium", "High"], ax=ax)
    ax.set_title(f"Confusion Matrix – {best_name}", weight="bold")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix.png"), dpi=150)
    plt.close()

    print(classification_report(y_test, best_preds, target_names=["Low", "Medium", "High"]))


def save(best_name, best_clf, mappings, features, rf_acc, hgb_acc):
    print("\n🚀 [5/5] Saving model...")
    payload = {
        "model_name": best_name,
        "model": best_clf,
        "features": features,
        "label_mappings": mappings,
        "class_names": ["Low", "Medium", "High"],
        "thresholds": {"low_limit": 3.65, "medium_limit": 7.76},
        "system_metadata": {
            "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dataset_rows": 550850,
            "framework": "scikit-learn",
            "rf_accuracy": round(rf_acc * 100, 2),
            "hgb_accuracy": round(hgb_acc * 100, 2),
        }
    }
    joblib.dump(payload, MODEL_OUT, compress=3)
    print(f"   Saved → {MODEL_OUT}")


if __name__ == "__main__":
    df = preprocess()
    df, mappings = encode(df)
    best_name, best_clf, best_preds, y_test, rf, rf_acc, hgb_acc, features = train(df, mappings)
    visualize(best_name, best_preds, y_test, rf, rf_acc, hgb_acc, features)
    save(best_name, best_clf, mappings, features, rf_acc, hgb_acc)
    print("\n🎉 Training complete!")

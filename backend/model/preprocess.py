"""
Shared preprocessing utilities used by both train_model.py and the predict route.
"""
import pandas as pd


THRESHOLDS = {"low_limit": 3.65, "medium_limit": 7.76}
CLASS_NAMES = ["Low", "Medium", "High"]
FEATURES = [
    "latitude", "longitude", "currentlevel", "level_diff",
    "year", "month", "day", "dayofyear",
    "state_name_encoded", "district_name_encoded",
    "basin_encoded", "sub_basin_encoded", "station_name_encoded"
]


def bin_water_level(val: float) -> int:
    """Convert a groundwater depth (metres) to a class index."""
    if val <= THRESHOLDS["low_limit"]:
        return 2   # High availability
    elif val <= THRESHOLDS["medium_limit"]:
        return 1   # Medium availability
    return 0       # Low availability


def current_status_label(val: float) -> str:
    """Human-readable current status from depth value."""
    idx = bin_water_level(val)
    return CLASS_NAMES[idx]


def build_input_df(data: dict, label_mappings: dict) -> pd.DataFrame:
    """
    Build a single-row DataFrame ready for model.predict() from a raw
    request dict and the label_mappings stored in the model payload.
    """
    date = pd.to_datetime(
        data.get("date", pd.Timestamp.now().strftime("%Y-%m-%d"))
    )

    def encode(col, val):
        return label_mappings.get(col, {}).get("mapping", {}).get(val, 0)

    row = [
        float(data["latitude"]),
        float(data["longitude"]),
        float(data["currentlevel"]),
        float(data["level_diff"]),
        date.year, date.month, date.day, date.dayofyear,
        encode("state_name", data.get("state_name", "")),
        encode("district_name", data.get("district_name", "")),
        encode("basin", data.get("basin", "")),
        encode("sub_basin", data.get("sub_basin", "")),
        encode("station_name", data.get("station_name", "")),
    ]
    return pd.DataFrame([row], columns=FEATURES)

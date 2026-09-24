"""
Data validation and DataFrame construction.
"""

import numpy as np
import pandas as pd


def validate_data(data: dict) -> None:
    """
    Validate the input dict {group_name: [values]}.

    Raises:
        TypeError, ValueError: if structure is invalid.
    """
    if not isinstance(data, dict):
        raise TypeError("DATA must be a dict")
    if len(data) < 2:
        raise ValueError(f"Need >= 2 groups, got {len(data)}")
    for name, values in data.items():
        if not isinstance(values, (list, tuple, np.ndarray)):
            raise TypeError(f"Group '{name}' values must be a list")
        if len(values) < 2:
            raise ValueError(f"Group '{name}' has too few values ({len(values)})")
        if np.isnan(np.asarray(values, dtype=float)).any():
            raise ValueError(f"Group '{name}' contains NaN")


def build_dataframe(data: dict) -> pd.DataFrame:
    """Convert {group: [values]} to a long-format DataFrame."""
    rows = [{"group": g, "value": float(v)} for g, vals in data.items() for v in vals]
    return pd.DataFrame(rows)
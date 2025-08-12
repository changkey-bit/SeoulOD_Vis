import pandas as pd
import math
from datetime import datetime, timedelta


def parse_time_components(df_row):
    return df_row['hour'], df_row['minutes'], df_row['second']


def loading_check(df, start_idx: int, load_duration: str) -> int:
    """
    Calculate loading end index given a start index and duration string 'MMSS'.
    Returns the index where loading ends.
    """
    # Starting timestamp
    h, m, s = parse_time_components(df.loc[start_idx])
    start_time = datetime.strptime(f"{h}:{m}:{s}", "%H:%M:%S")

    # Parse duration
    dur_min = int(load_duration[:2])
    dur_sec = int(load_duration[2:])
    load_delta = timedelta(minutes=dur_min, seconds=dur_sec)
    end_time = start_time + load_delta

    # Find first index where time >= end_time
    mask = (
        (df['hour'] == end_time.hour) &
        (df['minutes'] >= end_time.minute) &
        (df['second'] >= end_time.second)
    )
    end_indices = df.index[mask]
    end_idx = end_indices[0] if not end_indices.empty else None
    print(f"Loading end index for start {start_idx}: {end_idx}")
    return end_idx


def calculate_metrics(df_segment: pd.DataFrame, region: str) -> dict:
    """
    Calculate distance traveled, click count, and task time for specified region.
    region can be 'left', 'map', or 'all'.
    """
    # Define x-filter bounds
    bounds = {
        'left': (None, 440),
        'map': (441, 1920),
        'all': (None, 1920)
    }
    x_min, x_max = bounds.get(region, (None, None))

    # Filter clicks
    click_count = df_segment[df_segment['function'] == 'Left'].shape[0]

    # Filter points by region
    cond = pd.Series(True, index=df_segment.index)
    if x_min is not None:
        cond &= df_segment['x'] >= x_min
    if x_max is not None:
        cond &= df_segment['x'] <= x_max
    points = df_segment[cond]

    # Compute distance and time
    distance = 0.0
    task_time = 0
    prev_point = None
    prev_time = None

    for _, row in points.iterrows():
        current_point = (row['x'], row['y'])
        current_time = datetime.strptime(
            f"{row['hour']}:{row['minutes']}:{row['second']}", "%H:%M:%S"
        )

        if prev_point is not None:
            # accumulate distance
            dx = current_point[0] - prev_point[0]
            dy = current_point[1] - prev_point[1]
            distance += math.hypot(dx, dy)
            # accumulate time
            task_time += int((current_time - prev_time).total_seconds())

        prev_point, prev_time = current_point, current_time

    return {
        'distance': distance,
        'clicks': click_count,
        'task_time': task_time
    }


def split_tasks(df: pd.DataFrame, slices: list) -> list:
    """
    Split dataframe into segments based on provided index ranges.
    slices: list of (start, end) tuples
    Returns list of DataFrame segments.
    """
    return [df.loc[start:end] for start, end in slices]


if __name__ == '__main__':
    # Load data
    header = ['date', 'hour', 'minutes', 'second', 'mili_sec', 'x', 'y', 'function', 'up', 'scroll']
    df = pd.read_csv('mouse_tracking\mouse_tracking_P1.csv',names=header, header=None)

    # Define global tasks slices
    global_slices = []
    task_dfs = split_tasks(df, global_slices)

    # Further split each global task
    sub_slices = []

    # Process each main task
    for idx, task_df in enumerate(task_dfs, start=1):
        print(f"\nProcessing Task {idx}")
        slices = sub_slices[idx-1]
        segments = []
        for start, end in slices:
            end_idx = end if end is not None else task_df.index[-1]
            segments.append(task_df.loc[start:end_idx])

        for region in ['all', 'left', 'map']:
            # Aggregate metrics across segments
            metrics_list = [calculate_metrics(seg, region) for seg in segments]
            agg = pd.DataFrame(metrics_list).sum().to_dict()
            print(f"Region {region}: {agg}")

    # Example loading checks
    load_params = []
    for start_idx, duration in load_params:
        loading_check(df, start_idx, duration)

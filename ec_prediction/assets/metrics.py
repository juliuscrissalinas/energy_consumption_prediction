from dagster import asset
from ec_prediction.assets import constants
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.io as pio
import os
import matplotlib.pyplot as plt

@asset(
    group_name='data_visualization',
    deps = ['convert_to_float']
)
def plot_data(context, convert_to_float: np.ndarray) -> None:
    """
    Dynamically create and save plots for all data points, 200 points, 480 points, etc.
    """
    mw = convert_to_float[:, 0]  # Extract MW data

    # Generate timestamps (assuming hourly data starting from a specific datetime)
    start_time = datetime.datetime(2002, 12, 31, 1, 0, 0)
    timestamps = [start_time + datetime.timedelta(hours=i) for i in range(len(mw))]

    # Define data sizes to plot
    sizes = ["all", 200, 480, 960, 960 * 5]  # You can extend this as needed
    saved_files = []
    # Ensure the output folder exists
    output_folder = constants.MW_TIMESERIES_FOLDER
    os.makedirs(output_folder, exist_ok=True)

    for size in sizes:
        # Determine the range of data to plot
        if size == "all":
            sub_mw = mw
            sub_timestamps = timestamps
            size_label = "all"
        else:
            size = min(size, len(mw))  # Ensure size doesn't exceed data length
            sub_mw = mw[:size]
            sub_timestamps = timestamps[:size]
            size_label = f"{size}pts"

        # Create a Plotly time-series plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[ts.isoformat() for ts in sub_timestamps],  # X-axis: timestamps
            y=sub_mw,                                     # Y-axis: MW values
            mode='lines',
            name=f'MW Data ({size_label})',
            line=dict(color='blue')
        ))

        # Customize the layout
        fig.update_layout(
            title=f"MW Float Data Over Time ({size_label})",
            xaxis_title="Time",
            yaxis_title="MW",
            template="plotly_white"
        )

        # Dynamically generate a file name
        file_name = f"mw_time_series_{size_label}.png"
        file_path = os.path.join(constants.MW_TIMESERIES_FOLDER, file_name)

        # Save the plot as a PNG file
        fig.write_image(file_path)
        saved_files.append(file_path)
        context.log.info(f"Plot for {size_label} saved at {file_path}")

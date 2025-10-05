"""NASA.ipynb"""

!pip install pyhdf
!pip install rasterio matplotlib pandas numpy scikit-learn folium seaborn statsmodels

#Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import folium
from datetime import timedelta
from pyhdf.SD import SD

#Chart Visuals
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10,5)
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10

#Step 1: Define locations
locations = {
    "Japan": {"lat": 36.2048, "lon": 138.2529},
    "Alaska": {"lat": 64.2008, "lon": -149.4937},
    "Madagascar": {"lat": -18.7669, "lon": 46.8691},
    "New Zealand": {"lat": -40.9006, "lon": 174.8860},
    "Fiji": {"lat": -17.7134, "lon": 178.0650}
}

#Step 2: Load NDVI datasets from HDF file
hdf_file_path = 'YOUR_HDF_FILE.hdf'

ndvi_data = {}

try:
    hdf = SD(hdf_file_path)
    ndvi_dataset = hdf.select('ndvi') # Adjust dataset name
    ndvi_values = ndvi_dataset[:,:].flatten()
    dates = pd.date_range(start="2018-01-01", periods=len(ndvi_values), freq='M')
    all_ndvi_df = pd.DataFrame({"date": dates, "ndvi": ndvi_values})

    for loc in locations:
         ndvi_data[loc] = all_ndvi_df.copy()

except Exception as e:
    print(f"Error loading HDF file or processing data: {e}")
    for loc in locations:
        dates = pd.date_range(start="2018-01-01", end="2022-12-31", freq='M')
        ndvi = 0.3 + 0.3 * np.sin(np.linspace(0, 12*np.pi, len(dates))) + 0.05*np.random.randn(len(dates))
        ndvi = np.clip(ndvi, 0, 1)
        ndvi_data[loc] = pd.DataFrame({"date": dates, "ndvi": ndvi})

#Step 3: Plot NDVI trend for each location
for loc, df in ndvi_data.items():
    plt.figure()
    sns.lineplot(x='date', y='ndvi', data=df, marker='o', color='#2ca02c')
    plt.title(f'NDVI Trend for {loc}')
    plt.xlabel('Date')
    plt.ylabel('NDVI (Vegetation Index)')
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ======================
# Step 4: Fourier Series Prediction (Fixed with Amplitude Stretch) .......Used generative AI (ChatGPT) for this step.
# ======================
predictions = {}

def fourier_features(t, K=3, period=12):
    """Generate Fourier series terms up to order K"""
    features = []
    for k in range(1, K+1):
        features.append(np.sin(2 * np.pi * k * t / period))
        features.append(np.cos(2 * np.pi * k * t / period))
    return np.column_stack(features)

for loc, df in ndvi_data.items():
    df = df.copy()
    df['t'] = np.arange(len(df))  # month index

    #Add Fourier + bias + trend
    X = np.column_stack([
        np.ones(len(df)),                 # constant offset
        df['t'],                          # trend term
        fourier_features(df['t'], K=3)    # Fourier harmonics
    ])
    y = df['ndvi'].values

    model = LinearRegression()
    model.fit(X, y)

    #Predict next 12 months
    future_t = np.arange(len(df), len(df)+12)
    X_future = np.column_stack([
        np.ones(len(future_t)),
        future_t,
        fourier_features(future_t, K=3)
    ])
    pred_ndvi = model.predict(X_future)

    #Amplitude scaling
    hist_range = y.max() - y.min()
    pred_range = pred_ndvi.max() - pred_ndvi.min()
    if pred_range > 0:
        scale_factor = hist_range / pred_range
        pred_ndvi = (pred_ndvi - pred_ndvi.mean()) * scale_factor + pred_ndvi.mean()

    pred_ndvi = np.clip(pred_ndvi, 0, 1)
    predictions[loc] = pred_ndvi

    # Plot: past (green), future (orange, directly continuing)
    plt.figure()
    sns.lineplot(x='date', y='ndvi', data=df, marker='o', color='green', label='Past NDVI')
    future_dates = pd.date_range(start=df['date'].iloc[-1]+timedelta(days=30), periods=12, freq='M')
    sns.lineplot(x=future_dates, y=pred_ndvi, marker='o', color='orange', label='Predicted NDVI')

    # Connect last green point to first orange point
    plt.plot(
        [df['date'].iloc[-1], future_dates[0]],
        [df['ndvi'].iloc[-1], pred_ndvi[0]],
        color='orange'
    )

    plt.title(f'NDVI Prediction (Fourier Series) for {loc}')
    plt.xlabel('Date')
    plt.ylabel('NDVI')
    plt.ylim(0, 1)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Step 5: Interactive map with Folium.... Used generative AI (Chat GPT) for this step.
m = folium.Map(location=[0, 0], zoom_start=2, tiles='CartoDB positron')

for loc, coords in locations.items():
    folium.Marker(
        location=[coords['lat'], coords['lon']],
        popup=f"{loc} NDVI Prototype",
        icon=folium.Icon(color='green', icon='leaf')
    ).add_to(m)

m

# Step 6: charts for Figma prototype
import os
os.makedirs('charts', exist_ok=True)

for loc, df in ndvi_data.items():
    plt.figure()
    sns.lineplot(x='date', y='ndvi', data=df, marker='o', color='#2ca02c')
    future_dates = pd.date_range(start=df['date'].iloc[-1]+timedelta(days=30), periods=12, freq='M')
    sns.lineplot(x=future_dates, y=predictions[loc], marker='o', color='#ff7f0e')
    plt.title(f'NDVI Prediction (Fourier Series) for {loc}')
    plt.xlabel('Date')
    plt.ylabel('NDVI')
    plt.ylim(0,1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'charts/ndvi_{loc}.png')
    plt.close()

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
import os


warnings.filterwarnings('ignore')

class AgriculturalDataManager:
    def __init__(self):
        """
        Initializes the agricultural data manager.
        """
        self.monitoring_data = None
        self.weather_data = None
        self.soil_data = None
        self.yield_history = None
        self.parcels_data = None  # Add this line

    def load_data(self):
        """
        Loads all necessary datasets and parses dates where applicable.
        """
        try:
            self.monitoring_data = pd.read_csv('data/monitoring_cultures.csv', parse_dates=['date'])
            self.weather_data = pd.read_csv('data/meteo_detaillee.csv', parse_dates=['date'])
            self.soil_data = pd.read_csv('data/sols.csv')
            self.yield_history = pd.read_csv('data/historique_rendements.csv')
            self.parcels_data = self.monitoring_data.copy()  # Reuse monitoring data for parcels

            # Add 'predicted_yield' if missing
            if 'predicted_yield' not in self.parcels_data.columns:
                self.parcels_data['predicted_yield'] = np.random.uniform(5, 12, len(self.parcels_data))

            # Add 'crop_name' if missing
            if 'crop_name' not in self.parcels_data.columns:
                self.parcels_data['crop_name'] = ['Crop ' + str(i % 3 + 1) for i in range(len(self.parcels_data))]

        except FileNotFoundError as e:
            print(f"Error loading datasets: {e}")
            self.monitoring_data = None
            self.weather_data = None
            self.soil_data = None
            self.yield_history = None
            self.parcels_data = None




    def prepare_features(self):
        """Prepares data by merging monitoring, weather, and soil datasets."""
        # Merge monitoring and weather data
        merged_data = pd.merge_asof(
            self.monitoring_data.sort_values('date'),
            self.weather_data.sort_values('date'),
            on='date',
        )

        # Merge soil data
        merged_data = merged_data.merge(self.soil_data, on='parcelle_id', how='left')

        # Add 'annee' column derived from 'date'
        merged_data['annee'] = merged_data['date'].dt.year

        return merged_data

    def enrich_with_yield_history(self, data):
        """Enriches the data with historical yields."""
        enriched_data = data.merge(self.yield_history, on=['parcelle_id', 'annee'], how='left')
        return enriched_data

    def get_temporal_patterns(self, parcelle_id):
        """Analyzes temporal patterns for a specific parcelle_id."""
        parcelle_data = self.monitoring_data[self.monitoring_data['parcelle_id'] == parcelle_id]
        parcelle_data.set_index('date', inplace=True)

        # Compute a rolling mean for NDVI as an example
        parcelle_data['ndvi_rolling'] = parcelle_data['ndvi'].rolling(window=7, min_periods=1).mean()

        # Calculate trend metrics (example: linear regression)
        x = np.arange(len(parcelle_data))
        y = parcelle_data['ndvi'].values

        # Avoid issues if the dataset is too small
        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]  # Slope of the linear regression
            variation_mean = np.mean(y)    # Mean of the NDVI values
        else:
            slope = 0
            variation_mean = 0

        trend = {'pente': slope, 'variation_moyenne': variation_mean}
        return parcelle_data, trend

    def calculate_risk_metrics(self, data):
        """Calculates risk metrics based on weather and soil data."""
        data['drought_risk'] = data['precipitation'] < 10
        data['heat_risk'] = data['temperature'] > 35
        return data

    def analyze_yield_patterns(self, parcelle_id):
        """
        Performs advanced yield pattern analysis for a specific parcelle_id.
        """
        # Extract and prepare data
        history = self.yield_history[self.yield_history['parcelle_id'] == parcelle_id].copy()

        # Ensure data is sorted by year
        history.sort_values(by='annee', inplace=True)

        # Apply seasonal decomposition to yield data
        result = seasonal_decompose(history['rendement'], model='additive', period=1)

        # Return components for analysis
        return result.trend, result.seasonal, result.resid

if __name__ == "__main__":
    # Initialize the data manager
    data_manager = AgriculturalDataManager()

    # Load data
    data_manager.load_data()

    # Prepare features
    features = data_manager.prepare_features()

    # Enrich with yield history
    enriched_features = data_manager.enrich_with_yield_history(features)

    # Analyze temporal patterns for parcelle_id 'P001'
    parcelle_id = 'P001'
    temporal_patterns, trend = data_manager.get_temporal_patterns(parcelle_id)

    # Calculate risk metrics
    risk_metrics = data_manager.calculate_risk_metrics(features)

    # Advanced yield pattern analysis
    trend_component, seasonal_component, resid_component = data_manager.analyze_yield_patterns(parcelle_id)

    # Print outputs
    print("Sample Enriched Features:")
    print(enriched_features.head())

    print("\nTemporal Patterns for Parcelle 'P001':")
    print(temporal_patterns[['ndvi', 'ndvi_rolling']].head())

    print(f"\nTendance de rendement : {trend['pente']:.2f} tonnes/ha/an")
    print(f"Variation moyenne : {trend['variation_moyenne']*100:.1f}%")

    print("\nTendance générale :")
    print(trend_component)

    print("\nVariations saisonnières :")
    print(seasonal_component)

    print("\nRésidus :")
    print(resid_component)
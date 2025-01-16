import folium
from folium import plugins
from branca.colormap import LinearColormap
import pandas as pd

class AgriculturalMap:
    def __init__(self, data_manager):
        """
        Initialize the map with the data manager.

        The data manager must have loaded:
        - Parcelle data including latitude, longitude, and yield history
        """
        self.data_manager = data_manager
        self.map = None
        self.yield_colormap = LinearColormap(
            colors=['red', 'yellow', 'green'],
            vmin=0,
            vmax=12,  # Maximum yield in tonnes/ha
            caption="Yield (tonnes/ha)"
        )

    def create_base_map(self):
        """
        Create the base map centered on the parcels.
        """
        # Define the map's center and zoom level
        center_lat = self.data_manager.parcels_data['latitude'].mean()
        center_lon = self.data_manager.parcels_data['longitude'].mean()

        self.map = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    def add_yield_history_layer(self):
        """
        Add a layer visualizing the yield history for each parcel.
        """
        for _, row in self.data_manager.parcels_data.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=8,
                color=self.yield_colormap(row['predicted_yield']),
                fill=True,
                fill_opacity=0.7,
                popup=f"Crop: {row['crop_name']}<br>Yield: {row['predicted_yield']} tonnes/ha"
            ).add_to(self.map)

    def add_current_ndvi_layer(self):
        """
        Add a layer visualizing the current NDVI status for each parcel.
        """
        for _, row in self.data_manager.monitoring_data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"NDVI: {row['ndvi']}<br>Crop: {row['crop_name']}",
                icon=folium.Icon(color='green', icon='info-sign')
            ).add_to(self.map)

    def add_risk_heatmap(self):
        """
        Add a heatmap layer of risk zones.
        """
        heat_data = [
            [row['latitude'], row['longitude'], row['risk_score']]
            for _, row in self.data_manager.risk_data.iterrows()
        ]

        plugins.HeatMap(
            data=[[row[0], row[1]] for row in heat_data],
            radius=15,
            blur=10,
            max_zoom=1
        ).add_to(self.map)

    def save_map(self, filename="agricultural_map.html"):
        """
        Save the generated map to an HTML file.
        """
        self.map.save(filename)

# Mock data manager
class DataManager:
    def __init__(self):
        """
        Mock data manager to simulate data loading for the map.
        """
        self.parcels_data = pd.DataFrame({
            'latitude': [34.05, 34.07, 34.10],
            'longitude': [-6.83, -6.85, -6.80],
            'crop_name': ['Wheat', 'Corn', 'Soybean'],
            'predicted_yield': [8, 6, 10]
        })

        self.monitoring_data = pd.DataFrame({
            'latitude': [34.05, 34.07, 34.10],
            'longitude': [-6.83, -6.85, -6.80],
            'ndvi': [0.7, 0.6, 0.8],
            'crop_name': ['Wheat', 'Corn', 'Soybean']
        })

        self.risk_data = pd.DataFrame({
            'latitude': [34.05, 34.07, 34.10],
            'longitude': [-6.83, -6.85, -6.80],
            'risk_score': [0.4, 0.8, 0.3]
        })

# Main script to generate the map
if __name__ == "__main__":
    data_manager = DataManager()
    agri_map = AgriculturalMap(data_manager)

    agri_map.create_base_map()
    agri_map.add_yield_history_layer()
    agri_map.add_current_ndvi_layer()
    agri_map.add_risk_heatmap()

    # Save map to an HTML file
    agri_map.save_map("agricultural_map.html")
    print("Map has been generated and saved as 'agricultural_map.html'.")
import streamlit as st
from bokeh.embed import components
from bokeh.resources import CDN
from streamlit_folium import st_folium
from dashboard_richer_data_visualization_experience import AgriculturalDashboard
from map_visualization import AgriculturalMap
from data_manager import AgriculturalDataManager

class IntegratedDashboard:
    def __init__(self, data_manager):
        """
        Initializes the integrated dashboard, combining
        Bokeh visualizations and the Folium map.
        """
        self.data_manager = data_manager
        self.bokeh_dashboard = AgriculturalDashboard(data_manager)
        self.map_view = AgriculturalMap(data_manager)

    def initialize_visualizations(self):
        """
        Initializes all visual components.
        """
        # Initialize Bokeh visualizations
        self.bokeh_layout = self.bokeh_dashboard.create_layout()

        # Initialize Folium map and generate the HTML file
        self.map_view.create_base_map()
        self.map_view.add_yield_history_layer()
        self.map_view.add_current_ndvi_layer()
        self.map_view.add_risk_heatmap()

    def create_streamlit_dashboard(self):
        """
        Creates a Streamlit interface integrating all visualizations.
        """
        st.title("Tableau de Bord Agricole Intégré")

        # Render Bokeh visualizations in Streamlit
        st.subheader("Visualisations Bokeh")
        script, div = components(self.bokeh_layout, CDN)
        st.markdown(script, unsafe_allow_html=True)
        st.markdown(div, unsafe_allow_html=True)

        # Render Folium map in Streamlit
        st.subheader("Carte Interactive Folium")
        st_folium(self.map_view.map, width=700, height=500)

    def update_visualizations(self, parcelle_id):
        """
        Updates all visualizations for a selected parcel.
        """
        # Update Bokeh visualizations
        self.bokeh_dashboard.update_plots(None, None, parcelle_id)

        # Update Folium map layers
        self.map_view.add_yield_history_layer()
        self.map_view.add_current_ndvi_layer()

# Main script to run the integrated dashboard
if __name__ == "__main__":
    # Initialize the data manager and load data
    data_manager = AgriculturalDataManager()
    try:
        data_manager.load_data()
    except FileNotFoundError as e:
        st.error(f"Error loading datasets: {e}")
        st.stop()

    # Create integrated dashboard instance
    integrated_dashboard = IntegratedDashboard(data_manager)
    integrated_dashboard.initialize_visualizations()

    # Display the Streamlit dashboard
    integrated_dashboard.create_streamlit_dashboard()

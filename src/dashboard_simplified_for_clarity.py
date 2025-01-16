from bokeh.layouts import column
from bokeh.models import (ColumnDataSource, HoverTool)
from bokeh.plotting import figure, curdoc
from bokeh.palettes import RdYlBu11 as palette
import pandas as pd
import numpy as np

class AgriculturalDashboard:
    def __init__(self, data_manager):
        """
        Initialize the dashboard with the data manager

        The data manager (data_manager) must have loaded:
        - Current monitoring data
        - Historical yield data
        - Meteorological data
        - Soil characteristics
        """
        self.data_manager = data_manager
        self.source = None
        self.hist_source = None
        self.create_data_sources()

    def create_data_sources(self):
        """
        Prepare data sources for Bokeh by integrating current and historical data
        """
        monitoring_data = self.data_manager.monitoring_data
        self.source = ColumnDataSource(monitoring_data)

        yield_history = self.data_manager.yield_history
        self.hist_source = ColumnDataSource(yield_history)

    def create_yield_history_plot(self):
        """
        Create a plot showing historical yield evolution with annotations for important events
        """
        p = figure(title="Historique des Rendements par Parcelle",
                   x_axis_type="datetime",
                   height=400, width=800)

        p.line(x='annee', y='rendement', source=self.hist_source, line_width=2, color="blue", legend_label="Rendement")
        p.circle(x='annee', y='rendement', source=self.hist_source, size=8, color="blue")

        hover = HoverTool(tooltips=[("Année", "@annee{%F}"), ("Rendement", "@rendement")], formatters={"@annee": "datetime"})
        p.add_tools(hover)

        return p

    def create_ndvi_temporal_plot(self):
        """
        Create a plot showing NDVI evolution with historical thresholds
        """
        p = figure(title="Évolution du NDVI et Seuils Historiques",
                   x_axis_type="datetime",
                   height=400, width=800)

        p.line(x='date', y='ndvi', source=self.source, line_width=2, color="green", legend_label="NDVI")

        hover = HoverTool(tooltips=[("Date", "@date{%F}"), ("NDVI", "@ndvi")], formatters={"@date": "datetime"})
        p.add_tools(hover)

        return p

    def create_stress_matrix(self):
        """
        Create a stress matrix combining hydric stress and meteorological conditions
        """
        p = figure(title="Matrice de Stress",
                   x_range=(0, 1), y_range=(0, 1),
                   height=400, width=800)

        # Example stress matrix with dummy data
        x = [0.3, 0.5, 0.7]
        y = [0.3, 0.5, 0.7]
        stress = [0.1, 0.5, 0.9]
        colors = [palette[int(s * (len(palette) - 1))] for s in stress]

        p.rect(x=x, y=y, width=0.2, height=0.2, color=colors, alpha=0.7)

        return p

    def create_yield_prediction_plot(self):
        """
        Create a plot showing yield predictions based on historical and current data
        """
        p = figure(title="Prédiction des Rendements",
                   x_axis_type="datetime",
                   height=400, width=800)

        p.line(x='annee', y='prediction', source=self.hist_source, line_width=2, color="red", legend_label="Prédiction")

        hover = HoverTool(tooltips=[("Année", "@annee{%F}"), ("Prédiction", "@prediction")], formatters={"@annee": "datetime"})
        p.add_tools(hover)

        return p

    def create_layout(self):
        """
        Organize all plots into a coherent layout
        """
        yield_plot = self.create_yield_history_plot()
        ndvi_plot = self.create_ndvi_temporal_plot()
        stress_plot = self.create_stress_matrix()
        prediction_plot = self.create_yield_prediction_plot()

        layout = column(yield_plot, ndvi_plot, stress_plot, prediction_plot)
        return layout

class DataManager:
    def __init__(self):
        """
        Mock data manager to simulate data loading for the dashboard
        """
        self.monitoring_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=100),
            'ndvi': np.random.rand(100),
            'parcelle_id': ['P001'] * 100
        })
        self.yield_history = pd.DataFrame({
            'annee': pd.date_range(start='2020-01-01', periods=5, freq='Y'),
            'rendement': np.random.rand(5) * 10,
            'prediction': np.random.rand(5) * 10
        })

# Initialize the data manager and dashboard
data_manager = DataManager()
dash = AgriculturalDashboard(data_manager)

# Add the layout to the document
curdoc().add_root(dash.create_layout())
curdoc().title = "Tableau de Bord Agricole"
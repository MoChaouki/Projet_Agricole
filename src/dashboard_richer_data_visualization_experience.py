from bokeh.layouts import column, row, gridplot
from bokeh.models import (ColumnDataSource, Select, DateRangeSlider,
                          HoverTool, ColorBar, LinearColorMapper)
from bokeh.plotting import figure, curdoc
from bokeh.palettes import RdYlBu11 as palette
import bokeh.plotting as bk


class AgriculturalDashboard:
    def __init__(self, data_manager):
        """
        Initialise le tableau de bord avec le gestionnaire de données.
        
        Le gestionnaire de données (data_manager) doit avoir chargé :
        - Les données de monitoring actuelles
        - L’historique des rendements
        - Les données météorologiques
        - Les caractéristiques des sols
        """
        self.data_manager = data_manager
        self.source = None
        self.hist_source = None
        self.stress_source = None
        self.create_data_sources()

    def create_data_sources(self):
        """
        Prépare les sources de données pour Bokeh en intégrant
        les données actuelles et historiques.
        """
        # Source pour les données de monitoring
        monitoring_data = self.data_manager.monitoring_data

        # Source pour les données historiques des rendements
        yield_history = self.data_manager.yield_history

        # Créer des sources de données Bokeh
        self.source = ColumnDataSource(monitoring_data)
        self.hist_source = ColumnDataSource(yield_history)

        # Exemple de matrice de stress pour démonstration
        stress_data = {
            'x': [0.2, 0.5, 0.8],
            'y': [0.2, 0.5, 0.8],
            'stress': [0.1, 0.5, 0.9]
        }
        self.stress_source = ColumnDataSource(stress_data)

    def create_yield_history_plot(self):
        """
        Crée un graphique montrant l’évolution historique des rendements.
        """
        p = figure(title='Historique des Rendements par Parcelle',
                   x_axis_type='datetime',
                   height=400, width=800)

        p.line('annee', 'rendement', source=self.hist_source, line_width=2, color="blue", legend_label="Rendement")
        p.circle('annee', 'rendement', source=self.hist_source, size=8, color="blue")
        p.add_tools(HoverTool(tooltips=[("Année", "@annee"), ("Rendement", "@rendement")]))

        return p

    def create_ndvi_temporal_plot(self):
        """
        Crée un graphique montrant l’évolution du NDVI avec des seuils de référence.
        """
        p = figure(title='Évolution du NDVI et Seuils Historiques',
                   x_axis_type='datetime',
                   height=400, width=800)

        p.line('date', 'ndvi', source=self.source, line_width=2, color="green", legend_label="NDVI")
        p.add_tools(HoverTool(tooltips=[("Date", "@date{%F}"), ("NDVI", "@ndvi")],
                              formatters={"@date": "datetime"}))

        return p

    def create_stress_matrix(self):
        """
        Crée une matrice de stress combinant stress hydrique et conditions météorologiques.
        """
        p = figure(title='Matrice de Stress',
                   x_range=(0, 1), y_range=(0, 1),
                   height=400, width=800)

        mapper = LinearColorMapper(palette=palette, low=0, high=1)
        p.rect('x', 'y', width=0.1, height=0.1, source=self.stress_source,
               fill_color={'field': 'stress', 'transform': mapper})

        return p

    def create_yield_prediction_plot(self):
        """
        Crée un graphique de prédiction des rendements.
        """
        p = figure(title='Prédiction des Rendements',
                   x_axis_type='datetime',
                   height=400, width=800)

        # Exemple d'ajout de prédictions fictives
        p.line('annee', 'rendement', source=self.hist_source, line_width=2, color="red", legend_label="Prédiction")
        p.add_tools(HoverTool(tooltips=[("Année", "@annee"), ("Prédiction", "@rendement")]))

        return p

    def create_layout(self):
        """
        Organise tous les graphiques dans une mise en page cohérente.
        """
        yield_plot = self.create_yield_history_plot()
        ndvi_plot = self.create_ndvi_temporal_plot()
        stress_plot = self.create_stress_matrix()
        prediction_plot = self.create_yield_prediction_plot()

        layout = column(yield_plot, ndvi_plot, stress_plot, prediction_plot)
        return layout

    def update_plots(self, attr, old, new):
        """
        Met à jour tous les graphiques quand une nouvelle parcelle est sélectionnée.
        """
        parcelle_id = new
        updated_data = self.data_manager.monitoring_data[self.data_manager.monitoring_data['parcelle_id'] == parcelle_id]
        self.source.data = ColumnDataSource(updated_data).data

# Main code to run the Bokeh app
from data_manager import AgriculturalDataManager

data_manager = AgriculturalDataManager()
data_manager.load_data()

dash = AgriculturalDashboard(data_manager)
layout = dash.create_layout()

curdoc().add_root(layout)
curdoc().title = "Tableau de Bord Agricole"
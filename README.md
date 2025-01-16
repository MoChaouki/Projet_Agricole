# Projet_Agricole
# Projet Agricole Intégré

Ce projet vise à construire un tableau de bord intégré permettant de visualiser et d'analyser les données agricoles. Il combine des visualisations interactives en utilisant **Bokeh**, **Folium**, et **Streamlit**.

## Structure du Projet

```
projet_agricole/
│
├── data/                   # Contient les fichiers de données CSV nécessaires
├── notebooks/              # Pour les analyses exploratoires (facultatif)
├── reports/                # Contient les rapports ou documents générés
├── src/                    # Contient tous les fichiers Python pour le projet
│   ├── data_manager.py     # Gestion des données
│   ├── dashboard_richer_data_visualization_experience.py  # Visualisations avancées
│   ├── dashboard_simplified_for_clarity.py  # Visualisations simplifiées
│   ├── map_visualization.py  # Génération de cartes interactives
│   ├── integrated_dashboard.py  # Intégration complète avec Streamlit
│
├── templates/              # Contient des fichiers HTML générés (carte Folium)
├── venv/                   # Environnement virtuel Python (facultatif)
│
├── dashboard_richer_data_visualization_experience.py.jpg  # Capture d'écran du dashboard
├── dashboard_simplified_for_clarity.py.jpg                # Capture d'écran du dashboard simplifié
├── Documentation du Projet Tableau de Bord Agricole Intégré.docx  # Documentation complète
```

## Prérequis

1. **Python 3.7 ou version supérieure**
2. Installer les dépendances suivantes :
   - `pandas`
   - `numpy`
   - `scikit-learn`
   - `bokeh`
   - `folium`
   - `streamlit`
   - `branca`
   - `statsmodels`

## Installation

1. **Cloner le repository** :
   ```bash
   git clone https://github.com/votre-utilisateur/projet_agricole.git
   cd projet_agricole
   ```

2. **Configurer un environnement virtuel (recommandé)** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Linux/MacOS
   venv\Scripts\activate    # Sous Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Vérifier la structure des données** :
   Placez tous les fichiers CSV dans le dossier `data/` et assurez-vous que leurs noms correspondent aux fichiers référencés dans les scripts.

## Utilisation

1. **Lancer le tableau de bord intégré avec Streamlit** :
   ```bash
   streamlit run src/integrated_dashboard.py
   ```

2. **Ouvrir l'application** :
   Une URL locale sera affichée (exemple : `http://localhost:8501`), ouvrez-la dans un navigateur.

3. **Générer les cartes séparément** :
   Si nécessaire, exécutez `map_visualization.py` pour générer une carte HTML uniquement :
   ```bash
   python src/map_visualization.py
   ```

## Fonctionnalités

1. **Visualisations avancées avec Bokeh** :
   - Historique des rendements
   - Évolution du NDVI
   - Matrice de stress
   - Prédictions des rendements

2. **Carte interactive avec Folium** :
   - Localisation des parcelles
   - Statut NDVI
   - Carte de chaleur des zones à risque

3. **Intégration avec Streamlit** :
   - Interface utilisateur pour visualiser toutes les données dans un seul tableau de bord

## Problèmes connus

- Certaines fonctionnalités peuvent être limitées si les données ne sont pas complètes ou correctement formatées.
- Le projet n'est pas terminé à 100% en raison de contraintes de temps et d'obstacles techniques.
- 
## Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser et de le modifier.

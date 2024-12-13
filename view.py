import panel as pn
import folium as fl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class View_example:
    def __init__(self, model):
        """initialise view object with the model data as a self property"""

        self.model = model
        return

    def create_alerts(self):
        """create confirmed working alerts (tested in app.py)"""

        alert_pandas_version = pn.pane.Alert(f"Current pandas version: {pd.__version__}")
        alert_page1 = pn.pane.Alert("Representation of the dataframe")

        return alert_pandas_version, alert_page1

    def create_map(self):
        """create interactive map with markers centered on the mean of all unique coordinates"""

        mean_coords = self.model.mean_coordinates 

        coord_map = fl.Map(location=[mean_coords["Latitude (WGS-84)"], mean_coords["Longitude (WGS-84)"]], zoom_start=6)

        # for loop for generating markers on all the unique coords
        # has to be done like this because you can only create one marker at a time
        for lat, lng, project in zip(
            self.model.unique_coordinates_df["Latitude (WGS-84)"],
            self.model.unique_coordinates_df["Longitude (WGS-84)"],
            self.model.df.loc[self.model.unique_coordinates_df.index]["Project"]
        ):
            fl.Marker([lat, lng], popup=project, tooltip="Click for project").add_to(coord_map)

        return pn.pane.plot.Folium(coord_map, height=400)
    

    def create_plots(self):
        """create plots for unique values and N/A- value distribution"""

        # Unique values plot
        unique_counts = self.model.df.nunique()
        plt.figure(figsize=(15, 8))
        unique_counts.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.xlabel("Columns")
        plt.ylabel("Number of Unique Values")
        plt.title("Unique Values per Column")
        plt.xticks(ticks=range(len(unique_counts.index)) ,ha="right" ,va="top", labels=unique_counts.index, rotation=45)
        plt.yscale('log')
        plt.axhline(y=239320, color='red', linestyle='--', linewidth=2, label='Total Rows')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        unique_values_plot = pn.pane.Matplotlib(plt.gcf(), dpi=100)

        # N/A-ish values distribution
        na_counts, actual_counts = self.model.count_na_and_actual_values()
        fig, ax = plt.subplots(figsize=(15, 8))
        index = np.arange(len(na_counts))
        ax.bar(index, na_counts.values(), label='N/A-like Values', color='red')
        ax.bar(index, actual_counts.values(), bottom=list(na_counts.values()), label='Actual Values', color='blue')
        ax.set_xticks(index)
        ax.set_xticklabels(self.model.df.columns ,ha="right" ,va="top" ,rotation=45)
        ax.set_title("N/A-like vs Actual Values per Column")
        plt.tight_layout()
        na_values_plot = pn.pane.Matplotlib(plt.gcf(), dpi=100)

        return unique_values_plot, na_values_plot
    
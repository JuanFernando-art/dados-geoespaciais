import folium
import os

class Visualizer:
    @staticmethod
    def plot_folium(gdf, filepath="mapa_interativo.html"):
        if gdf.empty:
            raise ValueError("GeoDataFrame está vazio.")

        center = gdf.geometry.unary_union.centroid
        m = folium.Map(location=[center.y, center.x], zoom_start=12)

        for _, row in gdf.iterrows():
            geom = row.geometry
            nome = row.get("nome", "Local")

            if geom.geom_type == 'Point':
                folium.Marker([geom.y, geom.x], popup=nome).add_to(m)
            elif geom.geom_type == 'LineString':
                folium.PolyLine([[pt[1], pt[0]] for pt in geom.coords], popup=nome).add_to(m)
            elif geom.geom_type == 'Polygon':
                folium.Polygon([[pt[1], pt[0]] for pt in geom.exterior.coords], popup=nome).add_to(m)

        m.save(filepath)
        return os.path.abspath(filepath)

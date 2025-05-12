import pandas as pd
import geopandas as gpd
import json
import xml.etree.ElementTree as ET
from shapely.geometry import Point

class DataProcessor:
    def __init__(self):
        self.data = None

    def load_csv(self, file_path):
        df = pd.read_csv(file_path)

        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            raise ValueError("O CSV deve conter colunas 'latitude' e 'longitude'.")

        self.data = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
            crs="EPSG:4326"
        )

    def load_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.data = gpd.GeoDataFrame.from_features(data["features"], crs="EPSG:4326")

    def load_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        features = []
        for item in root.findall(".//local"):
            lat = item.findtext("latitude")
            lon = item.findtext("longitude")
            nome = item.findtext("nome") or "Sem nome"
            if lat and lon:
                point = Point(float(lon), float(lat))
                features.append({"nome": nome, "geometry": point})

        if not features:
            raise ValueError("Nenhum dado geoespacial encontrado no XML.")

        self.data = gpd.GeoDataFrame(features, crs="EPSG:4326")

    def get_data(self):
        if self.data is None:
            raise ValueError("Nenhum dado carregado.")
        return self.data

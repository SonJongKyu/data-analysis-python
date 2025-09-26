
# -*- coding: utf-8 -*-
"""
서울도서관 분석 - 코드별 스크립트
원본 워크북의 셀을 주제/기능별로 스크립트로 분리하여 GitHub 업로드용 구조로 재구성했습니다.
각 스크립트는 상대경로의 CSV/GeoJSON 파일을 사용합니다. (./data, ./maps 폴더)
"""
import warnings
warnings.filterwarnings("ignore")

import json
import folium
from folium.plugins import HeatMap
from utils import ensure_dirs, read_csv_cp949, MAPS_DIR, OUTPUT_DIR

ensure_dirs()

libraries = read_csv_cp949("서울시 공공도서관 현황정보.csv")
m = folium.Map(location=[37.5665,126.9780], zoom_start=11)

heat_data = [[row["위도"], row["경도"]] for _, row in libraries.iterrows()]
HeatMap(heat_data).add_to(m)

geo_path = f"{MAPS_DIR}/서울_자치구_경계_2017.geojson"
if os.path.exists(geo_path):
    with open(geo_path, "r", encoding="utf-8") as f:
        geo_data = json.load(f)
    folium.Choropleth(geo_data=geo_data, fill_opacity=0, line_opacity=0.8).add_to(m)

m.save(f"{OUTPUT_DIR}/library_heatmap.html")

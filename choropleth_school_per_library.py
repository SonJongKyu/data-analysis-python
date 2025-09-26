
# -*- coding: utf-8 -*-
"""
서울도서관 분석 - 코드별 스크립트
원본 워크북의 셀을 주제/기능별로 스크립트로 분리하여 GitHub 업로드용 구조로 재구성했습니다.
각 스크립트는 상대경로의 CSV/GeoJSON 파일을 사용합니다. (./data, ./maps 폴더)
"""
import warnings
warnings.filterwarnings("ignore")

import os, json
import matplotlib.pyplot as plt
import folium
from shapely.geometry import shape
import pandas as pd
from utils import ensure_dirs, read_csv_cp949, MAPS_DIR, OUTPUT_DIR

ensure_dirs()

libraries = read_csv_cp949("서울시 공공도서관 현황정보.csv")
schools = read_csv_cp949("서울시 학교 기본정보_통합.csv")

lib_cnt = libraries.groupby("구명").size().reset_index(name="도서관 수")
sch_cnt = schools.groupby("행정구").size().reset_index(name="학교 수")
merged = pd.merge(lib_cnt, sch_cnt, left_on="구명", right_on="행정구")
merged["비율"] = merged["학교 수"] / merged["도서관 수"]

# Choropleth
geo_path = os.path.join(MAPS_DIR, "서울_자치구_경계_2017.geojson")
m = folium.Map(location=[37.5665,126.9780], zoom_start=11)
if os.path.exists(geo_path):
    with open(geo_path, encoding="utf-8") as f:
        geo = json.load(f)
    folium.Choropleth(
        geo_data=geo, data=merged, columns=["구명","비율"],
        key_on="feature.properties.SIG_KOR_NM",
        fill_color="OrRd", fill_opacity=0.7, line_opacity=0.2,
        legend_name="학교 수 / 도서관 수 비율",
        threshold_scale=[0,5,7,9,11,15]
    ).add_to(m)
m.save(f"{OUTPUT_DIR}/school_per_library_choropleth.html")

# 비교 차트
import matplotlib.pyplot as plt
plt.rc("font", family="Malgun Gothic")
fig, ax1 = plt.subplots(figsize=(11,6))
ax1.bar(merged["행정구"], merged["학교 수"], label="학교 수")
ax1.set_xlabel("지역구명"); ax1.set_ylabel("학교 수")
ax1.tick_params(axis="x", rotation=45)
ax2 = ax1.twinx()
ax2.bar(merged["행정구"], merged["도서관 수"], alpha=0.7, label="도서관 수")
plt.title("서울 각 구별 학교 수와 도서관 수 비교")
fig.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/school_vs_library.png", dpi=150)

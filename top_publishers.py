
# -*- coding: utf-8 -*-
"""
서울도서관 분석 - 코드별 스크립트
원본 워크북의 셀을 주제/기능별로 스크립트로 분리하여 GitHub 업로드용 구조로 재구성했습니다.
각 스크립트는 상대경로의 CSV/GeoJSON 파일을 사용합니다. (./data, ./maps 폴더)
"""
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
from utils import ensure_dirs, read_csv_utf8, OUTPUT_DIR

ensure_dirs()

df = read_csv_utf8("popular_books_clean.csv")  # ingest에서 생성됨
top10 = df.groupby("발행처").size().sort_values(ascending=False).head(10)

plt.rcParams["font.family"] = "Malgun Gothic"
plt.figure(figsize=(10,6))
plt.barh(top10.index, top10.values)
plt.xlabel("대출 도서 수"); plt.title("출판사별 인기 대출 도서 수 (Top 10)")
plt.tight_layout(); plt.savefig(f"{OUTPUT_DIR}/top_publishers.png", dpi=150)

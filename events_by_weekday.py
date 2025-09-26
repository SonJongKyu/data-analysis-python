
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
from utils import ensure_dirs, read_csv_cp949, OUTPUT_DIR

ensure_dirs()

events = read_csv_cp949("서울도서관강좌및일정정제.csv")
events["날짜 처음"] = pd.to_datetime(events["날짜 처음"], format="%Y%m%d", errors="coerce")
events["요일"] = events["날짜 처음"].dt.day_name()
counts = events["요일"].value_counts()

plt.rcParams["font.family"] = "Malgun Gothic"
plt.figure(figsize=(8,6))
counts.plot(kind="bar")
plt.title("요일별 행사 수"); plt.xlabel("요일")
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/events_by_weekday.png", dpi=150)

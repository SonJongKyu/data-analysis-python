
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

loans = read_csv_utf8("서울도서관 대출정보_20240701_20240831.csv")
loans["대출일자"] = pd.to_datetime(loans["대출일자"], errors="coerce")

plt.figure(figsize=(11,6))
plt.plot(loans["대출일자"], loans["대출횟수"], marker="o")
plt.xlabel("대출일자"); plt.ylabel("대출횟수"); plt.title("일자별 대출횟수")
plt.xticks(rotation=90); plt.grid(True); plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/daily_loans.png", dpi=150)

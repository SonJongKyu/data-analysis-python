
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

df = read_csv_cp949("서울도서관 소장자료 현황정보.csv")

# 필터
df = df[
    df["출판사"].astype(str).str.contains("[가-힣]") &
    df["자료명"].astype(str).str.contains("[가-힣A-Za-z]") &
    df["청구기호"].astype(str).str.match("^[0-9]")
].copy()

def convert_cat(code: str):
    code = str(code)
    if not code:
        return None
    key = code[0] + "00"
    mapping = {
        "000":"총류","100":"철학","200":"종교","300":"사회과학",
        "400":"순수과학","500":"기술과학","600":"예술",
        "700":"언어","800":"문학","900":"역사"
    }
    return mapping.get(key)

df["분류"] = df["청구기호"].astype(str).apply(convert_cat)
cnt = df.groupby("분류")["자료코드"].count().sort_index()

# 막대
plt.rcParams["font.family"] = "Malgun Gothic"
ax = cnt.plot(kind="bar", figsize=(10,6))
ax.set_xlabel("도서분야(장르)"); ax.set_title("서울도서관 소장도서 분야별 권수")
plt.tight_layout(); plt.savefig(f"{OUTPUT_DIR}/holdings_by_class_bar.png", dpi=150)

# 파이
plt.figure(figsize=(8,8))
plt.pie(cnt.values, labels=cnt.index, autopct="%0.1f%%")
plt.title("서울도서관 소장도서 분야별 비율")
plt.tight_layout(); plt.savefig(f"{OUTPUT_DIR}/holdings_by_class_pie.png", dpi=150)

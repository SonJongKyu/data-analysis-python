
# -*- coding: utf-8 -*-
"""
서울도서관 분석 - 코드별 스크립트
원본 워크북의 셀을 주제/기능별로 스크립트로 분리하여 GitHub 업로드용 구조로 재구성했습니다.
각 스크립트는 상대경로의 CSV/GeoJSON 파일을 사용합니다. (./data, ./maps 폴더)
"""
import warnings
warnings.filterwarnings("ignore")

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MAPS_DIR = os.path.join(os.path.dirname(__file__), "..", "maps")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MAPS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def read_csv_cp949(name, **kwargs):
    """data 폴더의 CSV를 cp949로 읽습니다."""
    path = os.path.join(DATA_DIR, name)
    return pd.read_csv(path, encoding=kwargs.pop("encoding", "cp949"), **kwargs)

def read_csv_utf8(name, **kwargs):
    """data 폴더의 CSV를 utf-8로 읽습니다."""
    path = os.path.join(DATA_DIR, name)
    return pd.read_csv(path, encoding=kwargs.pop("encoding", "utf-8"), **kwargs)

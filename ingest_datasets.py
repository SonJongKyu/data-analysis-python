
# -*- coding: utf-8 -*-
"""
서울도서관 분석 - 코드별 스크립트
원본 워크북의 셀을 주제/기능별로 스크립트로 분리하여 GitHub 업로드용 구조로 재구성했습니다.
각 스크립트는 상대경로의 CSV/GeoJSON 파일을 사용합니다. (./data, ./maps 폴더)
"""
import warnings
warnings.filterwarnings("ignore")

"""
- 서울도서관 강좌/일정 정제 CSV 로드
- 서울시 공공도서관 현황정보 로드
- 서울 인구수 로드
- 서울도서관 대출정보 (7~8월) 전처리 및 일자별 집계
- 최근 60일 인기 대출 도서 발행처 표준화
"""
import re
import pandas as pd
from utils import ensure_dirs, read_csv_cp949, read_csv_utf8, OUTPUT_DIR

ensure_dirs()

# 1) 강좌/일정
events = read_csv_cp949("서울도서관강좌및일정정제.csv")
events.to_csv(f"{OUTPUT_DIR}/events_clean.csv", index=False)

# 2) 공공도서관 현황
libraries = read_csv_cp949("서울시 공공도서관 현황정보.csv", usecols=["도서관명","구명","위도","경도"])
libraries.to_csv(f"{OUTPUT_DIR}/libraries_clean.csv", index=False)

# 3) 서울 인구수 (utf-8, 첫 행 스킵)
pop = read_csv_utf8("서울 인구수.csv", skiprows=1)[["행정구역별(읍면동)", "총인구 (명)"]]
pop = pop.rename(columns={"행정구역별(읍면동)":"구명","총인구 (명)":"인구"})
pop.to_csv(f"{OUTPUT_DIR}/population_by_gu.csv", index=False)

# 4) 7~8월 대출정보: 사전 집계본 사용 (원본 7,8월 파일을 합쳐 집계한 결과라고 가정)
loans = read_csv_utf8("서울도서관 대출정보_20240701_20240831.csv")
# 일자 형식 보정
if "대출일자" in loans.columns:
    loans["대출일자"] = pd.to_datetime(loans["대출일자"], errors="coerce")
loans.to_csv(f"{OUTPUT_DIR}/loans_20240701_20240831.csv", index=False)

# 5) 인기 대출 도서 발행처 표준화
books = read_csv_cp949("대출 많은 책.csv")
publisher_mapping = {
    "북이십일": ["북이십일","아울북","21세기북스"],
    "다산북스": ["다산"],
    "매일경제": ["매일경제"],
    "불광": ["불광"],
    "유노북스": ["유노콘텐츠그룹"],
    "폴라웍스": ["폴라웍스"],
    "해시태그": ["해시태그"],
    "성안당": ["성안당"],
    "시원스쿨닷컴": ["에스제이더블유"],
    "아침사과": ["아침사과"],
    "청림출판": ["청림출판"],
    "포레스트북스": ["포레스트북스"],
    "페이지2북스": ["페이지2북스"],
    "영진닷컴": ["영진닷컴"],
    "동양북스": ["동양북스"],
    "샘터": ["샘터"],
    "어크로스": ["어크로스"],
    "위즈덤하우스": ["위즈덤하우스"],
    "이지스퍼블리싱": ["이지스퍼블리싱"],
    "한겨레출판": ["한겨레출판"],
    "단꿈아이": ["단꿈아이"],
    "김영사": ["김영사"],
    "다락원": ["다락원"],
    "웅진씽크빅": ["웅진"],
    "두란노": ["두란노"],
    "하이스트": ["하이스트","비전비엔피"],
    "제이펍": ["제이펍"],
    "바이포엠": ["바이포엠"],
    "미래엔": ["미래엔"],
    "넥서스": ["넥서스"],
    "대원씨아이": ["대원씨아이"],
    "북하우스": ["북하우스"],
    "사람in": ["사람in"],
    "상상아카데미": ["상상아카데미"],
    "파란정원": ["파란정원"],
    "휴머니스트": ["휴머니스트"],
    "문학동네": ["문학동네"],
    "국일증권경제연구소": ["국일증권경제연구소"],
    "규장": ["규장"],
    "시공사": ["시공사"],
    "필름": ["필름"],
    "디자인사강": ["디자인사강"],
    "골든래빗": ["골든래빗"],
    "길벗": ["길벗"],
    "중앙books": ["중앙books"],
    "경향BP": ["경향BP"],
    "로크미디어": ["로크미디어"],
    "돌핀북": ["돌핀북"],
    "EBS": ["EBS","이비에스"],
    "Penguin": ["Penguin"],
    "문학사상": ["문학사상"],
    "백도씨": ["백도씨"],
    "생각의길": ["생각의길"],
    "푸른숲": ["푸른숲"],
    "양철북": ["양철북"],
    "에이콘": ["에이콘"],
    "박영사": ["박영사","박영story"],
}

def normalize_publisher(val: str) -> str:
    if not isinstance(val, str):
        return val
    for new_pub, variants in publisher_mapping.items():
        for v in variants:
            if v in val:
                return new_pub
    return val

if "발행처" in books.columns:
    books["발행처"] = books["발행처"].apply(normalize_publisher)
books.to_csv(f"{OUTPUT_DIR}/popular_books_clean.csv", index=False)

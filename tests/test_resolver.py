from dateling import DatelingResolver

def test_cases():
    resolver = DatelingResolver()

    examples = [
        # 기존 v1.0 ~ v1.1 테스트 케이스
        "{today}",
        "{today -1d}",
        "{today +5d}",
        "{today -2m}",
        "{today +1m}",
        "{today -3y}",
        "{today +1y}",
        "{20250101 -3y}",
        "{2025-06-01 +2m}",
        "{today | year_start}",
        "{today | year_end}",
        "{today -1y | year_start}",
        "{today -1y | year_end}",
        "{today | year=nearest_year, month=03, day=10}",
        "{today -1y | year=nearest_year, month=03, day=10}",
        "{today | year=nearest_year, month=12, day=31}",
        "{year=2023, month=05, day=15}",
        "2025-01-01",
        "20250101",
        "{1000-01-01 +30y | year_end}",

        # v1.2 신규 기능 테스트
        "{first_date_of_this_month}",
        "{monday_of_this_week}",
        "${today -7d}",  # ${} 구문 지원 테스트
        "${first_date_of_this_month}",
        "${monday_of_this_week}",
        "{first_date_of_this_month}",
        "{monday_of_this_week}",
        "{today | year_start}",
        "{today | year_end}",
        "{today -1y | year_start}",
        "{today -1y | year_end}",
        "{monday_of_this_week -365d | year=year_start}",
        "{today -1y | year=nearest_year, month=03, day=10}",
        "{today | year=nearest_year, month=12, day=31}",
        "{year=2023, month=05, day=15}",
        "2025-01-01",
        "20250101",
        "{1000-01-01 +30y | year_end}",
        # v1.3 신규 기능 테스트 (month=nearest_month)
        "{today | year=nearest_year, month=nearest_month, day=10}",
        "{today -1y | year=nearest_year, month=nearest_month, day=10}",
        "{today +1y | year=nearest_year, month=nearest_month, day=10}",
        "{today | year=nearest_year, month=nearest_month, day=1}"
        # v1.3.1 신규 기능 테스트 (month=nearest_month)
        "{first_date_of_this_year}",
        "${first_date_of_this_year}",
        # v1.3.2 신규 기능 테스트 (계산 토큰 앞 띄워쓰기 인식)
        "{today + 1d}",
        "${today - 1d}",
        # v1.4.0 신규 기능 테스트 (주 단위 계산)
        "${today -1w}",  # 1주 전
        "${today -2w}",  # 2주 전
        "{today -1w}",  # 1주 전 (다른 형식)
        "${today +1w}",  # 1주 후
        "${today -1d}",  # 1일 전
        "${today -1m}",  # 1개월 전
        "${today -1y}",  # 1년 전
        "{today}",  # 오늘
        # 요일 앵커들 - 기존 형식
        "{last_friday}",  # 지난주 금요일
        "{last_monday}",  # 지난주 월요일
        "{friday}",  # 이번주 금요일
        "{monday}",  # 이번주 월요일
        "{saturday}",  # 이번주 토요일
        "{sunday}",  # 이번주 일요일
        # 요일 앵커들 - 새로운 형식 (this_week)
        "{monday_of_this_week}",  # 이번주 월요일
        "{tuesday_of_this_week}",  # 이번주 화요일
        "{wednesday_of_this_week}",  # 이번주 수요일
        "{thursday_of_this_week}",  # 이번주 목요일
        "{friday_of_this_week}",  # 이번주 금요일
        "{saturday_of_this_week}",  # 이번주 토요일
        "{sunday_of_this_week}",  # 이번주 일요일
        # 요일 앵커들 - 새로운 형식 (last_week)
        "{monday_of_last_week}",  # 지난주 월요일
        "{tuesday_of_last_week}",  # 지난주 화요일
        "{wednesday_of_last_week}",  # 지난주 수요일
        "{thursday_of_last_week}",  # 지난주 목요일
        "{friday_of_last_week}",  # 지난주 금요일
        "{saturday_of_last_week}",  # 지난주 토요일
        "{sunday_of_last_week}",  # 지난주 일요일
        # 요일 앵커 + 오프셋 조합
        "{last_friday +1w}",  # 지난주 금요일 + 1주 = 이번주 금요일
        "{friday -1w}",  # 이번주 금요일 - 1주 = 지난주 금요일
    ]

    for ex in examples:
        try:
            result = resolver.resolve(ex)
            formatted_result = resolver.resolve_and_format_date(ex)
            print(f"{ex} → {result} → {formatted_result}")
        except Exception as e:
            print(f"{ex} → ERROR: {e}")

if __name__ == "__main__":
    test_cases()

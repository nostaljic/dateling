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
    ]

    for ex in examples:
        try:
            result = resolver.resolve(ex)
            print(f"{ex} → {result}")
        except Exception as e:
            print(f"{ex} → ERROR: {e}")

if __name__ == "__main__":
    test_cases()

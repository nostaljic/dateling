from dateling import DatelingResolver

def test_cases():
    resolver = DatelingResolver()

    examples = [
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
        "{today | year=infer_year, month=03, day=10}",
        "{today -1y | year=infer_year, month=03, day=10}",
        "{today | year=infer_year, month=12, day=31}",
        "{year=2023, month=05, day=15}",
        "2025-01-01",
        "20250101",
        "{1000-01-01 +30y | year_end}",
    ]

    for ex in examples:
        print(f"{ex} → {resolver.resolve(ex)}")

if __name__ == "__main__":
    test_cases()

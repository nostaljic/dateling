# dateling

**dateling: A DSL parser and resolver for normalized date expressions**

`dateling` provides a formalized expression language and grammar for handling relative and absolute date computations.  
It defines a structured Date DSL (Domain-Specific Language) and provides a parser that resolves these expressions into actual dates.

The name **dateling** combines **date** and **handling**, representing its core purpose: structured date handling.

---

## ✅ Date Expression DSL

**Format:**


### Anchors

- `today` (current date)
- `YYYYMMDD` (e.g., `20250101`)
- `YYYY-MM-DD` (e.g., `2025-01-01`)

### Offsets

- `+Nd`, `-Nd` → days
- `+Nm`, `-Nm` → months
- `+Ny`, `-Ny` → years

### Modifiers

- `year_start` → start of year
- `year_end` → end of year
- `year=infer_year` → use anchor year; if resulting date is in future, fallback to previous year
- `year=YYYY` → explicit year override
- `month=MM` → month override
- `day=DD` → day override

---

## ✅ Examples

| DSL Expression | Meaning |
|---|---|
| `{today}` | today's date |
| `{today - Nd}` | N days ago |
| `{today - Ny}` | N years ago |
| `{today | year_start}` | start of current year |
| `{today | year=infer_year, month=MM, day=DD}` | month/day on anchor year, fallback to previous year if in future |
| `{today -1y | year_end}` | end of last year |

---

## ✅ Test Examples (executed on 2025-06-11)

| DSL | Resolved Date |
|---|---|
| `{today}` | 2025-06-11 |
| `{today -1d}` | 2025-06-10 |
| `{today -365d | year=infer_year}` | 2024-06-11 |
| `{today -3y}` | 2022-06-11 |
| `{today | year_start}` | 2025-01-01 |
| `{today | year_end}` | 2025-12-31 |
| `{today -1y | year_start}` | 2024-01-01 |
| `{today -1y | year_end}` | 2024-12-31 |
| `{today | year=infer_year, month=06, day=10}` | 2025-06-10 |
| `{today -1y | year=infer_year, month=03, day=10}` | 2024-03-10 |
| `{today | year=2024, month=06, day=10}` | 2024-06-10 |
| `{year=2022, month=05, day=15}` | 2022-05-15 |
| `2025-01-01` | 2025-01-01 |
| `20250101` | 2025-01-01 |
| `{1000-01-01 +30y | year_end}` | 1030-12-31 |
| `{today -36m}` | 2022-06-11 |
| `{today | year=infer_year, month=06, day=10}` | 2025-06-10 |

---

## ✅ Install

```bash
pip install dateling
```

---

## ✅ Usage

```python
from dateling import DatelingResolver

resolver = DatelingResolver()
date = resolver.resolve("{today -1y | year_start}")
print(date)
```

---

## ✅ License
MIT License

---

✅ Purpose
- Fully normalized date expression language (DSL)
- Precise parsing and evaluation of relative and absolute date computations
- Designed for any system that needs structured time computations:
    - search systems
    - reporting tools
    - schedulers
    - time-based data processing
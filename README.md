# dateling

🕰 **dateling — A Time Expression DSL and parser for deterministic date calculations.**

`dateling` provides a normalized formal language (DSL) to represent and resolve date calculations using structured expressions.  
Instead of parsing ambiguous natural language, it offers a precise syntax to express relative and absolute dates, compute date ranges, and perform robust date arithmetic.

The name `dateling` comes from combining **date** and **handling**.

---

## 🚀 Why dateling?

Most existing packages like `dateparser` or `parsedatetime` try to interpret free-text natural language into dates.  
In contrast, `dateling` takes a **strict, declarative, and composable approach**, offering:

- ✅ Predictable & reproducible date evaluation
- ✅ Fully composable date expressions
- ✅ Explicit syntax without ambiguity
- ✅ Ideal for any system requiring controlled time range calculations
- ✅ No natural language processing — purely deterministic time logic

---

## 📦 What's New in v1.2 & v1.3

### ✅ v1.2 Updates:

- Added `${}` support as an alternative bracket style to `{}`.
- Added new anchor keywords:
  - `first_date_of_this_month` — resolves to the first day of the current month.
  - `monday_of_this_week` — resolves to the Monday of the current week.

### ✅ v1.3 Updates:

- Added `month=nearest_month` modifier.
  - Similar to `year=nearest_year`, but applies nearest-month logic.
  - If the resolved date falls into the future, fallback to previous month (and adjust year if necessary).
- Further improved composability of partial expressions (ex: "11일의 주가 알려줘" → `{today | year=nearest_year, month=nearest_month, day=11}`).

### ✅ v1.3.1 Updates:
- Added new anchor keywords:
  - `first_date_of_this_year` — resolves to the first day of the current year.

### ✅ v1.3.2 Updates:
- Supports for blank after (+/-) sign:
  - now supports for `{today + 1d}`
네! **기존 README 포맷을 그대로 유지하면서**
\*\*변경된 지원 기능(week offset, full weekday anchors 등)\*\*이 반영된 DSL 문서 형식 예시로 맞춰드릴게요.

---

### ✅ v1.4 Updates:

* Added support for week (`w`) offset unit:

  * Now supports `{today -1w}`, `{monday +2w}`, etc.
* Added full weekday anchors:

  * Now supports `{monday}`, `{tuesday}`, ..., `{sunday}` for this week.
  * Also supports `{monday_of_this_week}`, `{last_friday}`, `{wednesday_of_last_week}`, etc.
* Allows blank after `+`/`-` sign (e.g. `{today + 1w}`).

---

## 📅 DSL Syntax

The general expression format is:

```text
{anchor [+/- offset] | [modifiers]}
```

### Anchors:

* `today` (system reference date)
* `first_date_of_this_year`
* `first_date_of_this_month`
* `monday_of_this_week`, `tuesday_of_this_week`, ..., `sunday_of_this_week`
* `monday`, `tuesday`, ..., `sunday` (this week)
* `last_monday`, ..., `last_sunday` (previous week)
* `monday_of_last_week`, ..., `sunday_of_last_week`
* `YYYYMMDD` (e.g. `20250101`)
* `YYYY-MM-DD` (e.g. `2025-01-01`)
* `{year=YYYY, month=MM, day=DD}` (absolute date)

### Offsets:

* Days: `+Nd`, `-Nd`
* Weeks: `+Nw`, `-Nw`    ← **NEW**
* Months: `+Nm`, `-Nm`
* Years: `+Ny`, `-Ny`
* (Spaces after `+`/`-` are allowed, e.g. `{today + 1w}`)

### Modifiers:

* `year_start` → resolves to start of year
* `year_end` → resolves to end of year
* `year=nearest_year` → use anchor year, fallback to previous year if resulting date is in the future
* `year=YYYY` → explicitly set year
* `month=nearest_month` → anchor month, fallback to previous month if resulting date is in the future
* `month=MM` → override month
* `day=DD` → override day

---

## 📊 Examples

| DSL Expression                  | Meaning                                 |                                                      |
| ------------------------------- | --------------------------------------- | ---------------------------------------------------- |
| `{today}`                       | today's date                            |                                                      |
| `${today}`                      | today's date                            |                                                      |
| `{today -1d}`                   | 1 day before today                      |                                                      |
| `{today -1w}`                   | 1 week before today                     |                                                      |
| `{today + 2w}`                  | 2 weeks after today                     |                                                      |
| `{monday}`                      | Monday of this week                     |                                                      |
| `{sunday_of_this_week}`         | Sunday of this week                     |                                                      |
| `{last_friday}`                 | Friday of last week                     |                                                      |
| `{tuesday_of_last_week}`        | Tuesday of last week                    |                                                      |
| `{today -1y \| year_start}` | start of year, 1 year ago | |
| `{2025-01-01 +30y \| year_end}` | year-end of 30 years after Jan 1, 2025 | |
| `{today \| year=nearest_year, month=03, day=10}` | March 10 of anchor year (or previous year if future) | |
| `{year=2023, month=05, day=15}` | absolute date                           |                                                      |
| `2025-01-01`                    | absolute date                           |                                                      |
| `20250101`                      | absolute date                           |                                                      |

---

## 🔬 Evaluation Example (Reference date: 2025-07-22)

| DSL                             | Output                                  |            |
| ------------------------------- | --------------------------------------- | ---------- |
| `{today}`                       | 2025-07-22                              |            |
| `{today -1d}`                   | 2025-07-21                              |            |
| `{today -1w}`                   | 2025-07-15                              |            |
| `{today +2w}`                   | 2025-08-05                              |            |
| `{monday}`                      | 2025-07-21                              |            |
| `{last_sunday}`                 | 2025-07-20                              |            |
| `{tuesday_of_last_week}`        | 2025-07-15                              |            |
| `{today -365d\|year=nearest_year}`                   | 2024-07-22 ||
| `{today -3y}`                   | 2022-07-22                              |            |
| `{today \| year_start}`                          | 2025-01-01 ||
| `{today \| year_end}`                            | 2025-12-31 ||
| `{today -1y \| year_start}`                          | 2024-01-01 ||
| `{today -1y \| year_end}`                            | 2024-12-31 ||
| `{today \| year=nearest_year, month=06, day=10}` | 2025-06-10 ||
| `{today -1y \| year=nearest_year, month=03, day=10}` | 2024-03-10 ||
| `{today \| year=2024, month=06, day=10}`          | 2024-06-10 ||
| `{year=2022, month=05, day=15}` | 2022-05-15                              |            |
| `2025-01-01`                    | 2025-01-01                              |            |
| `20250101`                      | 2025-01-01                              |            |
| `{1000-01-01 +30y\| year_end}`                            | 1030-12-31 ||
| `{today -36m}`                  | 2022-07-22                              |            |

---

필요에 따라 양식 더 조정하거나, example 더 추가 가능합니다!

## ⚙ Usage

```python
from dateling import DatelingResolver

resolver = DatelingResolver()
date = resolver.resolve("{today -1y | year_start}")
print(date)
```

You may also set a fixed reference date:

```python
resolver = DatelingResolver(reference_date="2025-06-11")
date = resolver.resolve("{today -3y | year_end}")
print(date)
```

---

## 📦 Installation

```bash
pip install dateling
```

(Once released to PyPI)

---

## 🔧 Design Philosophy

* 🧮 Formal expression language for time calculation
* 🔎 Fully deterministic, reproducible, and testable
* 🏷 No AI or natural language guessing
* 📈 Applicable across scheduling, reporting, ETL, search systems, financial applications, etc.

---

## 📄 License

MIT License

---

## 🔗 Related Alternatives

| Package         | Approach                           | Difference from dateling                       |
| --------------- | ---------------------------------- | ---------------------------------------------- |
| `dateparser`    | Natural language parsing           | No DSL, free-text interpretation               |
| `parsedatetime` | Human language parsing             | No formal syntax, heuristic parsing            |
| `textX`         | Generic DSL builder                | Requires custom DSL grammar creation           |
| `dateling`      | DSL-based date expression language | Strict syntax for controlled date calculations |

---

🧭 **dateling**:
When you want to write date calculations, not guess them.

import pandas as pd
from datetime import datetime, timedelta, date
import re
from dateutil.relativedelta import relativedelta

class DatelingResolver:
    """
    날짜 표현식을 파싱하고 변환하는 유틸리티 클래스

    지원하는 형식:
    - ${today}, {today}: 오늘 날짜
    - ${today -1w}, {today -1w}: 1주 전
    - ${today -1d}, {today -1d}: 1일 전
    - ${today -1m}, {today -1m}: 1개월 전
    - ${today -1y}, {today -1y}: 1년 전
    - {year=2024, month=12, day=31}: 절대 날짜

    요일 관련:
    - {monday}, {tuesday}, ... {sunday}: 이번주 해당 요일
    - {monday_of_this_week}, {tuesday_of_this_week}, ... {sunday_of_this_week}: 이번주 해당 요일
    - {last_monday}, {last_tuesday}, ... {last_sunday}: 지난주 해당 요일
    - {monday_of_last_week}, {tuesday_of_last_week}, ... {sunday_of_last_week}: 지난주 해당 요일
    """

    def __init__(self, reference_date=None):
        self.today = reference_date or datetime.today().date()

    def resolve(self, expr):
        """날짜 표현식을 파싱하여 date 객체로 변환"""
        expr = expr.strip()

        # New: support both {} and ${}
        if expr.startswith("${"):
            expr = "{" + expr[2:]

        # Full DSL expression pattern - 'w' (week) 단위 추가
        full_pattern = r"\{([a-zA-Z0-9\-_]+)(?:\s*([+-])\s*(\d+)\s*([dymw]))?(?:\s*\|\s*(.*))?\}"
        m = re.match(full_pattern, expr)
        if not m:
            # Absolute form: {year=YYYY, month=MM, day=DD}
            absolute_pattern = r"\{year=(\d+),\s*month=(\d+),\s*day=(\d+)\}"
            am = re.match(absolute_pattern, expr)
            if am:
                year = int(am.group(1))
                month = int(am.group(2))
                day = int(am.group(3))
                return datetime(year, month, day).date()
            else:
                try:
                    return pd.to_datetime(expr).date()
                except Exception:
                    return None

        # Extract parsed parts
        anchor_str = m.group(1)
        offset_sign = m.group(2)
        offset_num = m.group(3)
        offset_unit = m.group(4)
        modifiers_str = m.group(5)

        anchor = self._resolve_anchor(anchor_str)

        # Apply offset - week 단위 처리 추가
        if offset_num:
            offset_num = int(offset_num)
            if offset_sign == "-":
                offset_num = -offset_num

            if offset_unit == "d":
                anchor += timedelta(days=offset_num)
            elif offset_unit == "w":  # 주 단위 처리 추가
                anchor += timedelta(weeks=offset_num)
            elif offset_unit == "m":
                anchor += relativedelta(months=offset_num)
            elif offset_unit == "y":
                anchor += relativedelta(years=offset_num)

        # No modifiers → return directly
        if not modifiers_str:
            return anchor

        modifiers = self._parse_modifiers(modifiers_str)

        # Apply year_start / year_end
        if "year_start" in modifiers:
            anchor = datetime(anchor.year, 1, 1).date()
        if "year_end" in modifiers:
            anchor = datetime(anchor.year, 12, 31).date()

        # Apply year override
        if "year" in modifiers:
            if modifiers["year"] == "nearest_year":
                year = anchor.year
            else:
                year = int(modifiers["year"])
        else:
            year = anchor.year

        # Apply month override
        if "month" in modifiers:
            if modifiers["month"] == "nearest_month":
                month = anchor.month
            else:
                month = int(modifiers["month"])
        else:
            month = anchor.month

        # Apply day override
        day = int(modifiers.get("day", anchor.day))

        # Apply nearest_month fallback (after year applied)
        try_date = datetime(year, month, day).date()
        if modifiers.get("month") == "nearest_month" and try_date > self.today:
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            try_date = datetime(year, month, day).date()

        # Apply nearest_year fallback
        if modifiers.get("year") == "nearest_year" and try_date > self.today:
            year -= 1
            try_date = datetime(year, month, day).date()

        return try_date

    def _resolve_anchor(self, anchor_str):
        """앵커 문자열을 날짜로 변환"""
        if anchor_str == "today":
            return self.today
        elif anchor_str == "first_date_of_this_year":
            return datetime(self.today.year, 1, 1).date()
        elif anchor_str == "first_date_of_this_month":
            return datetime(self.today.year, self.today.month, 1).date()
        elif anchor_str == "monday_of_this_week":
            return self.today - timedelta(days=self.today.weekday())

        # 요일 이름과 인덱스 매핑 (0=월요일, 6=일요일)
        weekday_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        # 이번 주 요일 앵커들 (monday, tuesday, ..., sunday)
        for i, weekday in enumerate(weekday_names):
            if anchor_str == weekday:
                return self.today - timedelta(days=self.today.weekday() - i)

        # 이번 주 요일 앵커들 (monday_of_this_week, tuesday_of_this_week, ...)
        for i, weekday in enumerate(weekday_names):
            if anchor_str == f"{weekday}_of_this_week":
                return self.today - timedelta(days=self.today.weekday() - i)

        # 지난주 요일 앵커들 (last_monday, last_tuesday, ...)
        for i, weekday in enumerate(weekday_names):
            if anchor_str == f"last_{weekday}":
                return self.today - timedelta(days=self.today.weekday() + 7 - i)

        # 지난주 요일 앵커들 (monday_of_last_week, tuesday_of_last_week, ...)
        for i, weekday in enumerate(weekday_names):
            if anchor_str == f"{weekday}_of_last_week":
                return self.today - timedelta(days=self.today.weekday() + 7 - i)

        try:
            if "-" in anchor_str:
                return datetime.strptime(anchor_str, "%Y-%m-%d").date()
            else:
                return datetime.strptime(anchor_str, "%Y%m%d").date()
        except Exception:
            raise ValueError(f"Invalid anchor format: {anchor_str}")

    def _parse_modifiers(self, mod_str):
        """수정자 문자열을 파싱"""
        modifiers = {}
        for mod in mod_str.split(","):
            key_val = mod.strip().split("=")
            if len(key_val) == 1:
                modifiers[key_val[0].strip()] = True
            else:
                modifiers[key_val[0].strip()] = key_val[1].strip()
        return modifiers


    def _resolve_date_expression(self, expr: str, reference_date=None) -> date:
        """
        날짜 표현식을 변환하는 편의 함수
    
        Args:
            expr: 날짜 표현식 (예: "${today -1w}", "{today -1d}")
            reference_date: 기준 날짜 (기본값: 오늘)
    
        Returns:
            date: 변환된 날짜 객체
    
        Examples:
            >>> resolve_date_expression("${today -1w}")
            datetime.date(2025, 7, 14)  # 1주 전
    
            >>> resolve_date_expression("{today -3d}")
            datetime.date(2025, 7, 18)  # 3일 전
        """
        resolver = DatelingResolver(reference_date=reference_date)
        return resolver.resolve(expr)
    
    
    def _format_date_to_yyyymmdd(self, date_obj: date) -> str:
        """
        date 객체를 YYYYMMDD 형식 문자열로 변환
    
        Args:
            date_obj: date 객체
    
        Returns:
            str: YYYYMMDD 형식 문자열
        """
        return date_obj.strftime("%Y%m%d")


    def resolve_and_format_date(self, expr: str, reference_date=None) -> str:
        """
        날짜 표현식을 변환하고 YYYYMMDD 형식으로 포맷팅
    
        Args:
            expr: 날짜 표현식
            reference_date: 기준 날짜
    
        Returns:
            str: YYYYMMDD 형식 문자열 또는 빈 문자열 (변환 실패시)
        """
        try:
            resolved_date = self._resolve_date_expression(expr, reference_date)
            if resolved_date:
                return self._format_date_to_yyyymmdd(resolved_date)
            return ""
        except Exception:
            return ""


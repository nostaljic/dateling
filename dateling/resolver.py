import pandas as pd
from datetime import datetime, timedelta
import re
from dateutil.relativedelta import relativedelta

class DatelingResolver:
    def __init__(self, reference_date=None):
        self.today = reference_date or datetime.today().date()

    def resolve(self, expr):
        expr = expr.strip()

        full_pattern = r"\{([a-zA-Z0-9\-]+)(?:\s*([+-])(\d+)([dym]))?(?:\s*\|\s*(.*))?\}"
        m = re.match(full_pattern, expr)
        if not m:
            # absolute form: {year=YYYY, month=MM, day=DD}
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
                except:
                    return None

        anchor_str = m.group(1)
        offset_sign = m.group(2)
        offset_num = m.group(3)
        offset_unit = m.group(4)
        modifiers_str = m.group(5)

        anchor = self._resolve_anchor(anchor_str)

        if offset_num:
            offset_num = int(offset_num)
            if offset_sign == "-":
                offset_num = -offset_num

            if offset_unit == 'd':
                anchor += timedelta(days=offset_num)
            elif offset_unit == 'm':
                anchor += relativedelta(months=offset_num)
            elif offset_unit == 'y':
                anchor += relativedelta(years=offset_num)

        if not modifiers_str:
            return anchor

        modifiers = self._parse_modifiers(modifiers_str)

        if 'year_start' in modifiers:
            anchor = datetime(anchor.year, 1, 1).date()
        if 'year_end' in modifiers:
            anchor = datetime(anchor.year, 12, 31).date()

        if 'year' in modifiers:
            if modifiers['year'] == 'infer_year':
                year = anchor.year
            else:
                year = int(modifiers['year'])
        else:
            year = anchor.year

        month = int(modifiers.get('month', anchor.month))
        day = int(modifiers.get('day', anchor.day))
        candidate = datetime(year, month, day).date()

        if modifiers.get('year') == 'infer_year' and candidate > self.today:
            candidate = datetime(year - 1, month, day).date()

        return candidate

    def _resolve_anchor(self, anchor_str):
        if anchor_str == "today":
            return self.today
        try:
            if '-' in anchor_str:
                return datetime.strptime(anchor_str, "%Y-%m-%d").date()
            else:
                return datetime.strptime(anchor_str, "%Y%m%d").date()
        except:
            raise ValueError(f"Invalid anchor format: {anchor_str}")

    def _parse_modifiers(self, mod_str):
        modifiers = {}
        for mod in mod_str.split(","):
            key_val = mod.strip().split("=")
            if len(key_val) == 1:
                modifiers[key_val[0].strip()] = True
            else:
                modifiers[key_val[0].strip()] = key_val[1].strip()
        return modifiers

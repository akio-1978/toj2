import itertools
from datetime import datetime
import csv
import io

def stable_groupby(iterable, key):
    
    groups = []
    for group_key, group in itertools.groupby(iterable, lambda item: item.get(key, 'None')) :
        groups.append((group_key, list(group)))

    return groups

def datef(value, in_fmt="%Y/%m/%d", out_fmt="%Y/%m/%d"):
    """ 
        日付形式文字列の変換を行う。
        引数がin_fmtに合致しない場合、変換されない元の値を返します。
    """
    try:
        d = datetime.strptime(value, in_fmt)
        return d.strftime(out_fmt)
    except Exception:
        return value

def csvcell(value):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([value])
    return buf.getvalue().rstrip("\r\n")

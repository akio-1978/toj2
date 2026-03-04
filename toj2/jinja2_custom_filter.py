import itertools
from datetime import datetime

def stable_groupby(iterable, key):
    
    groups = []
    for group_key, group in itertools.groupby(iterable, lambda item: item.get(key, 'None')) :
        groups.append((group_key, list(group)))

    return groups

def zfilldate(value):
    """ 日付の月日のゼロ埋めを行う(ex 2025/1/9 -> 2025/01/09)
        ※日本のオープンデータでよく見られる形式だったので追加した
    """
    dt = datetime.strptime(value, "%Y/%m/%d")
    return dt.strftime("%Y/%m/%d")

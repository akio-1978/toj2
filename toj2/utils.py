import sys
import io
import contextlib

def get_stream(*, source:str | io.TextIOWrapper, encoding:str='utf8', mode:str='r'):
    """入出力ラッパー
        ファイル名が'-'ならstdin/outを使う
    """
    if source == '-':
        # stdio/outを割り当てる
        std =  sys.stdin if mode[1] == 'r' else sys.stdout
        return contextlib.nullcontext(io.TextIOWrapper(source.buffer, encoding=encoding))
    else:
        # 通常ファイル
        return contextlib.closing(open(source, encoding=encoding, mode=mode))
    

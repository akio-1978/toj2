import sys
import io
import contextlib

def get_stream(*, source:str | io.TextIOWrapper, encoding:str='utf8', mode:str='r'):
    """入出力ラッパー
        ファイル名が'-'ならstdin/outを使う
    """
    if source == '-':
        # stdio/outを割り当てる
        if mode[0] == 'w':
            
            sys.stdout.reconfigure(encoding=encoding)
            return contextlib.nullcontext(sys.stdout)
        else:
            return contextlib.nullcontext(sys.stdin)
    else:
        # 通常ファイル
        return contextlib.closing(open(source, encoding=encoding, mode=mode))
    

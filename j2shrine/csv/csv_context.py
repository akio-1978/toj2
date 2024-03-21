from ..context import RenderContext
from .csv_render import CsvRender
# CsvRender Context
class CsvRenderContext(RenderContext):
    def __init__(self, *, args):
        # default
        self.read_header = False
        self.delimiter = ','
        self.prefix = 'col_'
        self.skip_lines = 0
        self.names = []
        # assign args
        super().__init__(args=args)

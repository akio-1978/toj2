from toj2.processors import Processor

class CustomProcessor(Processor):
    
    def _execute(self, load_result, dest) -> None:
        dest.write('Hello Work!')

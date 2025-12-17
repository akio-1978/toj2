import unittest
from toj2.context import AppContext
from toj2.yaml.yaml_loader import YamlLoader
from toj2.processors import Jinja2Processor
from tests.testutils import J2SRenderingTest


class YamlTest(J2SRenderingTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'yaml'

    def test_simple_yaml(self):
        ctx = self.default_context()
        ctx.template='tests/yaml/templates/simple_yaml.tmpl'
        ctx.source = 'tests/yaml/src/simple_yaml.yaml'
        
        self.file_convert_test(context=ctx,
                               expect='tests/yaml/expect/simple_yaml.sql',
                               )

    def file_convert_test(self, *, context, expect):
        context.out = self.result_file()
        loader = YamlLoader(context=context, processor=Jinja2Processor(context))

        self.processor_test(loader=loader, expect_file=expect)

    def default_context(self):
        ctx = AppContext()
        ctx.parameters = {}
        ctx.template_encoding = 'utf8'
        ctx.input_encoding = 'utf8'
        ctx.output_encoding = 'utf8'
        
        return ctx


if __name__ == '__main__':
    unittest.main()

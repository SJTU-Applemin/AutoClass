from ult_generator.generator import Generator
from ult_generator.header_parser import HeaderParser


class MockGenerator(Generator):
    """

    """

    def __init__(self, info):
        """

        :param info:
        """
        Generator.__init__(self)
        if isinstance(info, HeaderParser):
            self.info = info
            self.mock_filename_h = 'mock_' + self.info.name
            self.mock_filename_cpp = 'mock_' + self.info.name[:-2] + '.cpp'
            self.mock_class_name = self.info.class_name + 'Mock'
            self.includes_h = []
            self.includes_cpp = []
            self.lines_h = []
            self.lines_cpp = []
        else:
            print('Use HeadParser Class to initialize!')

    def add_body_h(self, lines, info):
        """

        :param lines:
        :param info:
        :return:
        """
        lines.append('namespace ' + info.namespace + '\n')
        lines.append('{\n')
        lines.append('    class ' + self.mock_class_name + ' : public ' + info.class_name + '\n')
        lines.append('    {\n')
        lines.append('        public:\n\n')
        for var in info.vars:
            lines.append('            void set_' + var['name'] + '(' + var['type'] + ' ' + var['name'] + ');\n')
        lines.append('\n')
        lines.append('        protected:\n\n')
        for var in info.vars:
            lines.append('            ' + var['type'] + ' ' + var['name'] + ' = 0;\n')
        lines.append('    }\n')
        lines.append('}\n')

    def add_body_cpp(self, lines, info):
        """

        :param lines:
        :param info:
        :return:
        """
        lines.append('namespace ' + info.namespace + '\n')
        lines.append('{\n')
        for var in info.vars:
            lines.append('        void ' + self.mock_class_name + '::set_' + var['name'] + '(' + var['type'] + ' ' + var['name'] + '_mock)\n')
            lines.append('        {\n')
            lines.append('            ' + var['name'] + ' = ' + var['name'] + '_mock' + ';\n')
            lines.append('        }\n')
        lines.append('}\n')

    def generate_h(self):
        """

        :return:
        """
        self.add_file_header(self.lines_h)
        self.add_brief_intro_h(self.lines_h, self.mock_filename_h, self.mock_class_name)
        self.add_includes_h(self.lines_h, self.mock_filename_h[:-2], self.includes_h)
        self.add_body_h(self.lines_h, self.info)
        self.write_file(self.mock_filename_h, self.lines_h)

    def generate_cpp(self):
        """

        :return:
        """
        self.add_file_header(self.lines_cpp)
        self.add_brief_intro_cpp(self.lines_cpp, self.mock_filename_cpp, self.mock_class_name)
        self.add_includes_cpp(self.lines_cpp, self.includes_cpp)
        self.add_body_cpp(self.lines_cpp, self.info)
        self.write_file(self.mock_filename_cpp, self.lines_cpp)

import os
import copy
class ClassContent(object):

    def __init__(self):
        self.TestName = ''
        self.InputPara = []
        self.OutputPara = []
        self.filename = ''
        self.filepath = os.getcwd()
        self.includes = ['vp_reder_sfc_base.h', 'pipeline.h']
        self.lines = []
        self.level = 0

    def clear(self):
        self.TestName = ''
        self.InputPara = []
        self.OutputPara = []
        self.lines = []
        #self.filename = ''

    def generate(self):

        self.filename = self.TestName + '.h'
        self.addIncludeH(self.includes)
        self.addBody()
        self.addHeaders()
        self.writefile()

    def addIncludeH(self,includes = None):
        self.lines.append('\n')
        if includes:
            for h_file in includes:
                self.lines.append('#include \"' + h_file + '\"\n')
        self.lines.append('\n')

    def addBody(self):
        


        self.lines.append('\n')
        self.lines.append('class ' + self.TestName + '{\n')
        self.lines.extend(self.addClass(self.level+1))
        self.lines.append('};\n')

    def addClass(self,level):
        lines = []
        lines.append('\n')
        lines.append('    '*level + 'struct '+'Input{\n')
        lines.extend(self.addStruct(self.InputPara, level + 1 ))
        lines.append('    '*level + '};\n')
        lines.append('\n')
        lines.append('    '*level + 'struct ' + 'Output{\n')
        lines.extend(self.addStruct(self.OutputPara, level + 1 ))
        lines.append('    '*level + '};\n')
        lines.append('\n')
        return lines





    def addStruct(self, paras,level):
        lines = []
        for para in paras:
            lines.append('    '*level + para + ';\n')
        return lines

    def addHeaders(self):
        name_ifd = '__' + self.filename.split('.')[0].upper() + '_H__'
        lines = []
        lines.append('#ifndef ' + name_ifd + '\n')
        lines.append('#define ' + name_ifd + '\n')
        lines.append('\n')
        lines.extend(copy.deepcopy(self.lines))
        self.lines = lines
        self.lines.append('\n')
        self.lines.append('#endif\n')


    def writefile(self):
        file = self.filepath + '\\' + self.filename
        with open(self.filepath + '\\' + self.filename,'w') as fout:
            fout.writelines(self.lines)
                






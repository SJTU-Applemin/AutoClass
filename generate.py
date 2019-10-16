import os
import copy
class ClassContent(object):

    def __init__(self):
        self.TestName = ''
        self.inputPara = []
        self.outputPara = []
        self.inputName = []
        self.inputType = []
        self.inputValue = []
        self.outputType = []
        self.filename = ''
        self.file_header = os.getcwd() + '\\' + 'sample_header.txt'
        self.filepath = os.getcwd()
        self.includes = ['vp_reder_sfc_base.h', 'pipeline.h']
        self.lines = []
        self.level = 0
        self.className = ''
        self.functionName = ''

    def clear(self):
        self.TestName = ''
        self.inputPara = []
        self.inputName = []
        self.inputType = []
        self.inputValue = []
        self.outputPara = []
        self.lines = []
        #self.filename = ''

    def generate(self):

        self.filename = self.className + 'TestData.h'
        #self.add_file_header()
        #self.addHeaders()
        self.addIncludeH(self.includes)
        self.addParent()
        self.addBody()
        self.addHeaders()
        self.writefile()
        
    def generateInput(self):
        lines = []
        lines.append('<Header>\n')
        for index in range(len(self.inputName)):
            if self.inputValue[index]:
                lines.append(self.inputName[index] + ' = ' + self.inputValue[index] + '\n')
            else:
                lines.append(self.inputName[index] + ' = None\n')
        file = self.filepath + '\\' + self.className + self.functionName + self.TestName[:-8] + 'Input.dat'
        with open(file,'w') as fout:
            fout.writelines(lines)





    def addIncludeH(self,includes = None):
        self.lines.append('\n')
        if includes:
            for h_file in includes:
                self.lines.append('#include \"' + h_file + '\"\n')
        self.lines.append('\n')

    def addParent(self):
        self.lines.append('class TestData\n')
        self.lines.append('{\n')
        self.lines.append('public:\n')
        self.lines.append('    virtual void SetInput() =0;\n')
        self.lines.append('    //ReadTestData *m_readTestData;\n')
        self.lines.append('};\n')

    def addBody(self):
        self.lines.append('\n')
        self.lines.append('class ' + self.className + self.functionName + 'TestData: public TestData' + '\n{\n')
        self.lines.append('public:')
        self.lines.extend(self.addClass(self.level+1))
        self.lines.extend(self.addFunctions('input',self.level+1))
        self.lines.extend(self.addFunctions('output',self.level+1))
        self.lines.append('};\n')

    def addClass(self,level):
        lines = []
        lines.append('\n')
        lines.append('    '*level + 'struct '+'_inputParameters\n')
        lines.append('    '*level + '{\n')
        lines.extend(self.addStruct(self.inputPara, level + 1 ))
        lines.append('    '*level + '} inputParameters;\n')
        lines.append('\n')
        lines.append('    '*level + 'struct ' + '_outputParameters\n')
        lines.append('    '*level + '{\n')
        lines.extend(self.addStruct(self.outputPara, level + 1 ))
        lines.append('    '*level + '} outputParameters;\n')
        lines.append('\n')
        return lines


    def addStruct(self, paras,level):
        lines = []
        for para in paras:
            lines.append('    '*level + para + ';\n')
        return lines


    def addFunctions(self, fName,level):
        lines = []
        lines.append('\n')
        if fName == 'input':
            lines.append('    '*level + 'void SetInput()' + '\n')
        if fName == 'output':
            lines.append('    '*level + 'void SetOutputReference()' + '\n')
        #lines.append('    '*level + 'void' + fName + '\n')
        lines.append('    '*level + '{\n')
        lines.extend(self.addFunctionBody(fName, level+1 ))
        lines.append('    '*level + '}\n')
        lines.append('\n')
        return lines

    def addFunctionBody(self, fName, level):
        lines = []
        if fName == 'input':
            for i, input in enumerate(self.inputPara):
                if '*' in input:
                    value = 'nullptr'
                else:
                    value = self.getParaValue(self.inputType[i], input)
                para = input.split(' ')[-1].strip('*').strip('&')
                lines.append('    '*level + 'inputParameters.' + para + ' = '+ value)
                lines.append('\n')
        if fName == 'output':
            for i, output in enumerate(self.outputPara):
                if '*' in output:
                    value = 'nullptr'
                else:
                    value =  self.getParaValue(self.outputType[i], output)
                para = output.split(' ')[-1].strip('*').strip('&')
                lines.append('    '*level + 'outputParameters.' + para + ' = ' + value)
                lines.append('\n')
        return lines

    def generateReference(self):
        lines = []
        lines.append('<Header>\n')
        for i, output in enumerate(self.outputPara):
                if '*' in output:
                    value = 'nullptr'
                else:
                    value =  self.getParaValue(self.outputType[i], output)
                para = output.split(' ')[-1].strip('*').strip('&')
                lines.append(para + ' = ' + value + '\n')
        file = self.filepath + '\\' + self.className + self.functionName + self.TestName[:-8] + 'Reference.dat'
        with open(file,'w') as fout:
            fout.writelines(lines)

    def getParaValue(self, type, aa):
        if type == 'int':
            return '2';
        elif type == 'float':
            return '2.0'
        elif type == 'char':
            return '\'k\''
        elif type == 'bool':
            return 'true'
        elif type == 'selfDefined':
            return '0'
        elif type == 'container':
            pass

    def addHeaders(self):
        self.add_file_header()
        name_ifd = '__' + self.filename.split('.')[0].upper() + '_H__'
        lines = []
        lines.extend(copy.deepcopy(self.add_file_header()))
        lines.append('#ifndef ' + name_ifd + '\n')
        lines.append('#define ' + name_ifd + '\n')
        lines.append('\n')
        lines.extend(copy.deepcopy(self.lines))
        lines.append('\n')
        lines.append('#endif\n')
        self.lines = lines

    def add_file_header(self):
        lines = []
        with open(self.file_header, 'r') as fin:
            for line in fin:
                lines.append(line)
            lines.append('\n')
        return lines


    def writefile(self):
        file = self.filepath + '\\' + self.filename
        with open(self.filepath + '\\' + self.filename,'w') as fout:
            fout.writelines(self.lines)

    def generateClassNameFocusTestCpp(self):
        lines = []
        lines.append('#include ' + self.className + self.functionName + 'TestData.h\n')
        lines.append('#include ' + self.className + 'FocusTest.h\n')
        lines.append('TEST_F(' + self.className + 'FocusTest, ' + self.className + 'Test_' + self.functionName + '_' + self.TestName[:-8] + ')\n')
        lines.append('{\n')
        lines.append('   EXPECT_EQ(m_testMember->' + self.functionName + 'Test(inputRcId, referenceRcId, testname), 0);\n')
        lines.append('}\n')
        file = self.filepath + '\\' + self.className + 'FocusTest.cpp'
        with open(file,'w') as fout:
            fout.writelines(lines)

    def generateClassNameFocusTestH(self):
        lines = []
        lines.append('#ifndef __ENCODE_HEVC_VDENC_PIPELINE_G12_FT_H__\n')
        lines.append('#define __ENCODE_HEVC_VDENC_PIPELINE_G12_FT_H__\n')
        lines.append('#include "gtest/gtest.h"\n')
        lines.append('#include "gmock/gmock.h"\n')
        lines.append('#include ' + self.className + 'Test*.h\n')
        lines.append('using namespace testing;\n')
        lines.append('class ' + self.className + 'FT : public testing::Test\n')
        lines.append('{\n')
        lines.append('protected:\n')
        lines.append('   //!\n')
        lines.append('   //! \\brief   Initialization work before executing a unit test\n')
        lines.append('   //!\n')
        lines.append('   virtual void SetUp() \n')
        lines.append('   {\n')
        lines.append('      m_test = MOS_New(' + self.className + 'Test, nullptr, nullptr);\n')
        lines.append('   }\n')
        lines.append('\n')
        lines.append('   //!\n')
        lines.append('   //! \\brief   Uninitializaiton and exception handling after the unit test done\n')
        lines.append('   //!\n')
        lines.append('   virtual void TearDown()\n')
        lines.append('   {\n')
        lines.append('      MOS_Delete(m_test);\n')
        lines.append('   }\n')
        lines.append('   ' + self.className + 'Test* m_test = nullptr;\n')
        lines.append('}\n')
        file = self.filepath + '\\' + self.className + 'FocusTest.h'
        with open(file,'w') as fout:
            fout.writelines(lines)

    def generateClassNameTestH(self):
        lines = []
        lines.append('#include ' + self.className +'.h\n')
        lines.append('class ' + self.className +'Test : public ' + self.className +'\n')
        lines.append('{\n')
        lines.append('public:\n')
        lines.append('   ' + self.className +'Test(){};\n')
        lines.append('\n')
        lines.append('   virtual ~' + self.className +'Test() {};\n')
        lines.append('\n')
        lines.append('   MOS_STATUS ' + self.functionName +'Test();\n')
        lines.append('};\n')
        lines.append('\n')
        file = self.filepath + '\\' + self.className + 'Test.h'
        with open(file,'w') as fout:
            fout.writelines(lines)


    def generateClassNameTestCpp(self):
        lines = []
        lines.append('#include ' + self.className + self.functionName + 'TestData.h\n')
        lines.append('\n')
        lines.append('MOS_STATUS ' + self.className + 'Test::' + self.functionName + 'Test()\n')
        lines.append('{\n')
        lines.append('   ' + self.className + self.functionName + 'TestData testData;\n')
        lines.append('   testData.SetInput();\n')
        lines.append('   testData.SetOutputReference();\n')
        lines.append('\n')
        lines.append('   EXPECT_EQ(' + self.functionName + '(), testData.m_returnValue);\n')
        lines.append('\n')
        lines.append('   return MOS_STATUS_SUCCESS;\n')
        lines.append('}\n')
        file = self.filepath + '\\' + self.className + 'Test.cpp'
        with open(file,'w') as fout:
            fout.writelines(lines)






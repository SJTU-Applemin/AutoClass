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
        self.file_header = os.getcwd() + '\\' + 'sample_header.txt'
        self.workspace = ''
        self.includes = ['vp_reder_sfc_base.h', 'pipeline.h']
        #self.lines = []
        self.level = 0
        self.className = ''
        self.functionName = ''
        self.parser = None
        self.sourceFile = ''
        self.FTindex = ''
        self.returnValue = ''
        self.outputName = []


    def clear(self):
        self.TestName = ''
        self.inputPara = []
        self.inputName = []
        self.inputType = []
        self.inputValue = []
        self.outputPara = []
        self.outputName = []
        self.outputType = []

    # append if exists
    def generateTestDataH(self, update = False):
        path = self.workspace + '\\focus_test\\'
        if not os.path.exists(path):
            os.makedirs(path)
        file = path + self.sourceFile[:-2] + '_test_data.h'
        removeHead, removeTail = -1, -1
        if self.parser.namespace:
            indent = 3
        else:
            indent = 0
        if not update:
            lines = []
            lines.append('#ifndef __HEVCVDENCPIPELINETESTDATA_H__\n')
            lines.append('#define __HEVCVDENCPIPELINETESTDATA_H__\n')
            lines.append('#include "read_test_data.h"\n')
            if self.parser.namespace:
                lines.append('namespace ' + self.parser.namespace + '\n')
                lines.append('{\n')
            if self.parser.namespace:
                lines.append('}  // namespace encode\n')
            lines.append('#endif\n')
        else:
            with open(file,'r') as fout:
                lines = fout.readlines()
            for line_idx, line in enumerate(lines):
                if line.find('class ' + self.className + '_' + self.functionName) >= 0:
                    removeHead = line_idx - 1
                    break
            if removeHead >= 0:
                for line_idx in range(removeHead + 1, len(lines)):
                    if lines[line_idx].find('};') >= 0:
                        removeTail = line_idx
                        break

        insertLines = []
        insertLines.append('\n')
        insertLines.append(' ' * indent + 'class ' + self.className + '_' + self.functionName + '_TestData : public TestData\n')
        insertLines.append(' ' * indent + '{\n')
        insertLines.append(' ' * indent + 'public:\n')
        indent += 3
        insertLines.append(' ' * indent + self.className + '_' + self.functionName + '_TestData(uint32_t inputRcId, std::string &testName)\n')
        insertLines.append(' ' * indent + '{\n')
        indent += 3
        insertLines.append(' ' * indent + 'm_readTestData = MOS_New(ReadTestData, inputRcId, testName);\n')
        indent -= 3
        insertLines.append(' ' * indent + '}\n')
        insertLines.append('\n')
        insertLines.append(' ' * indent + 'int m_returnValue = 0;\n')  #m_readTestData->GetInputParams("returnValue", "returnValue", 0);\n')
        insertLines.append('\n')
        insertLines.append(' ' * indent + 'struct _inputParameters\n')
        insertLines.append(' ' * indent + '{\n')
        indent += 3
        for item in self.inputPara:
            insertLines.append(' ' * indent + item + ';\n')
        indent -= 3
        insertLines.append(' ' * indent + '} inputParameters;\n')
        insertLines.append('\n')
        insertLines.append(' ' * indent + 'struct _outputParameters\n')
        insertLines.append(' ' * indent + '{\n')
        indent += 3
        for item in self.outputPara:
            insertLines.append(' ' * indent + item + ';\n')
        indent -= 3
        insertLines.append(' ' * indent + '} outputParameters;\n')
        insertLines.append('\n')
        insertLines.append(' ' * indent + 'void SetInput()\n')
        insertLines.append(' ' * indent + '{\n')
        indent += 3
        for index, item in enumerate(self.inputName):
            insertLines.append(' ' * indent + 'inputParameters.' + item + ' = ' + self.getCastType(self.inputType[index]) + 'm_readTestData->GetInputParams("Input", "' + item + '", ' + self.getParaValue(self.inputType[index]) + ');\n')
        indent -= 3
        insertLines.append(' ' * indent + '}\n')
        insertLines.append('\n')
        insertLines.append(' ' * indent + 'void SetOutputReference()\n')
        insertLines.append(' ' * indent + '{\n')
        indent += 3
        insertLines.append(' ' * indent + 'm_returnValue = m_readTestData->GetInputParams("ReturnValue", "returnValue", 0);\n')
        for index, item in enumerate(self.outputName):
            insertLines.append(' ' * indent + 'outputParameters.' + item + ' = ' + self.getCastType(self.outputType[index]) + 'm_readTestData->GetInputParams("Output", "' + item + '", ' + self.getParaValue(self.outputType[index]) + ');\n')
        indent -= 3
        insertLines.append(' ' * indent + '}\n')
        indent -= 3
        insertLines.append(' ' * indent + '};\n')
        
        if removeHead >= 0:
            lines = lines[:removeHead] + lines[removeTail + 1:len(lines)-2] + insertLines + lines[len(lines)-2:]
        else:
            lines = lines[:len(lines)-2] + insertLines + lines[len(lines)-2:]

        with open(file,'w') as fout:
            fout.writelines(lines)
        print('generate ', file)

    def changeBool(self, s):
        if s.lower() == 'true':
            return '1'
        if s.lower() == 'false':
            return '0'
        return s

    def generateDat(self):
        lines = []
        lines.append('<Input>\n')
        for index in range(len(self.inputName)):
            if self.inputValue[index]:
                lines.append(self.inputName[index] + ' = ' + self.changeBool(self.inputValue[index]) + '\n')
            else:
                lines.append(self.inputName[index] + ' = None\n')
        lines.append('\n')
        lines.append('<ReturnValue>\n')
        lines.append('returnValue = ' + self.returnValue + '\n')
        lines.append('\n')
        lines.append('<Output>\n')
        for i, output in enumerate(self.outputPara):
                if '*' in output:
                    value = 'nullptr'
                else:
                    value =  self.getParaValue(self.outputType[i])
                para = output.split(' ')[-1].strip('*').strip('&')
                lines.append(para + ' = ' + self.changeBool(value) + '\n')
        path = self.workspace + '\\test_data\\focus_test\\' + self.className + '\\'
        if not os.path.exists(path):
            os.makedirs(path)
        file = path + self.className + self.functionName + self.TestName[:-8] + '.dat'
        with open(file,'w') as fout:
            fout.writelines(lines)
        print('generate ', file)

    def getCastType(self, type):
        if 'int' in type and type != 'int':
            return '(' + type + ')'
        return ''

    def getParaValue(self, type):
        if 'vector' in type:
            return 'null'
        if any([i in type for i in ['int', 'short', 'long', 'double', 'float', 'size']]):
            return '0'
        elif type == 'float':
            return '2.0'
        elif type == 'char':
            return "''"
        elif type == 'bool':
            return 'false'
        elif type == 'selfDefined':
            return '0'
        else:
            return 'null'


    def generateTestCaseCpp(self, update = False):
        file = self.workspace + '\\focus_test\\' + self.sourceFile[:-2] + '_test_case.cpp'
        if self.parser.namespace:
            indent = 3
        else:
            indent = 0
        if not update:
            lines = []
            lines.append('#include "' + self.sourceFile[:-2] + '_test_case.h"\n')
            lines.append('#include "test_data\\resource.h"\n')
            if self.parser.namespace:
                lines.append('namespace ' + self.parser.namespace +'\n')
                lines.append('{\n')
                lines.append('}  // namespace encode\n')
        else:
            with open(file) as fopen:
                lines = fopen.readlines()
        newLines = []
        newLines.append(' ' * indent + 'TEST_F(' + self.className + 'FT, ' + self.className + 'Test_' + self.functionName + '_' + self.TestName[:-8] + ')\n')
        newLines.append(' ' * indent + '{\n')
        indent += 3
        newLines.append(' ' * indent + 'std::string testName = ::testing::UnitTest::GetInstance()->current_test_info()->name();\n')
        newLines.append(' ' * indent + 'EXPECT_EQ(m_test->' + self.functionName + 'Test(' + self.className + self.functionName + self.TestName[:-8] + ', testName), 0);\n')
        indent -= 3
        newLines.append(' ' * indent + '}\n')
        
        lines = lines[:-1] + newLines + lines[-1:]
        with open(file,'w') as fout:
            fout.writelines(lines)
        print('generate ', file)

    def generateTestCaseH(self):
        if self.parser.namespace:
            indent = 3
        else:
            indent = 0
        lines = []
        lines.append('#ifndef __ENCODE_HEVC_VDENC_PIPELINE_G12_FT_H__\n')
        lines.append('#define __ENCODE_HEVC_VDENC_PIPELINE_G12_FT_H__\n')
        lines.append('#include "gtest/gtest.h"\n')
        lines.append('#include "gmock/gmock.h"\n')
        lines.append('#include "' + self.sourceFile[:-2] + '_test.h"\n')
        lines.append('using namespace testing;\n')
        if self.parser.namespace:
            lines.append('namespace ' + self.parser.namespace + '\n')
            lines.append('{\n')
        lines.append(' ' * indent + 'class ' + self.className + 'FT : public testing::Test\n')
        lines.append(' ' * indent + '{\n')
        lines.append(' ' * indent + 'protected:\n')
        indent += 3
        lines.append(' ' * indent + '//!\n')
        lines.append(' ' * indent + '//! \\brief   Initialization work before executing a unit test\n')
        lines.append(' ' * indent + '//!\n')
        lines.append(' ' * indent + 'virtual void SetUp()\n')
        lines.append(' ' * indent + '{\n')
        indent += 3
        lines.append(' ' * indent + 'm_test = MOS_New(' + self.className + 'Test, nullptr, nullptr);\n')
        indent -= 3
        lines.append(' ' * indent + '}\n')
        lines.append('\n')
        lines.append(' ' * indent + '//!\n')
        lines.append(' ' * indent + '//! \\brief   Uninitializaiton and exception handling after the unit test done\n')
        lines.append(' ' * indent + '//!\n')
        lines.append(' ' * indent + 'virtual void TearDown()\n')
        lines.append(' ' * indent + '{\n')
        indent += 3
        lines.append(' ' * indent + 'MOS_Delete(m_test);\n')
        indent -= 3
        lines.append(' ' * indent + '}\n')
        lines.append(' ' * indent + self.className + 'Test *m_test = nullptr;\n')
        indent -= 3
        lines.append(' ' * indent + '};\n')

        if self.parser.namespace:
            lines.append('}\n')
        lines.append('#endif\n')
        file = self.workspace + '\\focus_test\\' + self.sourceFile[:-2] + '_test_case.h'
        with open(file,'w') as fout:
            fout.writelines(lines)
        print('generate ', file)

    def getMethodIndex(self, name):
        for i, method in enumerate(self.parser.methods_info):
            if method['method_name'] == name:
                return i
        return -1

    def generateTestH(self):
        if self.parser.namespace:
            indent = 3
        else:
            indent = 0
        lines = []
        lines.append('#include "' + self.sourceFile[:-2] + '_test_data.h"\n')
        lines.append('#include "' + self.sourceFile + '"\n')
        lines.append('\n')
        if self.parser.namespace:
            lines.append('namespace ' + self.parser.namespace +'\n')
            lines.append('{\n')
        lines.append(' ' * indent + 'class ' + self.className + 'Test : public ' + self.className + '\n')
        lines.append(' ' * indent + '{\n')
        lines.append(' ' * indent + 'public:\n')
        indent += 3
        lines.append(' ' * indent + self.className + 'Test(')
        construct_id = self.getMethodIndex(self.className)
        if construct_id < 0:
            print('ERROR: no construct function')
        else:
            construct = self.parser.methods_info[construct_id]
            for i, para in enumerate(construct['parameters']):
                lines.append(para['type'] + ' ' + para['name'])
                if i != len(construct['parameters']) - 1:
                    lines.append(' ,')
            lines.append(') : ' + self.className + '(')
            for i, para in enumerate(construct['parameters']):
                lines.append(para['name'].lstrip('*').lstrip('&'))
                if i != len(construct['parameters']) - 1:
                    lines.append(' ,')
            lines.append('){};\n')
        #destruct_id = self.getMethodIndex('~' + self.className)
        #if destruct_id < 0:
        #    print('ERROR: no destruct function')
        #else:
        #    destruct = ''
        #    for line in self.parser.methods[destruct_id]:
        #        destruct = destruct + ' ' + line.strip()
        #    destruct = destruct.strip()
        #    if not destruct.endswith(';'):
        #        destruct += ';'
        #    lines.append(' ' * indent + destruct + '\n')
        lines.append(' ' * indent + 'virtual ~' + self.className + 'Test(){};\n')
        lines.append(' ' * indent + 'MOS_STATUS ' + self.functionName + 'Test(uint32_t inputRcId, std::string &testName);\n')
        indent -= 3
        lines.append(' ' * indent + '};\n')
        if self.parser.namespace:
            lines.append('}\n')
        file = self.workspace + '\\focus_test\\' + self.sourceFile[:-2] + '_test.h'
        with open(file,'w') as fout:
            fout.writelines(lines)
        print('generate ', file)

    def generateTestCpp(self):
        if self.parser.namespace:
            indent = 3
        else:
            indent = 0
        lines = []
        lines.append('#include "' + self.sourceFile[:-2] + '_test.h"\n')
        if self.parser.namespace:
            lines.append('namespace ' + self.parser.namespace + '\n')
            lines.append('{\n')
        lines.append(' ' * indent + 'MOS_STATUS ' + self.className + 'Test::' + self.functionName + 'Test(uint32_t inputRcId, std::string &testName)\n')
        lines.append(' ' * indent + '{\n')
        indent += 3
        lines.append(' ' * indent + self.className + '_' + self.functionName + '_TestData testData(inputRcId, testName);\n')
        lines.append(' ' * indent + 'testData.SetInput();\n')
        lines.append(' ' * indent + 'testData.SetOutputReference();\n')
        lines.append(' ' * indent + '//EXPECT_EQ(' + self.functionName + '(), testData.m_returnValue);\n')
        lines.append(' ' * indent + 'return MOS_STATUS_SUCCESS;\n')
        indent -= 3
        lines.append(' ' * indent + '}\n')
        if self.parser.namespace:
            lines.append('}  // namespace encode\n')
        file = self.workspace + '\\focus_test\\' + self.sourceFile[:-2] + '_test.cpp'
        with open(file,'w') as fout:
            fout.writelines(lines)
        print('generate ', file)

    def generateResourceH(self):
        file = self.workspace + '\\test_data\\resource.h'
        resource = self.className + self.functionName + self.TestName[:-8]
        focus_start_index = -1
        with open(file, 'r') as fopen:
            lines = fopen.readlines()
        for line_idx, line in enumerate(lines):
            if line.find('Focus Test') >= 0:
                focus_start_index = line_idx
                break
        if focus_start_index < 0:
            lines.append('\n')
            lines.append('// Focus Test\n')
            lines.append('#define ' + resource + ' ' * max(1, (47-len(resource))) + '300\n')
            self.FTindex = 1
        
        else:
            insert = False
            for i in range(focus_start_index+1, len(lines)):
                if not line.strip():
                    self.FTindex = str(i - focus_start_index)
                    lines.append('#define ' + resource + ' ' * max(1, (47-len(resource)))  + str(299 + i - focus_start_index) + '\n')
                    insert = True
                    return
            if not insert:
                self.FTindex = str(len(lines) - focus_start_index)
                lines.append('#define ' + resource + ' ' * max(1, (47-len(resource))) + str(299 + len(lines) - focus_start_index) + '\n')
        with open(file, 'w') as fopen:
            fopen.writelines(lines)
        print('generate ', file)

    def generateMediaDriverCodecUlt(self):
        file = self.workspace + '\\test_data\\media_driver_codec_ult.rc'
        with open(file, 'a') as fopen:
            resource = self.className + self.functionName + self.TestName[:-8]
            fopen.write(resource + ' ' * max(1, (45 - len(resource))) + 'TEST_DATA     "focus_test/' + self.TestName[:-8] + '/' + self.className + self.functionName + self.TestName[:-8] + '.dat"\n')
        print('generate ', file)

    def generateUltSrcsCmake(self):
        file = self.workspace + '\\ult_srcs.cmake'
        with open(file, 'r') as fopen:
            lines = fopen.readlines()
        for line_idx, line in enumerate(lines):
            if line.strip().startswith('set(TMP_SOURCES_'):
                for i in range(line_idx + 1, len(lines)):
                    if lines[i].strip().startswith(')'):
                        lines.insert(i, '    ${CMAKE_CURRENT_LIST_DIR}/focus_test/' + self.sourceFile[:-2] + '_test_case.cpp\n')
                        lines.insert(i + 1, '    ${CMAKE_CURRENT_LIST_DIR}/focus_test/' + self.sourceFile[:-2] + '_test.cpp\n')
                        break
                break
        for line_idx, line in enumerate(lines):
            if line.strip().startswith('set(TMP_HEADERS_'):
                for i in range(line_idx + 1, len(lines)):
                    if lines[i].strip().startswith(')'):
                        lines.insert(i, '    ${CMAKE_CURRENT_LIST_DIR}/focus_test/' + self.sourceFile[:-2] + '_test_case.h\n')
                        lines.insert(i + 1, '    ${CMAKE_CURRENT_LIST_DIR}/focus_test/' + self.sourceFile[:-2] + '_test.h\n')
                        lines.insert(i + 2, '    ${CMAKE_CURRENT_LIST_DIR}/focus_test/' + self.sourceFile[:-2] + '_test_data.h\n')
                        break
                break
        with open(file, 'w') as fopen:
            fopen.writelines(lines)
        print('generate ', file)








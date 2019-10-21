from ult_generator.generator import Generator
from ult_generator.header_parser import HeaderParser


class TestCaseGenerator(Generator):
    """

    """

    def __init__(self, head_parser):
        Generator.__init__(self)
        if isinstance(head_parser, HeaderParser):
            self.info = head_parser
            self.test_case_filename_h = self.info.name[:-2] + '_test_case.h'
            self.test_case_filename_cpp = self.info.name[:-2] + '_test_case.cpp'
            self.test_case_class_name = self.info.class_name + 'TestCase'
            self.test_class_name = 'Test' + self.info.class_name
            if self.info.namespace == 'vp':
                self.includes_h = ['TestFixture.h', 'test_' + self.info.name, 'media_interfaces_mhw.h', 'vp_mem_compression.h']
            else:
                self.includes_h = ['memory_leak_detector.h', 'mock_platform.h', 'encode_test_fixture.h',
                                'test_' + self.info.name]
            self.includes_cpp = [self.test_case_filename_h]
            self.lines_h = []
            self.lines_cpp = []
            self.test_case_variable = []
            self.class_member_variables = ['PMOS_INTERFACE']
            self.constructor_params = []
            #Do not change the sequence
            if self.info.namespace == 'vp':
                self.class_member_variables += ['VPMediaMemComp *', 'PVpAllocator', 'MhwInterfaces *']
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
        if info.namespace == 'vp':
            lines.append('    class ' + self.test_case_class_name + ' : public ' + 'DxvaTestFixture' + '\n')
        else:
            lines.append('    class ' + self.test_case_class_name + ' : public ' + 'EncodeTestFixture' + '\n')
        lines.append('    {\n\n')
        lines.append('    protected:\n\n')
        lines.append('\n')
        lines.append('        //!\n')
        lines.append('        //! \\brief   Initialization work before executing a unit test\n')
        lines.append('        //!\n')
        lines.append('        virtual void SetUp();\n')
        lines.append('\n')
        lines.append('        //!\n')
        lines.append('        //! \\brief   Uninitializaiton and exception handling after the unit test done\n')
        lines.append('        //!\n')
        lines.append('        virtual void TearDown();\n')
        lines.append('\n')
        if info.namespace != 'vp':
            lines.append('        //!\n')
            lines.append('        //! \\brief   Get Platform\n')
            lines.append('        //! \\param   [in] platform\n')
            lines.append('        //! \\        Reference to PLATFORM\n')
            lines.append('        //!\n')
            lines.append('        void GetPlatformByName(PLATFORM &platform);\n')
            lines.append('\n')
            lines.append('        //!\n')
            lines.append('        //! \\brief   Prepare Encode Params\n')
            lines.append('        //! \\param   [in] encodeParams\n')
            lines.append('        //! \\        Reference to EncodeParams\n')
            lines.append('        //!\n')
            lines.append('        void PrepareEncodeParams(EncoderParams &encodeParams);\n')
            lines.append('\n')
        linestr = self.str_radjust('        ' + self.test_class_name, 52)
        lines.append(linestr + '*m_test = nullptr;\n')
        for param in self.get_consturctor_method_parameters(info):
            iname = param['name']
            itype = param['type']
            bpointer = False
            #Todo, search the include file to find the Pxxx
            if((itype in self.media_ext_type) and iname.startswith('*')):
                itype = 'P'+ itype
                iname = 'm_' + iname[1:]
                bpointer = True;
            elif iname.startswith('*'):
                iname = iname[0] + 'm_' + iname[1:]
                bpointer = False
            elif iname.startswith('&'):
                iname = 'm_' + iname[1:]
            else:
                iname = 'm_'+ iname

            #vp FG-ULT, the mos interface and gpu context is created in the DxvaTestFixture::SetUp() already
            if(itype == 'PMOS_INTERFACE' and info.namespace == 'vp'):
                self.class_member_variables.remove(itype)
                self.constructor_params.append('m_pMosInterface')
                continue

            if iname.startswith('*'):
                self.constructor_params.append(iname[1:])
            else:
                self.constructor_params.append(iname)

            linestr = self.str_radjust('        ' + param['type'], 52)
            linestr += iname
            if bpointer or iname[0] == '*':
                linestr += ' = nullptr'
            lines.append(linestr + ' = nullptr;\n')

            self.test_case_variable.append({'type': itype, 'name': iname})

            if iname.startswith('*'):
                itype += ' *'
            if itype in self.class_member_variables:
                self.class_member_variables.remove(itype)

        for itype in self.class_member_variables:
            bpointer = False
            if itype[-1] == '*':
                iname = itype[0].lower() + itype[1:-2]
                bpointer = True
            else:
                iname = itype[0].lower() + itype[1:]
                if itype[0] == 'P' and (itype[1:] in self.media_ext_type):
                    bpointer = True

            idx = iname.find('_')
            preIdx = -1
            while idx != -1:
                if preIdx != -1:
                    iname = iname[:preIdx + 2]+iname[preIdx + 2:idx].lower()+iname[idx:]
                iname = iname[:idx - 1] + iname[idx - 1].lower() + iname[idx + 1].upper()+iname[idx + 2:]
                preIdx = idx
                idx = iname.find('_')

            if preIdx != -1:
                iname = iname[:preIdx]+ iname[preIdx] + iname[preIdx + 1:].lower()
            iname = 'm_'+ iname
            if itype[-1] == '*':
                iname = '*'+ iname
                itype = itype[:-2]
            self.test_case_variable.append({'type': itype, 'name': iname})
            if bpointer:
                lines.append(self.str_radjust('        ' + itype, 52) + iname + ' = nullptr;\n')
            else:
                lines.append(self.str_radjust('        ' + itype, 52) + iname + ';\n')


        lines.append('\n')
        lines.append('    };\n')
        lines.append('}\n')
        lines.append('\n')
        lines.append('#endif\n')

    def generate_h(self):
        """

        :return:
        """
        self.add_file_header(self.lines_h)
        self.add_brief_intro_h(self.lines_h, self.test_case_filename_h,self.test_case_class_name)
        self.add_includes_h(self.lines_h, self.test_case_filename_h[:-2], self.includes_h)
        self.add_body_h(self.lines_h, self.info)
        self.write_file(self.test_case_filename_h, self.lines_h)

    def get_consturctor_method_parameters(self, info):
        method = self.get_consturctor_method(info)
        return method['parameters']

    def get_consturctor_method(self, info):
        for method in info.methods_info:
            if method['return_type'] == 'Constructor':
                return method

    def mosinterface_generate(self, lines):
        space8Str = ' '*8
        space4Str = ' '*4
        lines.append('\n')
        lines.append(space8Str + 'if (m_osInterface == nullptr) \n')
        lines.append(space8Str + '{\n')
        lines.append(space8Str + space4Str + 'm_osInterface = (PMOS_INTERFACE)MOS_AllocAndZeroMemory(sizeof(MOS_INTERFACE));\n')
        lines.append(space8Str + '}\n')

    #TODO, add ui to set the MhwInterfaces::CreateParams
    def mhwinterface_setup(self, lines, mosinterfaceName):
        space8Str = ' '*8
        space4Str = ' '*4
        mmcName = ''
        lines.append('\n')
        lines.append(space8Str + 'MhwInterfaces::CreateParams params;\n')
        lines.append(space8Str + 'MOS_ZeroMemory(&params, sizeof(params));\n')
        lines.append(space8Str + 'params.Flags.m_render = true;\n')
        lines.append(space8Str + 'params.Flags.m_sfc = true;\n')
        lines.append(space8Str + 'params.Flags.m_vdboxAll = true;\n')
        lines.append(space8Str + 'params.Flags.m_vebox = true;\n')
        lines.append(space8Str + 'params.m_heapMode = (uint8_t)2;\n')
        lines.append('\n')
        lines.append(space8Str + 'MhwInterfaces *mhw = MhwInterfaces::CreateFactory(params, ' + mosinterfaceName +');\n')
        lines.append(space8Str + 'EXPECT_NE(nullptr, mhw);\n')
        lines.append('\n')

        if self.info.namespace == 'vp':
            lines.append(space8Str + 'EXPECT_NE(nullptr, mhw->m_sfcInterface);\n')
            lines.append(space8Str + 'EXPECT_NE(nullptr, mhw->m_veboxInterface);\n')

        else:
            lines.append(space8Str + 'CodechalHwInterface *hwInterface = nullptr;\n')
            lines.append(space8Str + 'if (platform.eProductFamily == IGFX_TIGERLAKE_LP)\n')
            lines.append(space8Str + '{\n')
            lines.append(space8Str + space4Str + 'hwInterface = MOS_New(CodechalHwInterfaceG12, m_osInterface, CODECHAL_FUNCTION_ENC_VDENC_PAK, mhw);\n')
            lines.append(space8Str + '}\n')
            lines.append(space8Str + 'if (platform.eProductFamily == IGFX_TIGERLAKE_HP)\n')
            lines.append(space8Str + '{\n')
            lines.append(space8Str + space4Str + 'hwInterface = MOS_New(CodechalHwInterfaceG12Tglhp, m_osInterface, CODECHAL_FUNCTION_ENC_VDENC_PAK, mhw);\n')
            lines.append(space8Str + '}\n')
            lines.append(space8Str + 'EXPECT_NE(nullptr, hwInterface);\n')
            lines.append(space8Str + 'MOS_Delete(mhw);\n')

        for param in self.test_case_variable:
            iname = param['name']
            itype = param['type']
            if itype == 'MhwInterfaces' and iname[0] == '*':
                lines.append(space8Str + iname[1:] + ' = mhw;\n')

            if itype == 'PVP_MHWINTERFACE':
                lines.append(space8Str + iname + ' = MOS_New(VP_MHWINTERFACE);\n')
                lines.append(space8Str + 'MOS_ZeroMemory(' + iname + ', sizeof(VP_MHWINTERFACE)); \n')
                lines.append(space8Str + iname + '->m_sfcInterface' + ' = mhw->m_sfcInterface;\n')
                lines.append(space8Str + iname + '->m_veboxInterface' + ' = mhw->m_sfcInterface;\n')
                lines.append(space8Str + iname + '->m_skuTable' + mosinterfaceName + '->pfnGetSkuTable( ' + mosinterfaceName + ' );\n')
            if itype == 'PMHW_VEBOX_INTERFACE':
                lines.append(space8Str + iname + ' = mhw->m_veboxInterface;\n')
            if itype == 'PMHW_SFC_INTERFACE':
                lines.append(space8Str + iname + ' = mhw->m_sfcInterface;\n')

            if itype == 'VPMediaMemComp' and iname[0] == '*':
                lines.append(space8Str + iname[1:] + ' = MOS_New(VPMediaMemComp, ' + mosinterfaceName + ', mhw->m_miInterface);\n')
                lines.append(space8Str + 'EXPECT_NE(nullptr, '+ iname[1:] + ');\n')
                mmcName = iname[1:]

        lines.append('\n')
        return mmcName


    def mosinterface_setup(self, lines, mosinterfaceName):
        for param in self.test_case_variable:
            iname = param['name']
            itype = param['type']
            # PMOS_INTERFACE init, in add_body_h, force to use PMOS_INTERFACE to define a member variable
            if itype == 'PMOS_INTERFACE':
                self.mosinterface_generate(lines)
                mosinterfaceName = iname


    def add_setup_method_body(self, lines, info):
        space8Str = " "*8
        mosinterfaceName = ''
        if self.info.namespace == 'vp':
            lines.append(space8Str + 'DxvaTestFixture::SetUp();\n')
            mosinterfaceName = 'm_pMosInterface'

        #vp create mos interface in dxvatest setup
        if self.info.namespace != 'vp':
            self.mosinterface_setup(lines, mosinterfaceName)

        mmcName = self.mhwinterface_setup(lines, mosinterfaceName)
        for param in self.test_case_variable:
            if param['type'] == 'PVpAllocator':
                lines.append(space8Str + param['name'] + ' = MOS_New(VpAllocator, ' + mosinterfaceName + ', ' + mmcName + ');\n')
                lines.append(space8Str + 'EXPECT_NE(nullptr, m_allocator);\n')

        lines.append('\n')
        lines.append(space8Str + 'm_test = MOS_New(Test' + self.info.class_name)
        for iparam in self.constructor_params:
            lines.append(', ' + iparam)
        lines.append('); \n\n')

        lines.append(space8Str + 'EXPECT_NE(nullptr, m_test);\n')

    def mhwinterface_teardown(self, lines):
        space8Str = " "*8
        for param in self.test_case_variable:
            iname = param['name']
            itype = param['type']
            if itype == 'PVP_MHWINTERFACE':
                lines.append(space8Str + 'MOS_Delete(' + iname + ');\n')
            elif iname[0] == '*' and (itype == 'MhwInterfaces' or itype == 'VPMediaMemComp') :
                iname = iname[1:]
                if(itype == 'MhwInterfaces'):
                    lines.append(space8Str + iname + '->Destroy();\n')
                lines.append(space8Str + 'MOS_Delete(' + iname + ');\n')

    def add_teardown_method_body(self, lines, info):
        space8Str = " "*8
        lines.append(space8Str + 'MOS_Delete(m_test); \n')
        self.mhwinterface_teardown(lines)
        if self.info.namespace == 'vp':
            lines.append(space8Str + 'DxvaTestFixture::TearDown();\n')

    def add_body_cpp(self, lines, info):
        """

        :return:
        """
        lines.append('namespace ' + info.namespace + '\n')
        lines.append('{\n')
        lines.append('\n')
        lines.append('    void ' + self.test_case_class_name + '::SetUp()\n')
        lines.append('    {\n')
        self.add_setup_method_body(lines, info)
        lines.append('    }\n')
        lines.append('\n')
        lines.append('    void ' + self.test_case_class_name + '::TearDown()\n')
        lines.append('    {\n')
        self.add_teardown_method_body(lines, info)
        lines.append('    }\n')
        if info.namespace != 'vp':
            lines.append('    void ' + self.test_case_class_name + '::GetPlatformByName(PLATFORM &platform)\n')
            lines.append('    {\n')
            lines.append('\n\n')
            lines.append('    }\n')
            lines.append('    void ' + self.test_case_class_name + '::PrepareEncodeParams(EncoderParams &encodeParams)\n')
            lines.append('    {\n')
            lines.append('\n\n')
            lines.append('    }\n')
        lines.append('\n\n')
        for method in info.methods_info:
            if method['method_name'] == '' or method['virtual']:
                continue
            lines.append('    TEST_F(' + self.test_case_class_name + ', ' + method['method_name'] + ')\n')
            lines.append('    {\n')
            lines.append('        EXPECT_EQ(m_test->' + method['method_name'] + 'Test(), MOS_STATUS_SUCCESS);\n')
            lines.append('    }\n')
        lines.append('}\n')

    def generate_cpp(self):
        """

        :return:
        """
        self.add_file_header(self.lines_cpp)
        self.add_brief_intro_cpp(self.lines_cpp, self.test_case_filename_cpp, self.test_case_class_name)
        self.add_precompiled_header(self.lines_cpp)
        self.add_includes_cpp(self.lines_cpp, self.includes_cpp)
        self.add_body_cpp(self.lines_cpp, self.info)
        self.write_file(self.test_case_filename_cpp, self.lines_cpp)

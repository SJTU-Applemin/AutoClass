from xml.dom.minidom import parse
import xml.dom.minidom
from ult_generator.header_parser import HeaderParser


def generate_header_xml(info, includes):
    """

    :return:
    """
    if isinstance(info, HeaderParser):
        lines = []
        lines.append('<?xml version="1.0" encoding="utf8"?>\n')
        lines.append('<' + info.name + '>\n')
        lines.append('  <test_' + info.name + '>\n')
        for i in includes['test_h']:
            lines.append('    <Header file="' + i + '"/>\n')
        #lines.append('    <Header file=""/>\n')
        for i in includes['test_cpp']:
            lines.append('    <Source file="' + i + '"/>\n')
        #lines.append('    <Source file=""/>\n')
        lines.append('  </test_' + info.name + '>\n')

        lines.append('  <' + info.name[:-2] + '_test_case.h>\n')
        for i in includes['test_case_h']:
            lines.append('    <Header file="' + i + '"/>\n')
        #lines.append('    <Header file=""/>\n')
        for i in includes['test_case_cpp']:
            lines.append('    <Source file="' + i + '"/>\n')
        lines.append('  </' + info.name[:-2] + '_test_case.h>\n')

        lines.append('  <mock_' + info.name + '>\n')
        lines.append('    <Header file=""/>\n')
        lines.append('    <Source file=""/>\n')
        lines.append('  </mock_' + info.name + '>\n')
        lines.append('</' + info.name + '>\n')
        with open(info.name[:-2] + '_header.xml', 'w') as fout:
            fout.writelines(lines)
    else:
        print('Use HeadParser Class to initialize!')


def read_header_xml(info):
    """

    :param info:
    :return:
    """
    includes = {'test_h': [], 'test_cpp': [], 'test_case_h': [], 'test_case_cpp': [], 'mock_h': [], 'mock_cpp': []}
    DOMTree = xml.dom.minidom.parse(info.name[:-2] + '_header.xml')
    collection = DOMTree.documentElement

    tmp = collection.getElementsByTagName('test_' + info.name)[0]
    headers = tmp.getElementsByTagName('Header')
    for tag in headers:
        if tag.getAttribute('file').endswith('.h'):
            includes['test_h'].append(tag.getAttribute('file'))
    headers = tmp.getElementsByTagName('Source')
    for tag in headers:
        if tag.getAttribute('file').endswith('.h'):
            includes['test_cpp'].append(tag.getAttribute('file'))

    tmp = collection.getElementsByTagName(info.name[:-2] + '_test_case.h')[0]
    headers = tmp.getElementsByTagName('Header')
    for tag in headers:
        if tag.getAttribute('file').endswith('.h'):
            includes['test_case_h'].append(tag.getAttribute('file'))
    headers = tmp.getElementsByTagName('Source')
    for tag in headers:
        if tag.getAttribute('file').endswith('.h'):
            includes['test_case_cpp'].append(tag.getAttribute('file'))

    tmp = collection.getElementsByTagName('mock_' + info.name)[0]
    headers = tmp.getElementsByTagName('Header')
    for tag in headers:
        if tag.getAttribute('file').endswith('.h'):
            includes['mock_h'].append(tag.getAttribute('file'))
    headers = tmp.getElementsByTagName('Source')
    for tag in headers:
        if tag.getAttribute('file').endswith('.h'):
            includes['mock_cpp'].append(tag.getAttribute('file'))

    return includes


def read_mock_xml(file_name):
    """

    """
    vars = []
    dependency_class = []
    DOMTree = xml.dom.minidom.parse(file_name)
    data = DOMTree.getElementsByTagName('variable')
    for var in data:
        tmp = {'type': '', 'name': '', 'min': '', 'max:' :''}
        for key in tmp:
            tmp[key] = var.getAttribute(key)
        vars.append(tmp)

    data2 = DOMTree.getElementsByTagName('class')
    for cls in data2:
        data = cls.getElementsByTagName('variable')
        tmp2 = []
        for var in data:
            tmp = {'type': '', 'name': '', 'min': '', 'max:': ''}
            for key in tmp:
                tmp[key] = var.getAttribute(key)
            tmp2.append(tmp)
        dependency_class.append(tmp2)

    return vars, dependency_class


def generate_mock_xml(info):
    """


    """
    class_dir = {}
    with open('class_file.txt', 'r') as fin:
        for line in fin:
            tmp = line.strip().split(line, ' ')
            class_dir[tmp[0]] = tmp[1]

    lines = []
    lines.append('<?xml version="1.0" encoding="utf8"?>\n')
    lines.append('<' + info['file_name'] + '>\n')
    for var in info['var']:
        lines.append('  <variable name="' + var['name'] + '" type="' + var['type'] + '" min="" max="" />\n')
    for var in info['class_var']:
        lines.append('  <class name="' + var['name'] + '" type="' + var['type'] + '">\n')
        if var['type'] in class_dir:
            dependency_xml = class_dir[var['type']][:-2] + '_mock.xml'
            dep_vars, dep_cls = read_mock_xml(dependency_xml)
            for class_var in info['dep_vars']:
                lines.append('  <variable name="' + class_var['name'] + '" type="' + class_var['type'] + '" min="" max="" />\n')
        lines.append('  </class>\n')
    lines.append('</' + info['file_name'] + '>\n')
    with open(info['file_name'] + '_mock.xml', 'w') as fout:
        fout.writelines(lines)


# def read_header_xml(info):
#     """
#
#     :param info:
#     :return:
#     """
#     includes = {'test': {'cpp': set(), 'h': set()},
#                 'test_case': {'cpp': set(), 'h': set()},
#                 'mock': {'cpp': set(), 'h': set()}}
#     DOMTree = xml.dom.minidom.parse(info['file_name'] + '_header.xml')
#     collection = DOMTree.documentElement
#
#     tmp = collection.getElementsByTagName(info['mock_name'])[0]
#     headers = tmp.getElementsByTagName('Header')
#     for tag in headers:
#         if tag.getAttribute('file').endswith('.h'):
#             includes['test']['h'].add(tag.getAttribute('file'))
#     headers = tmp.getElementsByTagName('Source')
#     for tag in headers:
#         if tag.getAttribute('file').endswith('.h'):
#             includes['test']['cpp'].add(tag.getAttribute('file'))
#
#     tmp = collection.getElementsByTagName(info['test_name'])[0]
#     headers = tmp.getElementsByTagName('Header')
#     for tag in headers:
#         if tag.getAttribute('file').endswith('.h'):
#             includes['test_case']['h'].add(tag.getAttribute('file'))
#     headers = tmp.getElementsByTagName('Source')
#     for tag in headers:
#         if tag.getAttribute('file').endswith('.h'):
#             includes['test_case']['cpp'].add(tag.getAttribute('file'))
#
#     tmp = collection.getElementsByTagName(info['mock_name2'])[0]
#     headers = tmp.getElementsByTagName('Header')
#     for tag in headers:
#         if tag.getAttribute('file').endswith('.h'):
#             includes['mock']['h'].add(tag.getAttribute('file'))
#     headers = tmp.getElementsByTagName('Source')
#     for tag in headers:
#         if tag.getAttribute('file').endswith('.h'):
#             includes['mock']['cpp'].add(tag.getAttribute('file'))
#
#     return includes

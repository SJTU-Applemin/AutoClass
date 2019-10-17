import re
import os
import ult_generator.tree as tree

class CppParser(object):
    """

    """

    def __init__(self, name, path, info=None):
        """

        :param name:
        :param path:
        """
        self.name = name
        self.path = path
        self.lines = []
        self.header_info = info
        self.conditions = {}
        self.includes = set()

    def read_file(self, name=None, path=None):
        if name:
            self.name = name
        if path:
            self.path = path
        with open(self.path + self.name, 'r') as fin:
            self.lines = fin.readlines()

        for line in self.lines:
            line_clr = line.strip()
            idx = line_clr.find('#include')
            if idx != -1:
                line_clr = line_clr[len('#include '):]
                line_clr = line_clr[line_clr.find('"') + 1 : line_clr.rfind('"')]
                self.includes.add(line_clr)


    @staticmethod
    def find_function(lines, function_info, class_name):
        #print(function_info['method_name'])
        function_head = function_info['return_type'] + ' ' + class_name + '::' + function_info['method_name'] + '('
        idx = -1
        for i in range(len(lines)):
            line_clr = lines[i].strip()
            if line_clr.startswith(function_head):
                idx = i
                break
        #print(idx)
        lines_func = []
        if idx != -1:
            c1 = 0
            c2 = 0
            while c1 > c2 or c1 == 0:
                lines_func.append(lines[idx])
                if lines[idx].find('{') != -1:
                    c1 += 1
                if lines[idx].find('}') != -1:
                    c2 += 1
                idx += 1

        return lines_func

    @staticmethod
    def tokenize(line):
        # print(line)
        line = line.strip().replace('->', '#')
        tokens = []
        t = ''
        operators = ('!', '|', '&', '=', '>', '<', '+', '\-', '*', '/')
        symbols = ''
        for i in operators:
            symbols = symbols + i
        symbols = '[' + symbols + ']'
        tokens = re.split(symbols, line)
        # print(tokens)
        tokens = [t.replace('#', '->') for t in tokens]
        tokens_filter = []
        filters = ['MOS_STATUS_SUCCESS', 'true', 'false', 'nullptr']
        for t in tokens:
            t = t.strip()
            t = t.replace('()', 'shit')
            t = t.replace('(', '')
            t = t.replace(')', '')
            t = t.replace('shit', '()')
            if t and not t.isdigit() and t not in filters:
                #print(t)
                #if t.replace('_', '').isalpha():
                tokens_filter.append(t)
        # print(tokens_filter)
        return tokens_filter

    @staticmethod
    def parse_expression(s):
        """

        :param s:
        :return:
        """
        condition = {'true':[], 'false':[]}
        operators = {'!': 2, '||': 12, '&&': 11, '=': 14, '==': 7, '!=': 7, '>': 6, '<': 6, '>=': 6, '<=': 6, '+': 4,
                     '-': 4, '*': 3, '/': 3, '(': 1, ')': 1}

        t = ''
        tokens = []
        stack_tokens = []
        stack_opt = []
        s  = s.replace(' ', '')
        f_continue = False
        for idx in range(len(s)):
            c = s[idx]
            opt = ''
            if f_continue:
                f_continue = False
                continue
            if s[idx:idx+2] in operators:
                opt = s[idx:idx+2]
            elif s[idx] in operators:
                if s[idx:idx + 2] == '->' or s[idx:idx + 2] == '()':
                    t += s[idx:idx + 2]
                    f_continue = True
                    continue
                opt = s[idx]
            # if c not in operators and s[idx:idx+2] not in operators:
            #     t += c
            else:
                t += s[idx]
            if opt:
                tokens.append({'name': t, 'type': ''})
                node_t = tree.Node(t)
                stack_opt.append(node_t)
                t = ''
                if len(opt) == 2:
                    f_continue = True
                if not stack_opt:
                    stack_opt.append(opt)
                    continue
                if operators[opt] < operators[stack_opt[-1]]:
                    stack_opt.append(opt)
                else:
                    while operators[opt] < operators[stack_opt[-1]]:
                        if opt == ')' and stack_opt[-1] == '(':
                            stack_opt.pop()
                            break
                        right = stack_tokens.pop()
                        left = stack_tokens.pop()
                        mid = stack_opt.pop()
                        new_node = tree.Node(mid, left, right)
                        stack_tokens.append(new_node)
                    if opt != ')':
                        stack_opt.append(opt)
        while stack_opt:
            right = stack_tokens.pop()
            left = stack_tokens.pop()
            mid = stack_opt.pop()
            new_node = tree.Node(mid, left, right)
            stack_tokens.append(new_node)

        return stack_tokens[0], tokens

    @staticmethod
    def calculate_expression(root, tokens, data_value):
        """

        :param root:
        :param tokens:
        :param data_value:
        :return:
        """
        pass



    @staticmethod
    def set_value_to_meet_condition(root, tokens):
        """

        :param root:
        :param tokens:
        :return:
        """
        f_True_condition = False
        f_False_condition = False
        conditions = []
        if root.value == '&&' or root.value == '||':
            left = CppParser.set_value_to_meet_condition(root.left, tokens)
            right = CppParser.set_value_to_meet_condition(root.right, tokens)
            if root.value == '&&':
                pass
            if root.value == '||':
                pass
        else:
            data_value = []
            all_possible_data_value = []
            for t in tokens:
                if t['type'] == 'bool':
                    new_value = []
                    for j in all_possible_data_value:
                        j[t['name']] = True
                        new_value.append(j)
                        j[t['name']] = False
                        new_value.append(j)
                    all_possible_data_value = new_value
                if t['type'] == 'int':
                    new_value = []
                    for j in all_possible_data_value:
                        j[t['name']] = 0
                        new_value.append(j)
                        j[t['name']] = 10
                        new_value.append(j)
                        j[t['name']] = 100
                        new_value.append(j)
                    all_possible_data_value = new_value
                if t['type'] == 'const':
                    data_value[t['name']] == int(t['name'])

            for data_value in all_possible_data_value:
                result = CppParser.calculate_expression(root, tokens, data_value)
                if result and f_True_condition:
                    f_True_condition = True
                    conditions.append((data_value, True))
                if not result and f_False_condition:
                    f_False_condition = True
                    conditions.append((data_value, False))
                if f_True_condition and f_False_condition:
                    break

        return conditions

    def parse_function(self, lines, function_info):
        # print(function_info['method_name'])
        # print(len(lines))
        conditions = []
        ifs = []
        tokens = []
        if_num = 0
        for i in range(len(lines)):
            line_clr = lines[i].strip()
            if line_clr.startswith('if'):
                #print(line_clr)
                ifs.append(i)
                idx = line_clr.find('if')
                idx_l = line_clr.find('(')
                idx_r = line_clr.rfind(')')
                if idx_r == -1:   # need work when if more than one line
                    continue
                condition = line_clr[idx_l+1:idx_r]
                tokens = self.tokenize(condition)
                #print(condition)
                #print(tokens)
                conditions.append({'condition': condition, 'vars': tokens})
       #     if line_clr.startswith('else'):

        return conditions

    def parse_conditions(self):
        for method in self.header_info.methods_info:
            function_lines = self.find_function(self.lines, method, self.header_info.class_name)
            self.conditions[method['method_name']] = self.parse_function(function_lines, method)

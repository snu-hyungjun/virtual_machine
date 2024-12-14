"""
VMO Lab.
Petite-Language Interpreter
"""
from .exceptions import *
from .ixx import *
from .utils import *
from .virtual_machine import VM

import operator


class PTVM(VM):
    """
    Petite Virtual Machine
    """
    INT_TYPE = int

    def __init__(self):
        """
            Operator precedence.
            0. '(', ')', '[', ']'
            1. '*', '/'
            2. '+', '-'
            3. '==', '!=', '<', '>', '<=', '>='
        """
        super().__init__()
        op0 = {'(': None, ')': None,
               '[': lambda x, n: operator.getitem(x, int(n)), ']': None}
        op1 = {'*': operator.mul, '/': operator.truediv}
        op2 = {'+': operator.add, '-': operator.sub}
        op3 = {'==': operator.eq, '!=': operator.ne,
               '<': operator.lt, '>': operator.gt,
               '<=': operator.le, '>=': operator.ge}
        self.operators = [op0, op1, op2, op3]  # Operator table.

    def scan_labels(self):
        self.labels = {}
        line_number = 0

        for line in self.code:
            if line != '':
                if line[-1] == ':':
                    line_name = line[:-1]
                    self.labels[line_name] = line_number
                line_number += 1
            else:
                line_number += 1


    def evaluate(self, expr):
        if expr.count(')') != expr.count('('):
            raise MismatchingParentheses()
        elif expr.count(']') != expr.count('['):
            raise MismatchingBrackets()
        
        if is_numeral(expr):
            return int(expr)
        
        elif is_varname(expr):
            if expr not in self.mem:
                raise UnknownVariable()
            else:
                return self.mem[expr]
            
        elif expr == 'input()':
            a = input()
            if not is_numeral(a):
                raise IllegalValue()
            else:
                return a
            
        for operator_dict in [self.operators[1], self.operators[2], self.operators[3]]:
            for operator in operator_dict:
                if operator in expr:
                    return self.compute(expr)
            
        if expr and expr[0] == '(' and expr[-1] == ')':
            return self.evaluate(expr[1:-1])    
        
        elif expr and expr[0] == '[' and expr[-1] == ')':
            raise MismatchingParentheses()
        
        elif expr and expr[0] == '(' and expr[-1] == ']':
            raise MismatchingParentheses()
        
        
        if expr and '[' in expr and expr[-1] == ']':  #x[E1]
            con = expr[:expr.index('[')]
            con1 = expr[expr.index('[')+1:-1]
            con1 = con1.strip()

            con1 = self.evaluate(con1)

            if not is_numeral(con1):
                raise IllegalValue()
            elif con not in self.mem:
                raise UnknownVariable()
            elif type(self.mem[con]) != list:
                raise IllegalValue()
            elif int(con1) > len(self.mem[con]):
                raise IllegalValue()
            return self.mem[con][int(con1)]
        
    
    def execute(self, pc, cmdline):
        if cmdline != '':
            if cmdline[0] == '#':
                return pc + 1
            tokens = cmdline.split()
            command = tokens[0]

            if command == 'jmp':
                condition = cmdline.lstrip(command)
                condition = condition.strip()
                condition1 = condition.split(',')[0]
                label = condition.split(',')[1].strip()

                condition1 = self.evaluate(condition1)

                if not is_numeral(condition1):
                    raise IllegalValue()
                else:
                    condition1 = int(condition1)

                if condition1 != 0:
                    if label not in self.labels:
                        raise UnknownLabel()
                    pc = self.labels[label]
                    
            elif command[-1] == ':':
                command_name = command[:-1]
                self.labels[command_name] = pc

            elif cmdline.split('(')[0] == "print":
                gm = cmdline.strip()[cmdline.strip().index('(')+1:-1].strip()
                
                gm = self.evaluate(gm)
                
                if not is_numeral(gm):
                    raise IllegalValue()
                print(gm)

            elif ' = ' in cmdline:
                parts = cmdline.split(' = ',1)
                var_name = parts[0].strip()
                expr = parts[1].strip()

                if ';' in expr:
                    # x = [E1; E2]
                    list_parts = expr.split(';')
                    e1_expr = list_parts[0].lstrip('[').strip()
                    e2_expr = list_parts[1].rstrip(']').strip()
                    e1_value = self.evaluate(e1_expr)
                    e2_value = self.evaluate(e2_expr)

                    if not is_numeral(e1_value) or not is_numeral(e2_value):
                        raise IllegalValue()

                    list_value = [e1_value] * e2_value
                    self.mem[var_name] = list_value

                elif '[' in var_name:
                    # x[E1] = E2
                    list_name = var_name[:var_name.index('[')]
                    index_expr = var_name[var_name.index('[')+1:-1]
                    index = self.evaluate(index_expr)
                    value = self.evaluate(expr)

                    if not is_numeral(index):
                        raise IllegalValue()

                    if list_name not in self.mem:
                        raise UnknownCommand()
                    
                    if type(self.mem[list_name]) != list:
                        raise IllegalValue()

                    if not is_numeral(value):
                        raise IllegalValue()

                    self.mem[list_name][int(index)] = value
                
                else:
                    # x = E
                    value = self.evaluate(expr)

                    if not is_numeral(value):
                        raise IllegalValue()

                    self.mem[var_name] = value

            else:
                raise UnknownCommand()
        
        return pc + 1


    def run(self, breakpoints):
        self.scan_labels()  
        current_vm = []  

        while self.pc < self.code_lines:
            if self.pc in breakpoints:
                
                current_vm.append(repr(self))

        
            cmdline = self.code[self.pc]

            if '#' in cmdline:
                cmdline = cmdline[:cmdline.index('#')].strip()  # 주석 제거
            
            if not cmdline:  # 주석만 있는 줄인 경우 건너뛰기
                self.pc += 1
                continue

            self.pc = self.execute(self.pc, cmdline)

        return current_vm

        
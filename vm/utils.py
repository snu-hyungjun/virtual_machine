"""
VMO Lab.
Petite-Language Calculator
"""
from .exceptions import *


def is_numeral(s):
    if s == None:
        return False
    
    try:
        int(s)
        return True
    except ValueError:
        return False

    
def is_varname(s):
    if not s:
        return False  
    elif s[0] == '_':
        return False
    for c in s:
        if not (c.islower() or c == '_'):
            return False 

    return True  



def is_labelname(s):
    if not s:
        return False
    elif s[0] == '_':
        return False
    
    for c in s:
        if not(c.isupper() or c== '_'):
            return False
    return True


def is_keyword(s):
    keywords = ['print','input','jmp']
    return s in keywords


def is_getitem(s):
    if len(s) < 4:
        return False

    if s[-1] == ']' and '[' in s[:-1]:
        if s.count(']') == s.count('['):
            return True
        else:
            raise MismatchingBrackets()
    else:
        return False



def in2post(operators, infix_tokens):
    """
    Convert infix token string into postfix.
    (Shunting Yard Algorithm)

    '[' is used to describe subscript.
    e.g., x[4] -> x 4 [
    """
    result = []
    op_stack = []
    if infix_tokens.count(')') != infix_tokens.count('('):
        raise MismatchingParentheses()
    elif infix_tokens.count(']') != infix_tokens.count('['):
        raise MismatchingBrackets()
    for t in infix_tokens:
        if t in operators[0] or t in operators[1] or t in operators[2] or t in operators[3]:
            if t == '[':
                op_stack.append(t)
            elif t == ']':
                while op_stack and op_stack[-1] != '[' and op_stack[-1] != '(':
                    result.append(op_stack.pop())
                if op_stack and op_stack[-1] == '(':
                    raise MismatchingParentheses()
                elif op_stack and op_stack[-1] == '[':
                    result.append(op_stack.pop())
                else:
                    raise MismatchingBrackets()
                
                
            else:
                if t != '(' and t != ')':
                    if t in operators[3]:
                        while op_stack and op_stack[-1] != '(' and op_stack[-1] != '[':
                            result.append(op_stack.pop())
                    
                    elif t in operators[2]:
                        op_stack_number = len(op_stack)
                        for i in range(op_stack_number):
                            if op_stack[-1] in operators[1] or op_stack[-1] in operators[2]:
                                result.append(op_stack.pop())
                    
                    else:
                        op_stack_number = len(op_stack)
                        for i in range(op_stack_number):
                            if op_stack[-1] in operators[1]:
                                result.append(op_stack.pop())
                    op_stack.append(t)        
                else:
                    if t == '(':
                        op_stack.append(t)
                    elif t == ')':
                        while op_stack and op_stack[-1] != '(' and op_stack[-1] != '[':
                            result.append(op_stack.pop())
                        if op_stack and op_stack[-1] == '(' and op_stack[-1] != '[':
                            op_stack.pop()
                        else:
                            raise MismatchingParentheses()
        else:
            result.append(t)
    while op_stack:
        if op_stack[-1] == '(':
            raise MismatchingParentheses()
        if op_stack[-1] == '[':
            raise MismatchingBrackets()
        result.append(op_stack.pop())
    return result


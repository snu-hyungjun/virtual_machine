class PTVMException(Exception):
    pass

class UnknownCommand(PTVMException):
    def __init__(self, message="Unknown Command"):
        self.message = message
        super().__init__(self.message)

class UnknownLabel(PTVMException):
    def __init__(self, message="Unknown Label"):
        self.message = message
        super().__init__(self.message)

class UnknownVariable(PTVMException):
    def __init__(self, message=" Unknown Variable"):
        self.message = message
        super().__init__(self.message)

class IllegalValue(PTVMException):
    def __init__(self, message=" Illegal Value"):
        self.message = message
        super().__init__(self.message)


class SyntaxError(PTVMException):
    pass


class MismatchingParentheses(SyntaxError):
        def __init__(self, message="Mismatching Parentheses"):
            self.message = message
            super().__init__(self.message)

class MismatchingBrackets(SyntaxError):
    def __init__(self, message="Mismatching Brackets"):
        self.message = message
        super().__init__(self.message)
        

class NumericException(PTVMException):
    pass


class OutOfCoverage(NumericException):
    def __init__(self, message="Out of Coverage"):
        self.message = message
        super().__init__(self.message)

class IllegalBitVector(NumericException):
    def __init__(self, message="Illegal Bit Vector"):
        self.message = message
        super().__init__(self.message)

class IllegalType(NumericException):
    def __init__(self, message="Illegal Type"):
        self.message = message
        super().__init__(self.message)

class Overflow(NumericException):
    def __init__(self, message="Overflow"):
        self.message = message
        super().__init__(self.message)

class DivideByZero(NumericException):
    def __init__(self, message="Divide by Zero"):
        self.message = message
        super().__init__(self.message)
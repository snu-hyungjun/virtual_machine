"""
VMO Lab.
Fixed length integers. ixx.
"""
from .exceptions import *


def larger_type(x, y):
    """ Find the larger type """
    if not issubclass(type(x), ixx) or not issubclass(type(y), ixx):
        raise Exception('Illegal Type')

    if x.BIT_LENGTH > y.BIT_LENGTH:
        return type(x)
    else:
        return type(y)


def zext(bitvec, length):
    """ Zero-Extension (in-place) """
    while len(bitvec) < length:
        bitvec.append(0)


def sext(bitvec, length):
    """ Signed-Extension (in-place) """
    msb = bitvec[-1]
    while len(bitvec) < length:
        bitvec.append(msb)


class ixx:
    """
    Base Class for the Fixed Length Integers.
    """
    BIT_LENGTH = 32

    def __init__(self, value):
        # LSB: index 0, MSB: index 31
        self.__bitvec = ()
        is_minus = False

        bitlist = []
        if type(value) == int:
            a = value
            b = 1    
            c = 0
            d = []
            if a >= 2**((self.BIT_LENGTH)-1) or a < -2**((self.BIT_LENGTH)-1):
                raise OutOfCoverage()    
            if a > 0:                                               #입력값이 양수인 경우와 음수인 경우를 분류
                while 2**b <= a:                                    #2진수의 자릿수를 계산
                    b = b + 1                                     
                for i in range(b):
                    c = c + (a // 2**(b - 1)) * 10**(b - 1)          #입력값을 입력값보다 크지 않은 2의 최대 거듭제곱수로 나누고 그 값을 구한 자릿수에 입력
                    a = a % 2**(b-1)                                 #a를 위에서 사용한 값을 뺀 값이지만 그것을 나머지로 구현
                    b = b - 1                                        #그 다음으로 큰 2의 거듭제곱수로 나누기 위해 b에서 1을 빼고 이를 while문으로 끝까지 반복         
                d = [int(digit) for digit in str(c)][::-1]
                zext(d, self.BIT_LENGTH)
                self.__bitvec = tuple(d)

            elif a < 0: 
                while 2**b * (-1) >= a:                             #a가 음수일 때, a값에 -1을 곱해서 2진수 변환을 진행
                    b = b + 1
                for i in range(b):
                    c = c + (-a // 2**(b - 1)) * 10**(b - 1)
                    a = -(-a % 2**(b-1))
                    b = b - 1
                d = [int(digit) for digit in str(c)][::-1]
                zext(d, self.BIT_LENGTH)
                for i in range(len(d)):
                    d[i] = 1- d[i]
                for i in reversed(range(len(d))):
                    if d[i] == 0:
                        d[i] == 1
                        break
                    d[i] = 0
                self.__bitvec = tuple(d)
            elif a == 0:
                d = [0] * 32
                self.__bitvec = tuple(d)
            
        elif type(value) == list:
            if len(value) > self.BIT_LENGTH:
                raise OutOfCoverage()
            
            for i in value:
                if i != 0 and i != 1:
                    raise IllegalBitVector()
            
            self.__bitvec = tuple(sext(value, self.BIT_LENGTH))

        elif issubclass(type(value), ixx):
            if value.BIT_LENGTH > self.BIT_LENGTH:
                raise OutOfCoverage()
            
            self.__bitvec = tuple(sext(value, self.BIT_LENGTH))        
        else:
            try:
                a = int(value)
                b = bin(a)[2:]
                d = [int(digit) for digit in str(b)][::-1]
                zext(d, self.BIT_LENGTH)
                self.__bitvec = tuple(d)
            except:
                raise IllegalType()
            

    def __getitem__(self, idx):
        return self.__bitvec[idx]

    def __repr__(self):
        return f'{int(self)}: {"".join(str(b) for b in self.__bitvec[::-1])}'

    def __int__(self):
        a = 0
        if self.__bitvec[-1] == 0:
            for i in range(len(self.__bitvec)-1):
                a = a + self.__bitvec[-2-i] * 2**(i)
        elif self.__bitvec[-1] == 1:
            for i in range(len(self.__bitvec)-1):
                a = a + (1 - self.__bitvec[-2-i]) * 2**(i)
        return a

    def __str__(self):
        return str(int(self))

    def __pos__(self):
        return self

    def __neg__(self):
        neg_bitvec = []
        for bit in self.__bitvec:
            neg_bitvec.append(1 - bit)
        neg_bitvec[-1] += 1  
        for i in range(len(neg_bitvec) - 1):
            if neg_bitvec[i] > 1:
                neg_bitvec[i] %= 2
                neg_bitvec[i + 1] += 1  
        if neg_bitvec[-1] > 1:
            raise Overflow()
        return self.__class__(neg_bitvec)

    def __add__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        result_bitvec = []
        carry = 0
        max_length = max(len(self.__bitvec), len(other.__bitvec))
        for i in range(max_length):
            bit_sum = self.__bitvec[i] + other.__bitvec[i] + carry
            result_bitvec.append(bit_sum % 2)  
            carry = bit_sum // 2  

        if carry != result_bitvec[-1]:
            raise Overflow()

        return self.__class__(result_bitvec)

    def __sub__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        neg_other = -other
        return self + neg_other

    def __mul__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        result = self.__class__(0)
        for _ in range(other):
            result += self
        return result

    def __truediv__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()
        if other == 0:
            raise DivideByZero()

        quotient = self.__class__(0)
        remainder = self.__class__(0)
        abs_self = abs(self)
        abs_other = abs(other)
        for _ in range(abs_self):
            remainder += abs_other
            if remainder > abs_self:
                break
            quotient += 1

        if (self < 0 and other > 0) or (self > 0 and other < 0):
            quotient = -quotient

        return quotient

    def __abs__(self):
        if self < 0:
            return -self
        else:
            return self

    def __bool__(self):
        return self != 0

    def __eq__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        return int(self) == int(other)

    def __ne__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        return int(self) != int(other)

    def __lt__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        return int(self) < int(other)

    def __gt__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        return int(self) > int(other)

    def __le__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        return int(self) <= int(other)

    def __ge__(self, other):
        if not isinstance(other, ixx):
            raise IllegalType()

        return int(self) >= int(other)



class i8(ixx):
    BIT_LENGTH = 8


class i16(ixx):
    BIT_LENGTH = 16


class i32(ixx):
    BIT_LENGTH = 32


class i64(ixx):
    BIT_LENGTH = 64


if __name__ == '__main__':
    """
    Test as you want.
    """
    x = i32(-999)
    y = i32(10)

    print(x)
    print(y)

    z = x / y

    print(f'{z}: {type(z)}')

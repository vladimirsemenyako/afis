def incrementBinaryByOne(num):
    num.reverse()
    if num[0] == '0':
        num[0] = '1'
    else:
        num[0] = '0'
        for x in range(1, len(num)):
            if num[x] == '0':
                num[x] = '1'
                break
            else:
                num[x] = '0'
    num.reverse()
    return num

def positiveBinaryConversion(num):
    stack = [num]
    binary = []
    while num > 1:
        num = num // 2
        stack.append(num)
    stack.reverse()
    for binNum in stack:
        binary.append(str(binNum % 2))
    while len(binary) < 8:
        binary.insert(0, "0")
    return "".join(binary)

def twoscompliment(num):
    binary = []
    for element in positiveBinaryConversion(-num):
        binary.append('0' if element == '1' else '1')
    binary = incrementBinaryByOne(binary)
    return "".join(binary)

def twoscomplimentForSub(num):
    binary = []
    num_list = list(num)  # split() не нужен
    for element in num_list:
        binary.append('0' if element == '1' else '1')
    binary = incrementBinaryByOne(binary)
    return "".join(binary)

def convertToBinary(num):
    return positiveBinaryConversion(num) if num >= 0 else twoscompliment(num)

def binaryToInt(binary_str):
    n = len(binary_str)
    if binary_str[0] == '1':
        inverted = ''.join(['1' if c == '0' else '0' for c in binary_str])
        num = 0
        for i in range(n):
            if inverted[i] == '1':
                num += (1 << (n - 1 - i))
        num += 1
        return -num
    else:
        num = 0
        for i in range(n):
            if binary_str[i] == '1':
                num += (1 << (n - 1 - i))
        return num

def unsigned_divide(dividend, divisor):
    quotient = 0
    remainder = 0
    if divisor == 0:
        return (0, 0)
    if divisor > dividend:
        return (0, dividend)
    if divisor == dividend:
        return (1, 0)

    num_bits = 32
    mask = 0xFFFFFFFF
    original_dividend = dividend

    d = 0
    for _ in range(num_bits):
        bit = (dividend >> 31) & 1
        remainder = (remainder << 1) | bit
        remainder &= mask
        d = dividend
        dividend = (dividend << 1) & mask
        num_bits -= 1
        if remainder >= divisor or num_bits == 0:
            break

    if remainder >= divisor:
        dividend = d
        remainder = (remainder >> 1) | (bit << 31)
        num_bits += 1
    else:
        dividend = d
        remainder = remainder >> 1
        num_bits += 1

    for _ in range(num_bits):
        bit = (dividend >> 31) & 1
        remainder = (remainder << 1) | bit
        remainder &= mask
        t = (remainder - divisor) & mask
        q = 1 if t <= remainder else 0
        dividend = (dividend << 1) & mask
        quotient = (quotient << 1) | q
        if q:
            remainder = t

    return (quotient, remainder)


def signed_divide(dividend, divisor):
    dend_abs = abs(dividend)
    dor_abs = abs(divisor)
    q, r = unsigned_divide(dend_abs, dor_abs)
    quotient = q
    remainder = r
    if (dividend < 0) != (divisor < 0):
        quotient = -q
    if dividend < 0:
        remainder = -r
    return (quotient, remainder)


def binary_signed_divide(dividend_bin, divisor_bin):
    dividend = binaryToInt(dividend_bin)
    divisor = binaryToInt(divisor_bin)
    quotient, remainder = signed_divide(dividend, divisor)
    quotient_bin = convertToBinary(quotient)
    remainder_bin = convertToBinary(remainder)
    return (quotient_bin, remainder_bin)

def addBinary(num1, num2):
    num1, num2 = list(num1), list(num2)
    added = []
    carry = 0
    for x in range(len(num1) - 1, -1, -1):
        if num1[x] == '0' and num2[x] == '0':
            added.append('1' if carry else '0')
            carry = 0
        elif (num1[x], num2[x]) in [('0', '1'), ('1', '0')]:
            added.append('0' if carry else '1')
        elif num1[x] == '1' and num2[x] == '1':
            added.append('1' if carry else '0')
            carry = 1
    added.reverse()
    return "".join(added)

def rightShift(a, q):
    num = a + q
    shifted = [num[0]] + list(num[:-1])
    return "".join(shifted)[:8], "".join(shifted)[8:]


class BinaryNumber:
    def __init__(self, value):
        if isinstance(value, int):
            self.binary = convertToBinary(value)
        elif isinstance(value, str) and all(c in ('0', '1') for c in value):
            self.binary = value.zfill(8)  # Нормализация длины
        else:
            raise ValueError("Invalid input type")

    def __repr__(self):
        return f"{self.binary} ({self.to_int()})"

    def __add__(self, other):
        other = self._ensure_binary(other)
        result = addBinary(self.binary, other.binary)
        return BinaryNumber(result)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        other = self._ensure_binary(other)
        result = multByBooth(self.binary, other.binary)
        return BinaryNumber(result)

    def __truediv__(self, other):
        other = self._ensure_binary(other)
        quotient, remainder = binary_signed_divide(self.binary, other.binary)
        return BinaryNumber(quotient), BinaryNumber(remainder)

    def __neg__(self):
        negated = twoscomplimentForSub(self.binary)
        return BinaryNumber(negated)

    def _ensure_binary(self, other):
        if not isinstance(other, BinaryNumber):
            return BinaryNumber(other)
        return other

    def to_int(self):
        return binaryToInt(self.binary)


# Модифицированная функция умножения с полным результатом
def multByBooth(m, q):
    a = "00000000"
    q_neg1 = "0"
    q_neg0 = q[-1]
    for _ in range(len(m)):
        if q_neg0 == "1" and q_neg1 == "0":
            a = addBinary(a, twoscomplimentForSub(m))
        elif q_neg0 == "0" and q_neg1 == "1":
            a = addBinary(a, m)
        q_neg1 = q_neg0
        a, q = rightShift(a, q)
        q_neg0 = q[-1]
    full_result = a + q  # Объединяем регистры A и Q
    return full_result


# Остальные функции остаются без изменений
# [Здесь должны быть все ваши оригинальные функции]

# Пример использования
if __name__ == "__main__":
    a = BinaryNumber(5)
    b = BinaryNumber(3)

    print("\nСложение:")
    res_add = a + b
    print(res_add)

    print("\nВычитание:")
    res_sub = a - b
    print(res_sub)

    print("\nУмножение:")
    res_mul = a * b
    print(res_mul)


    print("\nДеление:")
    res_div, rem_div = a / b
    print("Частное:", res_div)
    print("Остаток:", rem_div)
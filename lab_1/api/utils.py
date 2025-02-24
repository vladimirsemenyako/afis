def increment_binary_by_one(num):
    num.reverse()
    if num[0] == '0':
        num[0] = '1'
    else:
        num[0] = '0'
        for i in range(1, len(num)):
            if num[i] == '0':
                num[i] = '1'
                break
            else:
                num[i] = '0'
    num.reverse()
    return num

def positive_binary_conversion(num):
    stack = [num]
    binary = []
    while num > 1:
        num //= 2
        stack.append(num)
    stack.reverse()
    for value in stack:
        binary.append(str(value % 2))
    while len(binary) < 8:
        binary.insert(0, "0")
    return "".join(binary)

def twos_complement(num):
    binary = []
    for bit in positive_binary_conversion(-num):
        binary.append('0' if bit == '1' else '1')
    binary = increment_binary_by_one(binary)
    return "".join(binary)

def twos_complement_for_sub(num):
    binary = []
    num_list = list(num)
    for bit in num_list:
        binary.append('0' if bit == '1' else '1')
    binary = increment_binary_by_one(binary)
    return "".join(binary)

def convert_to_binary(num):
    return positive_binary_conversion(num) if num >= 0 else twos_complement(num)

def binary_to_int(binary_str):
    length = len(binary_str)
    if binary_str[0] == '1':
        inverted = ''.join(['1' if c == '0' else '0' for c in binary_str])
        num = sum((1 << (length - 1 - i)) for i in range(length) if inverted[i] == '1')
        return -num - 1
    return sum((1 << (length - 1 - i)) for i in range(length) if binary_str[i] == '1')

def binary_divide_with_fraction(dividend, divisor, frac_digits=5):
    if divisor == 0:
        raise ZeroDivisionError("Division by zero")
    total_bits = 8 + frac_digits
    result = dividend / divisor
    scaled = int(round(result * (2 ** frac_digits)))
    if scaled < 0:
        scaled = (1 << total_bits) + scaled
    fixed_bin = format(scaled, f'0{total_bits}b')
    return fixed_bin[:8] + '.' + fixed_bin[8:]

def add_binary(num1, num2):
    num1, num2 = list(num1), list(num2)
    added = []
    carry = 0
    for i in range(len(num1) - 1, -1, -1):
        if num1[i] == '0' and num2[i] == '0':
            added.append('1' if carry else '0')
            carry = 0
        elif (num1[i], num2[i]) in [('0', '1'), ('1', '0')]:
            added.append('0' if carry else '1')
        else:
            added.append('1' if carry else '0')
            carry = 1
    added.reverse()
    return "".join(added)

def right_shift(a, q):
    num = a + q
    shifted = [num[0]] + list(num[:-1])
    return "".join(shifted)[:8], "".join(shifted)[8:]

def multiply_by_booth(m, q):
    a = "00000000"
    q_neg1 = "0"
    q_neg0 = q[-1]
    for _ in range(len(m)):
        if q_neg0 == "1" and q_neg1 == "0":
            a = add_binary(a, twos_complement_for_sub(m))
        elif q_neg0 == "0" and q_neg1 == "1":
            a = add_binary(a, m)
        q_neg1 = q_neg0
        a, q = right_shift(a, q)
        q_neg0 = q[-1]
    return a + q

class BinaryNumber:
    def __init__(self, value):
        if isinstance(value, int):
            self.binary = convert_to_binary(value)
        elif isinstance(value, str) and all(c in ('0', '1') for c in value):
            self.binary = value.zfill(8)
        else:
            raise ValueError("Invalid input type")

    def __repr__(self):
        return f"{self.binary} ({self.to_int()})"

    def __add__(self, other):
        other = self._ensure_binary(other)
        return BinaryNumber(add_binary(self.binary, other.binary))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        other = self._ensure_binary(other)
        return BinaryNumber(multiply_by_booth(self.binary, other.binary))

    def __truediv__(self, other):
        other = self._ensure_binary(other)
        return binary_divide_with_fraction(self.to_int(), other.to_int())

    def __neg__(self):
        return BinaryNumber(twos_complement_for_sub(self.binary))

    def _ensure_binary(self, other):
        return other if isinstance(other, BinaryNumber) else BinaryNumber(other)

    def to_int(self):
        return binary_to_int(self.binary)

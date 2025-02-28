import math

class BinaryNumber:
    def __init__(self, value):
        if isinstance(value, int):
            self.binary = BinaryNumber._convert_to_binary(value)
        elif isinstance(value, str) and set(value) <= {'0', '1'}:
            self.binary = value.zfill(8)
        else:
            raise ValueError("Invalid input type")

    def __repr__(self):
        return f"{self.binary} ({self.to_int()})"

    def __add__(self, other):
        other = self._ensure_binary(other)
        return BinaryNumber(BinaryNumber._add_binary(self.binary, other.binary))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        other = self._ensure_binary(other)
        return BinaryNumber(BinaryNumber._multiply_by_booth(self.binary, other.binary))

    def __truediv__(self, other):
        other = self._ensure_binary(other)
        return BinaryNumber._binary_divide_with_fraction(self.to_int(), other.to_int())

    def __neg__(self):
        return BinaryNumber(BinaryNumber._twos_complement_for_sub(self.binary))

    def _ensure_binary(self, other):
        return other if isinstance(other, BinaryNumber) else BinaryNumber(other)

    def to_int(self):
        return BinaryNumber._binary_to_int(self.binary)

    @staticmethod
    def _increment_binary_by_one(num_list):
        num_list.reverse()
        if num_list[0] == '0':
            num_list[0] = '1'
        else:
            num_list[0] = '0'
            for i in range(1, len(num_list)):
                if num_list[i] == '0':
                    num_list[i] = '1'
                    break
                else:
                    num_list[i] = '0'
        num_list.reverse()
        return num_list

    @staticmethod
    def _positive_binary_conversion(num):
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

    @staticmethod
    def sign_mode(num):
        num = BinaryNumber._positive_binary_conversion(abs(num))
        num = '1' + num[1:]
        return num

    @staticmethod
    def ones_complement(num):
        bin_num = []
        num = BinaryNumber._positive_binary_conversion(abs(num))
        for bit in num[1:]:
            bin_num.append('0' if bit == '1' else '1')
        return '1' + "".join(bin_num)


    @staticmethod
    def twos_complement(num):
        binary = []
        pos_conv = BinaryNumber._positive_binary_conversion(-num)
        for bit in pos_conv:
            binary.append('0' if bit == '1' else '1')
        binary = BinaryNumber._increment_binary_by_one(list(binary))
        return "".join(binary)

    @staticmethod
    def _twos_complement_for_sub(binary_str):
        binary = []
        for bit in binary_str:
            binary.append('0' if bit == '1' else '1')
        binary = BinaryNumber._increment_binary_by_one(binary)
        return "".join(binary)

    @staticmethod
    def _convert_to_binary(num):
        if num >= 0:
            return BinaryNumber._positive_binary_conversion(num)
        else:
            return BinaryNumber.twos_complement(num)

    @staticmethod
    def _binary_to_int(binary_str):
        length = len(binary_str)
        if binary_str[0] == '1':
            inverted = ''.join(['1' if c == '0' else '0' for c in binary_str])
            num = sum((1 << (length - 1 - i)) for i, c in enumerate(inverted) if c == '1')
            return -num - 1
        else:
            return sum((1 << (length - 1 - i)) for i, c in enumerate(binary_str) if c == '1')

    @staticmethod
    def _binary_divide_with_fraction(dividend, divisor, frac_digits=5):
        if divisor == 0:
            raise ZeroDivisionError("Division by zero")
        total_bits = 8 + frac_digits
        result = dividend / divisor
        scaled = int(round(result * (2 ** frac_digits)))
        if scaled < 0:
            scaled = (1 << total_bits) + scaled
        fixed_bin = format(scaled, f'0{total_bits}b')
        return fixed_bin[:8] + '.' + fixed_bin[8:]

    @staticmethod
    def _add_binary(num1, num2):
        num1_list = list(num1)
        num2_list = list(num2)
        added = []
        carry = 0
        for i in range(len(num1_list) - 1, -1, -1):
            if num1_list[i] == '0' and num2_list[i] == '0':
                added.append('1' if carry else '0')
                carry = 0
            elif (num1_list[i], num2_list[i]) in [('0', '1'), ('1', '0')]:
                added.append('0' if carry else '1')
            else:
                added.append('1' if carry else '0')
                carry = 1
        added.reverse()
        return "".join(added)

    @staticmethod
    def _right_shift(a, q):
        num = a + q
        shifted = [num[0]] + list(num[:-1])
        return "".join(shifted)[:8], "".join(shifted)[8:]

    @staticmethod
    def _multiply_by_booth(m, q):
        a = "00000000"
        q_neg1 = "0"
        q_neg0 = q[-1]
        for _ in range(len(m)):
            if q_neg0 == "1" and q_neg1 == "0":
                a = BinaryNumber._add_binary(a, BinaryNumber._twos_complement_for_sub(m))
            elif q_neg0 == "0" and q_neg1 == "1":
                a = BinaryNumber._add_binary(a, m)
            q_neg1 = q_neg0
            a, q = BinaryNumber._right_shift(a, q)
            q_neg0 = q[-1]
        return a + q


class IEEE754Float:
    def __init__(self, value):
        if isinstance(value, float):
            self.value = value
            self.bits = IEEE754Float._float_to_binary(value)
        elif isinstance(value, str) and len(value) == 32 and set(value) <= {'0', '1'}:
            self.bits = value
            self.value = IEEE754Float._binary_to_float(value)
        else:
            raise ValueError("Invalid input type. Provide a float or a 32-bit binary string.")

    def __add__(self, other):
        if not isinstance(other, IEEE754Float):
            other = IEEE754Float(other)
        sign1, exp1, frac1 = self.bits[0], int(self.bits[1:9], 2), self.bits[9:]
        sign2, exp2, frac2 = other.bits[0], int(other.bits[1:9], 2), other.bits[9:]
        if sign1 != '0' or sign2 != '0':
            raise ValueError("Only positive numbers are supported")
        M1 = (1 << 23) | int(frac1, 2) if exp1 != 0 else int(frac1, 2)
        M2 = (1 << 23) | int(frac2, 2) if exp2 != 0 else int(frac2, 2)
        if exp1 > exp2:
            shift = exp1 - exp2
            M2 >>= shift
            exp = exp1
        else:
            shift = exp2 - exp1
            M1 >>= shift
            exp = exp2
        M_result = M1 + M2
        if M_result >= (1 << 24):
            M_result >>= 1
            exp += 1
        frac_result = M_result - (1 << 23)
        exp_bits = format(exp, '08b')
        frac_bits = format(frac_result, '023b')
        result_bits = '0' + exp_bits + frac_bits
        return IEEE754Float(result_bits)

    def __repr__(self):
        return f"IEEE-754: {self.bits} | Float: {self.value}"

    @staticmethod
    def _float_to_binary(num):
        if num == 0.0:
            return "0" * 32
        sign_bit = '0' if num >= 0 else '1'
        num_abs = abs(num)
        m, e = math.frexp(num_abs)
        bias = 127
        exponent = e - 1 + bias

        if exponent <= 0:
            exponent = 0
            fraction = int(num_abs / (2 ** (1 - bias)) * (1 << 23))
        else:
            fraction = int(((m * 2) - 1) * (1 << 23))

        exponent_bits = format(exponent, '08b')
        fraction_bits = format(fraction, '023b')
        return sign_bit + exponent_bits + fraction_bits

    @staticmethod
    def _binary_to_float(bstr):
        sign = int(bstr[0])
        exponent = int(bstr[1:9], 2)
        fraction = int(bstr[9:], 2)
        bias = 127

        if exponent == 0:
            value = fraction / (1 << 23) * (2 ** (1 - bias))
        else:
            value = (1 + fraction / (1 << 23)) * (2 ** (exponent - bias))
        if sign == 1:
            value = -value
        return value

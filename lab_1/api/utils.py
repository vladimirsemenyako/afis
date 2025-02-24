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

# Новая функция деления, возвращающая фиксированное представление частного с дробной частью (до 5 битов после разделителя)
def binary_divide_with_fraction(dividend, divisor, frac_digits=5):
    if divisor == 0:
        raise ZeroDivisionError("Division by zero")
    # Определяем суммарное число бит: 8 бит для целой части + frac_digits для дробной
    total_bits = 8 + frac_digits
    # Вычисляем результат деления как число с плавающей точкой
    result = dividend / divisor
    # Масштабируем результат для фиксированной точки (с дробной частью)
    scaled = int(round(result * (2 ** frac_digits)))
    # Если результат отрицательный, представляем его в виде двух дополнений
    if scaled < 0:
        scaled = (1 << total_bits) + scaled
    # Представляем число в виде строки с фиксированным количеством бит
    fixed_bin = format(scaled, '0{}b'.format(total_bits))
    # Вставляем разделитель между целой и дробной частями
    int_part = fixed_bin[:8]
    frac_part = fixed_bin[8:]
    return int_part + '.' + frac_part

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

# Модифицированная функция умножения с использованием алгоритма Бута
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
    full_result = a + q  # объединяем регистры A и Q
    return full_result

class BinaryNumber:
    def __init__(self, value):
        if isinstance(value, int):
            self.binary = convertToBinary(value)
        elif isinstance(value, str) and all(c in ('0', '1') for c in value):
            self.binary = value.zfill(8)  # нормализуем до 8 бит
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

    # Новый оператор деления: возвращает строку с фиксированным двоичным представлением частного с дробной частью
    def __truediv__(self, other):
        other = self._ensure_binary(other)
        dividend = self.to_int()
        divisor = other.to_int()
        result = binary_divide_with_fraction(dividend, divisor, frac_digits=5)
        return result

    def __neg__(self):
        negated = twoscomplimentForSub(self.binary)
        return BinaryNumber(negated)

    def _ensure_binary(self, other):
        if not isinstance(other, BinaryNumber):
            return BinaryNumber(other)
        return other

    def to_int(self):
        return binaryToInt(self.binary)

# Новый класс для представления 32-битных чисел с плавающей точкой по стандарту IEEE-754-2008
class IEEE754Float:
    def __init__(self, value):
        if isinstance(value, float):
            self.value = value
            self.bits = self.float_to_binary(value)
        elif isinstance(value, str) and len(value) == 32 and set(value) <= {'0', '1'}:
            self.bits = value
            self.value = self.binary_to_float(value)
        else:
            raise ValueError("Invalid input type. Provide a float or a 32-bit binary string.")

    def float_to_binary(self, num):
        import struct
        packed = struct.pack('!f', num)
        return ''.join(f'{b:08b}' for b in packed)

    def binary_to_float(self, bstr):
        import struct
        bytes_val = bytes(int(bstr[i:i+8], 2) for i in range(0, 32, 8))
        return struct.unpack('!f', bytes_val)[0]

    # Сложение двух положительных чисел с плавающей точкой по стандарту IEEE-754
    def __add__(self, other):
        if not isinstance(other, IEEE754Float):
            other = IEEE754Float(other)
        # Извлекаем экспоненту и мантиссу (с неявной единицей для нормализованных чисел)
        exp1 = int(self.bits[1:9], 2)
        exp2 = int(other.bits[1:9], 2)
        frac1 = int(self.bits[9:], 2)
        frac2 = int(other.bits[9:], 2)
        M1 = (1 << 23) | frac1 if exp1 != 0 else frac1
        M2 = (1 << 23) | frac2 if exp2 != 0 else frac2

        # Выравниваем экспоненты
        if exp1 > exp2:
            shift = exp1 - exp2
            M2 >>= shift
            exp = exp1
        else:
            shift = exp2 - exp1
            M1 >>= shift
            exp = exp2

        # Суммируем мантиссы
        M_result = M1 + M2

        # Нормализуем результат
        if M_result >= (1 << 24):  # если произошёл перенос
            M_result >>= 1
            exp += 1

        # Отбрасываем неявную единицу
        frac_result = M_result - (1 << 23)
        exp_bits = format(exp, '08b')
        frac_bits = format(frac_result, '023b')
        result_bits = '0' + exp_bits + frac_bits
        return IEEE754Float(result_bits)

    def __repr__(self):
        return f"IEEE-754: {self.bits} | Float: {self.value}"

# Примеры использования

# Операции с целыми числами в двоичном представлении
a = BinaryNumber(-6)
b = BinaryNumber(3)
print("Деление:")
result_div = a / b  # результат теперь выводится в виде фиксированного двоичного представления (8 бит целой части и 5 бит дробной)
print(result_div)

# Операции с плавающей точкой по стандарту IEEE-754
print("\nСложение чисел с плавающей точкой:")
a_float = IEEE754Float(21.12)
b_float = IEEE754Float(4.13)
c_float = a_float + b_float
print(c_float)  # например, для 21.12 + 4.13 выводится соответствующее 32-битное представление IEEE-754

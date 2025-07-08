from functools import lru_cache

def find_pair_digit_dp(d):
    if d == 0:
        return 0, 0
    
    if d % 9 != 0:
        return None
    digits = list(map(int, str(d)[::-1])) + [0]
    L = len(digits)
    max_delta = 9 * L


    @lru_cache(None)
    def dfs(pos, carry, delta):

        if pos == L:
           return [] if (carry == 0 and delta == 0) else None
    
        d_i = digits[pos] if pos < L else 0

        for a_i in range(10):
            s = a_i + d_i + carry
            b_i = s % 10
            new_carry = s // 10

            new_delta = delta + (a_i - b_i)
            if abs(new_delta) > max_delta:
                continue
            
            res = dfs(pos + 1, new_carry, new_delta)
            if res is not None:
                return [a_i] + res
            
        return None
    
    a_digits = dfs(0, 0, 0)
    if a_digits is None:
        return None
    a = 0
    for i, digit in enumerate(a_digits):
        a += digit * (10 ** i)
    b = a + d
    return a, b


with open('Number Pairs/N3/N3.in', 'r') as infile, \
     open('Number Pairs/N3/N3_SOL.txt', 'w') as outfile:
    next(infile)
    for line in infile:
        number = int(line.strip())
        result = find_pair_digit_dp(number)
        if result:
            a, b = result
            outfile.write(f'{a} {b}\n')
        else:
            outfile.write('NONE' + '\n')
        
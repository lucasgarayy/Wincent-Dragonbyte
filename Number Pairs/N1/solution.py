def sum_digits(n):
    return sum(int(d) for d in str(n))

def find_pair(d):
    for a in range(1, 10000):
        b = d + a
        if sum_digits(a) == sum_digits(b):
            return a, b
    return "NONE"

with open('N1.in', 'r') as infile, \
     open('N1.txt', 'w') as outfile:
    next(infile)
    for line in infile:
        number = int(line.strip())
        a,b = find_pair(number)
        outfile.write(f'{a} ' + f'{b}' + '\n')
        
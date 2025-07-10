def sum_digits(n):
    return sum(int(d) for d in str(n))

def find_pair(d):
    for a in range(1, 1000000):
        b = d + a
        if sum_digits(a) == sum_digits(b):
            return a, b
    return None

with open('Number Pairs/N2/N2.in', 'r') as infile, \
     open('Number Pairs/N2/N2_BF.txt', 'w') as outfile:
    next(infile)
    for line in infile:
        number = int(line.strip())
        solution = find_pair(number)
        if solution:
            a, b = solution
            outfile.write(f'{a} ' + f'{b}' + '\n')
        else:
            outfile.write('NONE' + '\n')
        
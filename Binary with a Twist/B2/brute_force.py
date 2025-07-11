import math 
def base_d(n):
    if n == 0 or n==1 or n==3 or n==10:
        return 3
    if n == 2:
        return -1
    
    limit = int(math.isqrt(n)) + 1
    for d in range(3, limit):
        if d > n:
            break
        temp = n
        valid = True
        while temp:
            if temp % d > 1:
                valid = False
                break
            temp = temp // d
        if valid:
            return d
    return n - 1

with open('Binary with a Twist/B2/B2.in', 'r') as infile, \
     open('Binary with a Twist/B2/B2_SOL.txt', 'w') as outfile:
     next(infile)
     for line in infile:
         number = int(line.strip())
         d = base_d(number)
         outfile.write(f'{d}' +'\n')
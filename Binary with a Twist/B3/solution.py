from tqdm import tqdm
import math 
def base_d(n):
    if n <= 3:
        return 3 if n != 2 else -1
    
    L = n.bit_length()

    for k in range(L-1, 1, -1):
        d0 = int(round(n ** (1.0/k)))

        for d in (d0-1, d0, d0+1):
            if d <= 2 or d == n-1:
                continue
            temp = n
            valid = True
            while temp:
                if temp % d > 1:
                    valid = False
                    break
                temp //= d
            if valid:
                return d

    return n - 1

with open('Binary with a Twist/B3/B3.in', 'r') as infile, \
     open('Binary with a Twist/B3/B3.txt', 'w') as outfile:
     next(infile)
     for line in tqdm(infile):
         number = int(line.strip())
         d = base_d(number)
         outfile.write(f'{d}' +'\n')
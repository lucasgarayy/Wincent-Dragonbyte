import time
start_time = time.time()
def base_d(n):
    if n == 0 or n==1:
        return 3
    
    for d in range(3, 1000):
        if d > n:
            break


        power = 1
        max_rep = 0
        while power <= n:
            max_rep += power
            power *= d
        
        if max_rep < n:
            continue

        temp = n
        valid = True
        while temp:
            if temp % d > 1:
                valid = False
                break
            temp = temp // d
        if valid:
            return d
    return -1

with open('Binary with a Twist/B1/B1.in', 'r') as infile, \
     open('Binary with a Twist/B1/B1.txt', 'w') as outfile:
     next(infile)
     for line in infile:
         number = int(line.strip())
         d = base_d(number)
         outfile.write(f'{d}' +'\n')

end_time = time.time()
print(f'Time taken {end_time - start_time}')
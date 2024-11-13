## extensible performance-testing framework for implementations of tuberosum counting algorithm
## applications are incredibly obvious and require no discussion

from utime import ticks_us
t = ticks_us
t0 = t()
potato_count = 1

for test in range(1000000):
    
    # benchmarked @ 9.45881 µs per kilopotato on RPi Pico (spud rate: 105.722 Mpotato/s)
    while potato_count < 999:
        for n in range(3): # '1 potato etc'
            potato_count += 1
        if potato_count == 4: # 'four'
            potato_count += 1
        else: # 'more'
            potato_count += 1
            
    """
    # 9.45949 µs per kilopotato (spud rate: 105.714 Mpotato/s)
    while potato_count < 1001:
        while potato_count % 4 > 0:
            #print(potato_count, ' potato')
            potato_count += 1
        if potato_count == 4:
            pass #print('four')
        else:
            pass #print('more')
        potato_count += 1
    """
∆t = t() - t0

print(f'{potato_count-1:,}', 'potatoes counted', f'{test+1:,}', 'times in', f"{∆t:,}", 'µs')
print(f'{∆t/((potato_count-1)*(test+1))*1000:,}', 'µs per kilopotato')
print('spud rate:', f'{(test+1)/∆t*1000:,.3f}', 'Mpotato/s')
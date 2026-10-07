vehicle = ['train', 'bus', 'car', 'ship']
try:
    vehicle.extend(10)
except TypeError as e:
    print('TypeError:', e)

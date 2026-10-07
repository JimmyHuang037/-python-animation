vehicle = ['train', 'bus', 'car', 'ship']
try:
    vehicle.append(10, 11)
except TypeError as e:
    print('TypeError:', e)

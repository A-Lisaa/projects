#-*- coding: utf-8 -*-
a = {2: 60, 4: 45, 8: 30, 16: 15, 32: 0}
for i in range(1, 20):
    a[2**(i+5)] = 360-15*i
print(a)
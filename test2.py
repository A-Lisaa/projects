import os
import time

a = os.listdir("E:\\Эротические фотокарточки\\Хентай (полноразмерный)")

start_time = time.time()

# counter = 0
# for elem in a:
#     counter += 1
counter = len(a)
    
print(time.time()-start_time)
    
print(counter)
print(len(a))
import random
import time

test_list = [1, 2, 3, 4, 5, 6]

for x in test_list:
    print(test_list.pop(random.randrange(len(test_list))))
    time.sleep(1)

"""
For & While Loops
"""

my_list = [1, 2, 3, 4, 5, 6]

for i in my_list:
    print(i)

i = 0
while i < len(my_list):
    i += 1
    if i == 3: continue     # continue on
    if i == 4: break        # break
    print(i)
else:
    print("i is now larger than the size of the list")  # Does not print on break
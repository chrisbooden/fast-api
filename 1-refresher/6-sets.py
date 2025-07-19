"""
Sets are similar to lists but are unordered and cannot contain duplicates
Tuples are similar to a set but can refer to an item at an index (tuples are immutable)
"""

my_set = {1, 2, 4, 5, 6, 1, 2}
print(my_set)

# Unordered and so cannot get element at an index
# cannot go my_set[0]

print(len(my_set))  # 5

for x in my_set:
    print(x)


if (4 in my_set):
    print("4 in the set")


# Union
my_set_2 = { 10, 20, 30}
my_set.update(my_set_2)

print(my_set)


# Tuple
my_tuple = (1, 2, 3, 4, 5)

print(my_tuple[2])

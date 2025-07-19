"""
Lists are a collection of data
"""

x = [1, 2, 3, 4, 5]

print(x[0])
print(x[-1])
print(x[0:3])       # slice
print(x[-3::-1])
print(x[-1::-2])

print(len(x))

y = range(1, len(x)+1)
print(type(y))      # type range and not a list
print(list(y))      # convert to a list


# Append
x.append(6)
print(x)

# Insert
x.insert(1,10)
print(x)

# Remove last element
x.pop()
print(x)

# Remove last element and return
z = x.pop()
print(f"z = {z}")

# Remove an element
x.remove(1)     # Remove first occurence of a value
print(x)

# Extend a list
y = [20, 30, 40]
x.extend(y)

print(x)

z = [x**2 for x in range(0,10)]
print(z)


# Test
zoo = ["cat", "dog", "frog", "snake", "lion"]

# Remove third element
animal = zoo.pop(2)
print(animal)

# Remove a lion
zoo.remove("lion")
print(zoo)

# Add a monkey
zoo.append("monkey")
print(zoo)

# Print first 3
print(zoo[0:3])



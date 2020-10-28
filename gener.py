some_string = "hello"
string_iterator = iter(some_string)

some_list = [1,2,3,4,5]
list_iterator = iter(some_list)
# We can call next(iterator) to get the next value 
# in the container
# print(next(string_iterator))

# print(next(list_iterator))


def some_generator():
    yield 1
    yield 2
    yield 3

# for value in some_generator():
#     print(value)

# print(next(some_generator()))



def fibonacci():
    first,second = 0,1
    while True:
        yield first
        first,second=second,first+second



print(next(fibonacci()))


for value in fibonacci():
    if value > 100:
        break
    print(value, " ")



list_comprehension_example = [n**2 for n in range(11)]
generator_expression_example = (n**2 for n in range(11))

print(list_comprehension_example) # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
print(generator_expression_example) # <generator object <genexpr> at 0x01413EA0>

print(next(generator_expression_example))
print(next(generator_expression_example))
print(next(generator_expression_example))
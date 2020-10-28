def sleep(name):
    return name + " sleeping"

def eat(name):
    return name + " eating"

def human_action(action_function):
    return action_function("John")

print(human_action(sleep))



def my_decorator(func):
    def inner_decorator():
        print("Adding decorator")
        func()
    return inner_decorator



# decorated_function = my_decorator(normal_function)
# decorated_function() 


def my_first_decorator(func):
    def inner_decorator():
        print("Adding first decorator")
        func()
        print("End of first decorator")
    return inner_decorator

def my_second_decorator(func):
    def inner_decorator():
        print("Adding second decorator")
        func()
        print("End of second decorator")

    return inner_decorator


@my_first_decorator
@my_second_decorator
def normal_function():
    print("Do something")

normal_function()


def smart_decorator(func):
    def inner(*args, **kwargs):
        for arg in args:
            print(arg)
        for kwarg in kwargs.items():
            print(kwarg)
        print("I can decorate any function")
        return func(*args, **kwargs)
    return inner


@smart_decorator
def people_attirbutes(name,surname,age):
    print(name,surname,age)

people_attirbutes("John", "Doe", 32)
people_attirbutes(age=28, name="Mary", surname="Jane")

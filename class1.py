# The arguments appointed and arguments not positioned in the function Python
def sum_numbers(x,y):
    # Definition
    print(f'{x=} {y=}', '|', 'x+y= ', x+ y)
    
sum_numbers(5, 10)  # Positional arguments
sum_numbers(x=5, y=10)  # Keyword arguments

print(1,2,3, sep='.')
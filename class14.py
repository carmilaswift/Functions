# Escopo means the location where that one can to achieve the code
x = 1

def escopo():
    x = 11 # the global variable x is remove protected inside the function escopo()
    def other_function():
        y = 2
        print(x,y)

    other_function()
    print(x)

# you can't modify the variable x inside the function escopo() \ 
# because is the protected variable
escopo()
print(x)
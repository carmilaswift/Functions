def calculator():
    print("Simple Calculator")
    print("Operations: +, -, *, /, ** (power), % (modulus)")
    
    while True:
        try:
            num1 = float(input("\nEnter first number: "))
            op = input("Enter operation (+, -, *, /, **, %) or 'q' to quit: ")
            
            if op.lower() == 'q':
                print("Goodbye!")
                break
            
            num2 = float(input("Enter second number: "))
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    print("Error: Cannot divide by zero")
                    continue
                result = num1 / num2
            elif op == '**':
                result = num1 ** num2
            elif op == '%':
                if num2 == 0:
                    print("Error: Cannot divide by zero")
                    continue
                result = num1 % num2
            else:
                print("Invalid operation")
                continue
            
            print(f"Result: {num1} {op} {num2} = {result}")
        
        except ValueError:
            print("Invalid input, please enter numbers.")

if __name__ == "__main__":
    calculator()
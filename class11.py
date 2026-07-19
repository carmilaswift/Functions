"""
Temperature Converter Module
Converts between Celsius, Fahrenheit, and Kelvin
"""


class TemperatureConverter:
    """A class to convert between different temperature units."""
    
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def celsius_to_kelvin(celsius):
        """Convert Celsius to Kelvin."""
        return celsius + 273.15
    
    @staticmethod
    def kelvin_to_celsius(kelvin):
        """Convert Kelvin to Celsius."""
        return kelvin - 273.15
    
    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit):
        """Convert Fahrenheit to Kelvin."""
        celsius = TemperatureConverter.fahrenheit_to_celsius(fahrenheit)
        return TemperatureConverter.celsius_to_kelvin(celsius)
    
    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        """Convert Kelvin to Fahrenheit."""
        celsius = TemperatureConverter.kelvin_to_celsius(kelvin)
        return TemperatureConverter.celsius_to_fahrenheit(celsius)


def main():
    """Main function to demonstrate temperature conversions."""
    print("=" * 50)
    print("Temperature Converter")
    print("=" * 50)
    
    while True:
        print("\nSelect conversion type:")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Celsius to Kelvin")
        print("4. Kelvin to Celsius")
        print("5. Fahrenheit to Kelvin")
        print("6. Kelvin to Fahrenheit")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '7':
            print("Thank you for using Temperature Converter!")
            break
        
        if choice not in ['1', '2', '3', '4', '5', '6']:
            print("Invalid choice. Please try again.")
            continue
        
        try:
            value = float(input("Enter the temperature value: "))
            
            if choice == '1':
                result = TemperatureConverter.celsius_to_fahrenheit(value)
                print(f"{value}°C = {result:.2f}°F")
            elif choice == '2':
                result = TemperatureConverter.fahrenheit_to_celsius(value)
                print(f"{value}°F = {result:.2f}°C")
            elif choice == '3':
                result = TemperatureConverter.celsius_to_kelvin(value)
                print(f"{value}°C = {result:.2f}K")
            elif choice == '4':
                result = TemperatureConverter.kelvin_to_celsius(value)
                print(f"{value}K = {result:.2f}°C")
            elif choice == '5':
                result = TemperatureConverter.fahrenheit_to_kelvin(value)
                print(f"{value}°F = {result:.2f}K")
            elif choice == '6':
                result = TemperatureConverter.kelvin_to_fahrenheit(value)
                print(f"{value}K = {result:.2f}°F")
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    main()

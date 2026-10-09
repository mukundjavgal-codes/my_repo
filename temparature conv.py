import sys

unit = input("enter the unit of your temperature (celsius 'c' or kelvin 'k' or fahrenheit 'f'):")
if unit not in ["celsius", "kelvin", "fahrenheit", "c", "k", "f"]:
    print("WHAT are we doing my guy")
    sys.exit()
temp = float(input("enter the temperature you want to convert "))
if unit == "celsius" or unit == "c":
    temp = (temp*9/5) + 32
    temp2= temp + 273
    print(f"the temperature in fahrenheit is {round(temp, 2)}F"
          f" and in kelvin, {round(temp2, 2)}K")
elif unit == "kelvin" or unit == "k":
    temp -= 273
    temp2 = (temp - 273) * 9/5 + 32
    print(f"the temperature in celsius is {round(temp, 2)}C"
          f" and in fahrenheit, {round(temp2, 2)}F")
elif unit == "fahrenheit" or unit == "f":
    temp = (temp - 32)*5/9
    temp2 = (temp - 32) * 5/9 + 273
    print (f"the temperature in celsius is {round(temp, 2)}C"
           f" and in kelvin, {round(temp2, 2)}K")

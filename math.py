import math
#there are functions called math.ciel or math.floor which round a number down or up
#for example 9.2 floored would be 9 and cieled would be 10
#to print circumference and area of a circle
r = float(input("enter the radius of your circle:"))
x = math.pi
def calc_circumference():
    return 2*x*r
def calc_area():
    return x*(r**2)
circumference = calc_circumference()
idk1 = calc_area()
print (f"the circumference of your circle would be: {round(idk, 2)}")
print (f"the area of your circle would be: {round(idk1, 2)}")

#prog for pythagoras th
side1 = float(input("enter the first side of your triangle:"))
side2 = float(input("enter the second side of your triangle:"))
def calc_hypotenuse():
    return math.sqrt((side1**2) + (side2**2))
hypotenuse_length = calc_hypotenuse()
print(f"the length of hypotenuse of triangle is: {round(hypotenuse_length, 2)}")
foods = []
price = 0
while True:
    food = input("enter food you want to buy (q or Q to quit):")
    if food == 'q' or food == 'Q':
            break
    else:
        price_food = float(input("enter the price of the item:"))
        foods.append(food)
        price = price + price_food
    if not food.isalpha():
        print ("you have not entered anything!")
        food = input("enter food you want to buy (q or Q to quit):")
print("--- YOUR SHOPPING LIST ---")
for food in foods:
    print (food)
total_price = price + (5/100 * price)
print ("total price is (INCLUDES GST AMOUNT OF 5%):",total_price)


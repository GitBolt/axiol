sum_value = 0 # didn't used the variable name "sum" as it's an inbuilt function
count = 0
for i in range(10):
    inp = int(input("Enter number: "))
    if (inp % 2 != 0):
        sum_value += inp
        count += 1
        avg = sum_value/count
print("The total of the odd numbers is", sum_value, end="")
print(" and their average is", avg)
from random import randint
GREEN = '\033[92m'
RESET = '\033[0m'
print(GREEN)
for i in range(50000):
    for j in range(100):
        print(f"{randint(0,1)}",end=" ")
    print()
print(RESET)
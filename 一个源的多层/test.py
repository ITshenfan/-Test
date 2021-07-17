

A = 2
def print_hi():
    global A
    A = A + 1
    print(A)
    if(A > 5) :
        return
    print_hi()

if __name__ == '__main__':
    print_hi()






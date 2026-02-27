# random concept:

# given code fails when we don't use `global a` line for python,
# but if we write the same code in lox it will work. cuase in lox
# local variable is shadowed until it gets assigned. so our interpreter
# looks for the variable with that name from outer scope and when it finds 
# it, it uses that variable. to allow this behaviour in python we use global 
# keyword, which tells the function to take the variable from global scope and
# not to create a new variable. so it work fundamentally different then lox
# as it does not create new variable rather just updatas the variable from 
# previous scope.
a = 1
def main():
    global a
    a = a + 2
    print(a)

print(a)

main()

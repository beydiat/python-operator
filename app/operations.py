def add(op1, op2):
    return op1 + op2

def sub(op1, op2):
    return op1 - op2

def div(op1, op2):
    try:
        result = op1/op2
    except ZeroDivisionError:
        result = 0
    return result

def puis(op1, op2):
    return pow(op1, op2)
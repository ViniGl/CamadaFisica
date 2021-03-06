def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


# Performs Modulo-2 division
def mod2div(divident, divisor):

    # Number of bits to be XORed at a time.
    pick = len(divisor)

    # Slicing the divident to appropriate
    # length for particular step
    tmp = divident[0 : pick]

    while pick < len(divident):

        if tmp[0] == '1':

            # replace the divident by the result
            # of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + divident[pick]

        else:   # If leftmost bit is '0'

            # If the leftmost bit of the dividend (or the
            # part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an
            # all-0s divisor.
            tmp = xor('0'*pick, tmp) + divident[pick]

        # increment pick to move further
        pick += 1

    # For the last n bits, we have to carry it out
    # normally as increased value of pick will cause
    # Index Out of Bounds.
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)

    checkword = tmp
    return checkword

# Function used at the sender side to encode
# data by appending remainder of modular divison
# at the end of data.
def encodeData(data, key):
    data = str(int.from_bytes(data,"big"))

    l_key = len(key)

    # Appends n-1 zeroes at end of data
    appended_data = data + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)
    remainder = bin(int(remainder,2))
    remainder = int(remainder, 2)
    # print("remainder: {} {}".format(remainder, type(remainder)))
    # Append remainder in the original data
    return remainder
'''
key = "1001"

ans = encodeData(data,key)
print(ans)
s.sendall(ans)


# receive data from the server
print s.recv(1024)

# close the connection
s.close() '''

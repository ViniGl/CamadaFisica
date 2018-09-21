# First of all import the socket library
import socket

# Importado do Geeksforgeeks.com

def crc (data, key):
    def xor(a, b):

        # initialize result
        result = []

        # Traverse all bits, if bits are
        # same, then XOR is 0, else 1
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

    # Function used at the receiver side to decode
    # data received by sender
    def decodeData(data, key):
        data = str(int.from_bytes(data,"big"))

        l_key = len(key)

        # Appends n-1 zeroes at end of data
        appended_data = data + '0'*(l_key-1)
        remainder = mod2div(appended_data, key)
        remainder = bin(int(remainder,2))
        remainder = int(remainder, 2)
        print("remainder: {} {}".format(remainder, type(remainder)))
        # Append remainder in the original data
        return remainder
        
    ans = decodeData(data, key)
    ans = int(ans).to_bytes(1,'big')
        # print("Remainder after decoding is->"+ans)
    return (int(str(int.from_bytes(ans,byteorder='big'))))
    # If remainder is all zeros then no error occured
    # temp = "0" * (len(key) - 1)
    # if ans == temp:
    #     c.sendall("THANK you Data ->"+data + " Received No error FOUND")
    # else:
    #     c.sendall("Error in data")

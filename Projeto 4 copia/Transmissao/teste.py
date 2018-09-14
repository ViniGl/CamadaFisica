def contains(small, big):
    l_small = len(small)
    l_big = len(big)
    i = 0
    c = []

    while i < len(big)-1:
    	if big[i] == small[0] and big[i+1] == small[1] and big[i+2] == small[2]:
    		c.append([i,i+1])
    	i += 1

    return c

a = [1,2]
b = [1,2,6,3]
c = [1,2,6,1,2]

d = contains(a,b)
e = contains(a,c)

print(d)
print(e)
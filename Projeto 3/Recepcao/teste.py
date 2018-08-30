
lista = [5,0,25,0,65,0,12,0,248,0,5,0,7,0,3,0,1,3,0,2,0,1,0]
eop = [3,2,1]


def eop_e_desstuffing(lista,eop,byte_stuffing):
    queue = []
    eop_pos = 0
    for i in range(len(lista)):
        #
        queue.append(lista[i])
        if len(queue) >= 3:
            print(queue[-3:])
            if queue[-3:] == eop:
                print(queue[-3:])
                eop_pos = i-2
        if len(queue) >= 6:
            print(queue[-6:])
            if queue[-6:] == byte_stuffing:
                del(queue[-5])
                del(queue[-3])
                del(queue[-1])
        i += 1
    return eop_pos, queue



print(eop_e_desstuffing(lista,eop,[3,0,2,0,1,0])[1])






# lista = []
# a = (170).to_bytes(1,'big')
# for i in range(50):
#     lista.append(a)
#
# def checkStuff(lista):
#     i = 0
#
#     while i < len(lista):
#         check = lista[i]
#         target = a
#         stuff = (0).to_bytes(1,'big')
#         if check == target:
#             try:
#                 t1 = lista[i+1]
#                 t2 = lista[i+3]
#                 if t1 != stuff and t2 == stuff:
#                     return True
#             except:
#                 pass
#         i +=1
#
#
#
# print(lista)

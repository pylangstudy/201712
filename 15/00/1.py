import socket
s1, s2 = socket.socketpair()
b1 = bytearray(b'----')
b2 = bytearray(b'0123456789')
b3 = bytearray(b'--------------')
print(s1.send(b'Mary had a little lamb'))
print(s2.recvmsg_into([b1, memoryview(b2)[2:9], b3]))
print([b1, b2, b3])

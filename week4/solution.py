from oracle import *
import sys

if len(sys.argv) < 2:
    print("Usage: python sample.py <filename>")
    sys.exit(-1)

f = open(sys.argv[1])
msg_forged = f.read()
f.close()

# strip down to 64 characters (textfile always has nullcharacter for example)
msg_forged = msg_forged[:64]
print(msg_forged)

Oracle_Connect()

#msg_forged = "I, the server, hereby agree that I will pay $100 to this student"
quarter = len(msg_forged)/4
msg_0 = msg_forged[         :  quarter]
msg_1 = msg_forged[  quarter:2*quarter]
msg_2 = msg_forged[2*quarter:3*quarter]
msg_3 = msg_forged[3*quarter:]

# Mac'(msg_forged)       := F_k(m3 xor F_k(m2 xor F_k(m1 xor F_k(m0))))
# Mac(two_block_message) :=                       F_k(m1 xor F_k(m0))

tag_1 = Mac(msg_0+msg_1, len(msg_0+msg_1))

# xor tag_1 into msg_2 to simulate a four block mac oracle:
# Mac(m2 xor tag_1) = F_k(m3 xor F_k(      m2 xor tag_1        ))
#                   = F_k(m3 xor F_k(m2 xor F_k(m1 xor F_k(m0))))
# which is exactly the tag we need for our forged message

msg_2 = ''.join(chr(ord(m)^t) for m, t in zip(msg_2, tag_1))
tag_2 = Mac(msg_2+msg_3, len(msg_2+msg_3))

if Vrfy(msg_forged, len(msg_forged), tag_2):
    print("Message verified successfully!")
else:
    print("Message verification failed.")

Oracle_Disconnect()

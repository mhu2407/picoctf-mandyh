# Semantic Security 101

This problem demonstrates the notion of the semantic security game using a type
of transposition cipher called a route cipher. The game works as follows:

  1. The server flips a coin bit={0,1} on each connection.
  2. A user connects to the server, and chooses either to a) encrypt or b)
     solve.
  3. If the user chooses encrypt <M1,M2>, the server will act like an encryption
     oracle. The user must give two messages M1,M2 with len(M1)=len(M2). The
     server returns the encryption of M_{bit}.
  4. When the user chooses "solve b", they are asked what is the bit.  If they
     choose correctly, they get back the encryption of the flag. If they guess
     incorrectly, they are told so.
     
     
This game differs from true CPA semantic security on step (4) because we require
the user to decrypt the flag. Semantic security only requires the user to guess
right with prob > 1/2. 

To win, the user just needs to ask for an encryption of two blocks, such as:
encrypt(AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC)

The server's bit is 0 if the ciphertext repeats itself after 16 bytes, while it is 1 otherwise)


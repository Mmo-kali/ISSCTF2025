use radare command 

r2 -d filename 

then in radare type: aaa

then type (LIST ALL FUNCTIONS) : afl 

then type: s.FunctionName

then type: s address of the printf

then type dc 



______________________________
STEP1:
r2 -d DoYouDare
THEN TYPE aaa
[0x7f397e091810]> aaa
Then TYPE afl
[0x7f397e091810]> afl


STEP2: 
[0x7f397e091810]> s 0x559a6d7c8199 (address of sym.base64_decode) 
[0x559a6d7c8199]> pdf


STEP3: 
[0x559a6d7c8311]> s 0x559a6d7c8311
[0x559a6d7c8311]> wa nop
INFO: Written 1 byte(s) (nop) = wx 90 @ 0x559a6d7c8311
[0x559a6d7c8311]> wa nop
INFO: Written 1 byte(s) (nop) = wx 90 @ 0x559a6d7c8311
[0x559a6d7c8311]> wa jmp 0x559a6d7c8321
INFO: Written 2 byte(s) (jmp 0x559a6d7c8321) = wx eb0e @ 0x559a6d7c8311
[0x559a6d7c8311]> wq

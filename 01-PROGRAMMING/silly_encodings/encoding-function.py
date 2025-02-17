message = "redacted"

alphabet = {
"a":"gtr4",
"b":"r7yrje",
"c":"gtfs5",
"d":"gt",
"e":"fr3h",
"f":"rew34",
"g":"hr",
"h":"rsjl",
"i":"gje",
"j":"fr3",
"k":"jki",
"l":"gtfs",
"m":"rew",
"n":"rxhbv",
"o":"fr3hrx",
"p":"fg4t",
"q":"rj",
"r":"fr34rs",
"s":"rts", 
"t":"fr34",
"u":"fr3hrt",
"v":"4g",
"w":"gje3",
"x":"4r",
"y":"jki4",
"z":"r7y",
" ":"f53d7",
".":"234v5",
}
encoded = ""
for i in message:
    encoded += alphabet[i.lower()]

print(encoded)



'''
===================
===================
Below is th function to obtain the flag, you need the original message in order to obtain it by passing it as an argument
===================
===================
'''

#flag with message as substitution flag key
def substitution_flag(original_message):
    keys = [50, 89, 99, 121, 26, 235, 247, 166, 383, 266, 39, 282, 397, 338, 78, 141, 302]
    print('bhbureauCTF{', end='')
    for sub in keys:
        
        print(message[sub], end='')
    print('}')

substitution_flag(message)

import strutils, nimcrypto

var 
    b : char
    e : char
    te : seq[char]
    c11 : seq[char]
    c12 : seq[char]
    c13 : seq[char]
    c14 : seq[char]
    c21 : seq[char]
    c22 : seq[char]
    c23 : seq[char]
    c31 : seq[char]
    c32 : seq[char]
    c33 : seq[char]
    c34 : seq[char]
    c35 : seq[char]


proc ob (i: seq[char]) : seq[char] =
    var r : seq[char]
    var c = 0
    while c < i.len:
        case c:
            of 0:
                r.add(chr(ord(i[c]) xor 2))
                c += 1
            of 1:
                r.add(chr(ord(i[c]) xor 3))
                c += 1
            of 2:
                r.add(chr(ord(i[c]) xor 5))
                c += 1
            of 3:
                r.add(chr(ord(i[c]) xor 7))
                c += 1
            of 4:
                r.add(chr(ord(i[c]) xor 9))
                c += 1
            of 5:
                r.add(chr(ord(i[c]) xor 11))
                c += 1
            of 6:
                r.add(chr(ord(i[c]) xor 13))
                c += 1
            of 7:
                r.add(chr(ord(i[c]) xor 17))
                c += 1
            of 8:
                r.add(chr(ord(i[c]) xor 19))
                c += 1
            of 9:    
                r.add(chr(ord(i[c]) xor 23))
                c += 1
            of 10:
                r.add(chr(ord(i[c]) xor 29))
                c += 1
            else:
                c += 1
    return r

proc ini =
    b = '{'
    e = '}'
    te = @['S', '3', 'C']
    c11 = ob(te)
    te = @['_', 'M', '1', 'S', 'S', 'I', 'L', 'E']
    c12 = ob(te)
    te = @['_', 'A', '5', 'S', 'U', 'R', 'E', 'D']
    c13 = ob(te)
    te = @['I', 'K', 'E']
    c14 = ob(te)
    te = @['O', 'N', 'D', '_']
    c21 = ob(te)
    te = @['C', 'U', 'B', 'A', 'N']
    c22 = ob(te)
    te = @['_', 'C', 'R', '1', 'S', 'I', 'S']
    c23 = ob(te)
    te = @['M', 'U', 'T', 'U']
    c31 = ob(te)
    te = @['A', 'L']
    c32 = ob(te)
    te = @['S', '7', 'R']
    c33 = ob(te)
    te = @['_', 'D', 'E', 'S', 'T']
    c34 = ob(te)
    te = @['R', 'U', 'C', 'T', 'I', 'O', 'N']
    c35 = ob(te)


proc de (i: seq[char]) : seq[char] =
    var r : seq[char]
    var c = 0
    while c < i.len:
        case c:
            of 0:
                r.add(chr(ord(i[c]) xor 2))
                c += 1
            of 1:
                r.add(chr(ord(i[c]) xor 3))
                c += 1
            of 2:
                r.add(chr(ord(i[c]) xor 5))
                c += 1
            of 3:
                r.add(chr(ord(i[c]) xor 7))
                c += 1
            of 4:
                r.add(chr(ord(i[c]) xor 11))
                c += 1
            of 5:
                r.add(chr(ord(i[c]) xor 13))
                c += 1
            of 6:
                r.add(chr(ord(i[c]) xor 17))
                c += 1
            of 7:
                r.add(chr(ord(i[c]) xor 19))
                c += 1
            of 8:
                r.add(chr(ord(i[c]) xor 23))
                c += 1
            of 9:
                r.add(chr(ord(i[c]) xor 29))
                c += 1
            else:
                c += 1
    return r


proc chk (i: string) : int =
    const o = "D6DA551D6E5B40C2F61F49174D657"
    const o1 = "9B718B37958F35F"
    const o2 = "874E780CD7BD08979C89"
    const ox = o1 & o2 & o
    const f = "CBD745BB1124E89A90DF0DC740F5E9081C4AC90DDE949047852F6F7598E94028"
    var s =  "ICBM" & "Guid" & "Sys"
    var h = sha256.digest(i & s)
    let c = $h
    case c:
        of ox:
            c11 = ob (c11)
            c21 = ob (c21)
            c33 = ob (c33)
            c14 = ob (c14)
            return 1
        of f:
            c22 = de (c22)
            c12 = de (c12)
            c23 = de (c23) 
            return -1
        else:
            return 0


proc mn =
    ini()
    echo "------------------------------------------------------------"
    echo "\t\tWelcome to ICBM control system"
    echo "------------------------------------------------------------"
    stdout.write("Enter your secret key: ")
    var k = stdin.readLine()
    var rc = chk(k)
    case rc:
        of 1:
            stdout.write("Your requested resource is: ")
            stdout.write(b)
            stdout.write(c11.join("") & c21.join("") & c33.join("") & c14.join(""))
            stdout.write(e)
        of -1:
            stdout.write("Your requested resource is: ")
            stdout.write(b)
            stdout.write(c22.join("") & c12.join("") & c23.join(""))
            stdout.write(e)
        else:
            echo "Invalid key"

mn()
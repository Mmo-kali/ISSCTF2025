uwu:
    ; create a new stack frame
    push ebp
    mov ebp, esp
    sub esp, 0x28           ; Allocate space for local variables (80 bytes)

    ; store function name (WinExec)
    xor eax, eax
    push eax
    push 0x636578
    push 0x456E6957
    mov [ebp - 0x04], esp   ; Store pointer to "WinExec\x00" in var 4

    ; look for kernel32.dll base address
    xor eax, eax
    mov ebx, [fs:0x30 + eax]    ; PEB
    mov ebx, [ebx + 0x0C]       ; PEB_LDR_DATA
    mov ebx, [ebx + 0x14]       ; InMemoryOrderModuleList (first entry)
    mov ebx, [ebx]              ; Flink (ntdll.dll)
    mov ebx, [ebx]              ; Flink (kernel32.dll)
    mov ebx, [ebx + 0x10]       ; BaseAddress
    
    mov [ebp - 0x8], ebx    ; Store kernel32.dll base address in var 8
    
    ; look for address of Address Table, Name Pointer Table & Ordinal Table in kernel32.dll
    mov eax, [ebx + 0x3C]   ; PE Signature RVA (base + 0x3C)
    add eax, ebx            ; PE Signature addr.
    mov eax, [eax + 0x78]   ; Export Table RVA (PE addr. + 0x78)
    add eax, ebx            ; Export Table addr.

    mov edx, [eax + 0x14]   ; Number of exported functions
    
    mov ecx, [eax + 0x1C]   ; RVA of Address Table (Export Table addr. + 0x1C)
    add ecx, ebx            ; Addr. of Address Table
    mov [ebp - 0x0C], ecx   ; Store Address Table addr. in var C
    
    mov ecx, [eax + 0x20]   ; RVA of Name Pointer Table (Export Table addr. + 0x20)
    add ecx, ebx            ; Addr. of Name Pointer Table
    mov [ebp - 0x10], ecx   ; Store Name Pointer Table addr. in var 10
    
    mov ecx, [eax + 0x24]   ; RVA of Ordinal Table (Export Table addr. + 0x24)
    add ecx, ebx            ; Addr. of Ordinal Table
    mov [ebp - 0x14], ecx   ; Store Ordinal Table addr. in var 14
    
    xor eax, eax            ; counter for keeping track of position

    ; look for the string
    .scan:
        mov edi, [ebp - 0x10]   ; Name Pointer Table addr.
        mov esi, [ebp - 0x04]   ; String "WinExec"
        xor ecx, ecx            ; clearing the character counter
        cld                     ; clear direction flag to read strings left to right
        
        ; since we're moving the base address of Name Pointer Table in edi every turn,
        ; and each entry is 4 bytes, just increment by the position (eax) * 4 bytes
        ; that gets us the RVA of n'th entry
        mov edi, [edi + eax * 0x04]
        add edi, ebx    ; get addr. of n'th entry

        add cx, 0x07    ; Num of bytes to be compared in "WinExec"
        repe cmpsb      ; repeat until equal, compare esi and edi byte by byte
        jz uwu.good     ; if match is found (ZF=1), jump to the label 'good'
        
        inc eax         ; increment counter
        cmp eax, edx    ; compare if we reached the last exported function
        jb uwu.scan     ; if eax < edx, continue loop
        
        jmp uwu.fin
    
    ; if the string is found
    .good:
        mov edx, [ebp - 0x14]   ; Addr. of Ordinal Table
        mov ecx, [ebp - 0x0C]   ; Addr. of Address Table
        
        ; move the Ordinal Number into eax (Ordinal Base + Position * Bytes in Each Entry)
        movzx eax, word [edx + eax * 0x02]
        ; move the RVA into eax (Address Table base + Ordinal Number * Bytes in Each Entry)
        mov eax, [ecx + eax * 0x04]
        add eax, ebx            ; get actual address of function by adding to kernel32 base
        
        ; call the function with args "C:\Windows\System32\cmd.exe /c "ShadowCTF{Cookie_FOR_your_hardWork}" > flag.txt"
        ; don't worry about unescaped characters, they'll be normalised when pushing into stack anyways
        xor edx, edx
        push edx
        ;push message: 
        push 0x7478742e
        push 0x67616c66
        push 0x203e2022
        push 0x7d6b726f
        push 0x57647261
        push 0x685f7275
        push 0x6f795f52
        push 0x4f465f65
        push 0x696b6f6f
        push 0x437b4654
        push 0x43776f64
        push 0x61685322
        push 0x206f6863
        push 0x6520632f
        push 0x20657865
        push 0x2e646d63
        push 0x5c32336d
        push 0x65747379
        push 0x535c7377
        push 0x6f646e69
        push 0x575c3a43

        mov esi, esp        ; esi -> "C:\Windows\System32\cmd.exe /c "ShadowCTF{Cookie_FOR_your_hardWork}" > flag.txt"
        
        push 0x0A           ; Window State SW_DEFAULT (10)
        push esi            ; push pointer to command string
        call eax            ; Invoke WinExec

    ; cleanup    
    .fin:
        add esp, 0x54
        pop ebp
        ret

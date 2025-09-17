"                            * "
"str" set

"str" get "newstr" set

0 while dup 30 < do
    "str" get . 
    0 while dup 28 < do
        dup
        "newstr" get swap
        dup
        dup 0 + "str" get swap idx swap
        dup 1 + "str" get swap idx swap
            2 + "str" get swap idx
        "*" = if 1 else 0 end swap
        "*" = if 2 else 0 end + swap
        "*" = if 4 else 0 end +
        while 1 do // switch case
            dup 0 = if " " break end 
            dup 1 = if "*" break end
            dup 2 = if "*" break end
            dup 3 = if "*" break end
            dup 4 = if " " break end
            dup 5 = if "*" break end
            dup 6 = if "*" break end
            dup 7 = if " " break end 
            break // default
        whileend 
        swap drop swap 
        1 + swap 
        setidx "newstr" set
        1 +
    whileend drop
    "newstr" get "str" set
    1 +
whileend drop


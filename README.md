# $name
Recreational Programming Language focusing on list manipulation

# data types
There are only two data types in $name. Numbers, and lists. Lists can only contain numbers. All numbers are Python `int`s, `float`s, or `complex`s. Literals can only generate `float`s and `complex`s, but `int`s can be obtained through functions. `int`s and `float`s that are divisible by `1` are treated the same way.

# syntax
The syntax for $name is fairly intuitive if you know the syntax of [Jelly](https://github.com/DennisMitchell/jelly). Since there are only numbers and lists, all other syntactical components are just shorthand for numbers. List syntax doesn't exist because it's covered by string syntax, which is almost always shorter anyway.

`”a`: single character literal. Yields `ord('a')`  
`\n`: single escaped character literal. Yields `ord('\n')`  
`"ab"`: double character literal. Yields `[ord('a'), ord('b')]`  
`‷abc`: triple character literal. Yields `[ord('a'), ord('b'), ord('c')]`
`“...”`: string literal. Backslash escaping is supported. Use `#...` with a valid number literal to insert a number into the string. All characters are then converted to numbers using `ord`, giving a list of numbers.  
`“...“...”`: string list literal. Backslash escaping is supported. Use `#...` with a valid number literal to insert a number into the string. All character are then converted to numbers using `ord`, giving a list of lists of numbers.  
`...‴`: String literal; like `“...”` but without open quote. Deletes every token before it and turns all of the code up until then into a string. Note that the last occurrence of `‴` denotes the superstring because any later ones will delete the previous one.  
`-?`: Negative number literal. Without a number, `-1`.  
`?.?`: Decimal number literal. Left argument defaults to `0`. Right argument defaults to `.5`. Without arguments, `0.5`.  
`?ı?`: Complex number literal. Left argument defaults to `0`. Right argument defaults to `1j`.  
`?ȷ?`: Scientific notation literal. Left argument defaults to `1`. Right argument defaults to `⨉10³`

# logic/control flow
$name is stack-based, but operations that require more values than present will take command line/default arguments to save some bytes here and there.

# long functions
`∑...}`: Sum with a certain (monadic) function.  
`∃...}`: There exists a value that satisfies a certain predicate (monadic).  
`∄...}`: Inverse of the above.  
`∀...}`: Apply function to each element.  
`þ...}`: Sort by a (monadic) key function.  
`Þ...}`: Sort with a (dyadic) comparator function.  

# short functions
symbol|description
-|-
`!`|Pi/Factorial function
`B`|Convert number to binary digits
`D`|Convert number to decimal digits
`F`|Flatten list
`L`|Length
`H`|Divide number by 2
`R`|Range `[1..n]`
`W`|`n -> [n]`
`w`|Wraps the entire stack into one list
`⊹`|Pops the first element from the stack and unwraps it
`‥`|Range `[x..y]`
`…`|Range `[x..x+z....y]`
`¹`|Identity function (actually useless for stack-based languages...)
`²`|Squared (behaves predictably but much differently for lists, which vectorize on both sides)
`³`|First argument or `32` (`' '`)
`⁴`|Second argument or `10` (`'\n'`)
`⁵`|Third argument or `[]`
`⁶`|Fourth argument or `16`
`⁷`|Fifth argument or `64`
`⁸`|Sixth argument or `100`
`⁹`|Seventh argument or `256`
`₁₂₃₄₅₆₇₈₉`|Get the `n`-th `1`-indexed element from the array at the top, or from the digits of the number at the top
`π`|Constant PI (3.14)
`τ`|Constant TAU (6.28)
`ϕ`|Constant PHI (1.62)
`+`|Vectorizing addition
`_`|Vectorizing subtraction
`⨉`|Vectorizing multiplication
`*`|Vectorizing product
`∏`|Product of list/range of number
`Σ`|Sum of list/range of number
`Δ`|Differences; Increments

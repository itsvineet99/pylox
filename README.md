jlox is an tree-walk interpreter written in java for custom built language lox. both the language and interpreter are implemented in a book "[crafting interpreters](https://craftinginterpreters.com/)" by [Bob Nystrom](https://stuffwithstuff.com/).

in this repository i re-implemnt jlox in python. the purpose of doing so is to learn more about python and what differs it from statistically typed language like java.

in pylox we implement all the given things:
- tokens and lexing
- abstract syntax trees
- recursive descent parsing
- prefix and infix expressions
- runtime representation of objects
- interpreting code using the Visitor pattern
- lexical scope
- environment chains for storing variables
- control flow
- functions with parameters
- closures
- static variable resolution and error detection
- classes
- constructors
- fields
- methods
- and finally inheritance

how to use the interpreter:

```
git clone https://github.com/itsvineet99/pylox.git
cd pylox
cd src
```

once inside `src`, type given command to interprete from source file:

```
python lox.py <path_to_source_code>
```
this command will interprete the code from a file at given path and print output on terminal.

visual representation of running lox program using our interpreter:

![interpreter.py](https://i.ibb.co/93vhf5wP/image.png)

to use REPL (read–eval–print loop) mode, type given command:

```
python lox.py
```

after typing above command you can use REPL. here you can enter you code, for example,

```
var a = 23;
var b = 23;
var c = a + b;
print c;
```

press ctr+D to quit out of REPL version.

you can use example files from `tests/` repository to see how code is written in lox and to see how pylox interpretes it.

for ease of running all test cases at once you can use `test_script.py` which interpreters all the tests programs and prints output to your terminal.

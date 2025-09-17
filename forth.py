#! /usr/bin/python3

# pyforth!

import copy
import os

iota_counter = 0
def iota(reset = False):
    global iota_counter
    if reset: iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

class Loc:
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def __str__(self):
        return f"{self.line}: {self.col}"
    def __repr__(self):
        return self.__str__()

class Op:
    def __init__(self, op, args, loc):
        self.op = op
        self.args = args
        self.loc = loc
    Plus         = iota(True)
    Sub          = iota()
    Mul          = iota()
    Div          = iota()
    Pow          = iota()
    Eq           = iota()
    Lt           = iota()
    Gt           = iota()
    Not          = iota()
    Push         = iota()
    Dup          = iota()
    Drop         = iota()
    Over         = iota()
    Swap         = iota()
    Dump         = iota()
    If           = iota()
    Else         = iota()
    End          = iota()
    While        = iota()
    Do           = iota()
    WhileEnd     = iota()
    Break        = iota()
    Continue     = iota()
    Index        = iota()
    StoreAtIndex = iota()
    SetVar       = iota()
    GetVar       = iota()
    Debug        = iota()
    COUNT        = iota()

stack = []
bindings = {}

def simulate_program(program):
    global stack
    global bindings
    ip = 0
    assert Op.COUNT == 28, "Exhaustive handling of Ops"
    while ip < len(program):
        curr = program[ip]
        if curr.op == Op.Plus:
            fst = stack.pop()
            snd = stack.pop()
            stack.append(fst + snd)
            ip += 1
        elif curr.op == Op.Sub:
            fst = stack.pop()
            snd = stack.pop()
            stack.append(snd - fst)
            ip += 1
        elif curr.op == Op.Mul:
            fst = stack.pop()
            snd = stack.pop()
            stack.append(fst * snd)
            ip += 1
        elif curr.op == Op.Div:
            fst = stack.pop()
            snd = stack.pop()
            stack.append(snd / fst)
            ip += 1
        elif curr.op == Op.Pow:
            fst = stack.pop()
            snd = stack.pop()
            stack.append(snd ** fst)
            ip += 1
        elif curr.op == Op.Eq:
            fst = stack.pop()
            snd = stack.pop()
            if fst == snd:
                stack.append(1)
            else:
                stack.append(0)
            ip += 1
        elif curr.op == Op.Lt:
            fst = stack.pop()
            snd = stack.pop()
            if fst > snd:
                stack.append(1)
            else:
                stack.append(0)
            ip += 1
        elif curr.op == Op.Gt:
            fst = stack.pop()
            snd = stack.pop()
            if fst < snd:
                stack.append(1)
            else:
                stack.append(0)
            ip += 1
        elif curr.op == Op.Not:
            cond = stack.pop()
            if cond == 1:
                stack.append(0)
            else:
                stack.append(1)
            ip += 1
        elif curr.op == Op.Push:
            stack.append(curr.args[0])
            ip += 1
        elif curr.op == Op.Dump:
            v = stack.pop()
            print("+", v)
            ip += 1
        elif curr.op == Op.Dup:
            v = stack.pop()
            stack.append(v)
            stack.append(v)
            ip += 1
        elif curr.op == Op.Drop:
            stack.pop()
            ip += 1
        elif curr.op == Op.Over:
            a = stack.pop()
            b = stack.pop()
            stack.append(b)
            stack.append(a)
            stack.append(b)
            ip += 1
        elif curr.op == Op.Swap:
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
            ip += 1
        elif curr.op == Op.If:
            cond = stack.pop()
            if cond == 0:
                ip = curr.args[0]
            else:
                ip += 1
        elif curr.op == Op.Else:
            ip = curr.args[0]
        elif curr.op == Op.End:
            ip += 1
        elif curr.op == Op.While:
            ip += 1
        elif curr.op == Op.Do:
            cond = stack.pop()
            if cond == 0:
                ip = curr.args[0]
            else:
                ip += 1
        elif curr.op == Op.WhileEnd:
            ip = curr.args[0]
        elif curr.op == Op.Break:
            ip = curr.args[0]
        elif curr.op == Op.Continue:
            ip = curr.args[0]
        elif curr.op == Op.Index:
            idx = stack.pop()
            lis = stack.pop()
            stack.append(lis[idx])
            ip += 1
        elif curr.op == Op.StoreAtIndex:
            val = stack.pop()
            idx = stack.pop()
            lis = stack.pop()
            lisstart = lis[:idx]
            lisend = lis[idx + 1:]
            stack.append(lisstart + val + lisend)
            ip += 1
        elif curr.op == Op.SetVar:
            name = stack.pop()
            value = stack.pop()
            bindings.update({name: value})
            ip += 1
        elif curr.op == Op.GetVar:
            name = stack.pop()
            stack.append(bindings[name])
            ip += 1
        elif curr.op == Op.Debug:
            print("DEBUG")
            for (idx, i) in enumerate(stack[::-1]):
                print(f"! {idx}: {repr(i)}")
            print("DEBUG")
            ip += 1
        else:
            assert False, "unreachable"
    return stack

def configure_blocks(pgrm):
    program = copy.deepcopy(pgrm)
    ip = len(program) - 1
    if_stack = []
    while_stack = []
    assert Op.COUNT == 28, "Exhaustive handling of Ops"
    while ip >= 0:
        curr = program[ip]
        if curr.op == Op.If:
            curr.args = [if_stack.pop() + 1]
            ip -= 1
        elif curr.op == Op.Else:
            curr.args = [if_stack.pop() + 1]
            if_stack.append(ip)
            ip -= 1
        elif curr.op == Op.End:
            if_stack.append(ip)
            ip -= 1
        elif curr.op == Op.Do:
            curr.args = [while_stack.pop() + 1]
            ip -= 1
        elif curr.op == Op.WhileEnd:
            while_stack.append(ip)
            ip -= 1
        elif curr.op == Op.Break:
            curr.args = [while_stack[-1] + 1]
            ip -= 1
        else:
            ip -= 1
    ip = 0
    whileend_stack = []
    assert Op.COUNT == 28, "Exhaustive handling of Ops"
    while ip < len(program):
        curr = program[ip]
        if curr.op == Op.While:
            whileend_stack.append(ip)
            ip += 1
        elif curr.op == Op.Continue:
            curr.args = [whileend_stack[-1] + 1]
            ip += 1
        elif curr.op == Op.WhileEnd:
            curr.args = [whileend_stack.pop() + 1]
            ip += 1
        else:
            ip += 1
    return program

def read_lines_from_file(filepath, content = ""):
    if content == "":
        with open(filepath, "r") as f:
            text = f.read()
            return [x.split('//')[0] for x in text.splitlines()]
    else:
        return [x.split('//')[0] for x in content.splitlines()]

preprocessor_macros = {
    "sqrt" : "0.5 ^",
}

def get_line_tokens(line, linenum):
    if line.startswith("!"):
        if line.startswith("!alias "):
            l = line.removeprefix("!alias ") + " "
            idx = l.find(" ")
            name = l[:idx]
            to = l[idx + 1:]
            preprocessor_macros.update({ name : to })
        elif line.startswith("!unalias "):
            del preprocessor_macros[line.removeprefix("!unalias ")]
        else:
            raise Exception("Unrecognised command in execution")
        return []

    ct = 0
    acc_tok = ""
    quoted = False
    escaped = False
    res = []
    while ct < len(line):
        if quoted:
            if not escaped and line[ct] == "\"":
                acc_tok += line[ct]
                quoted = False
                res.append((acc_tok, Loc(linenum, ct)))
                acc_tok = ""
            elif not escaped and line[ct] == "\\" and quoted:
                escaped = True
            elif escaped:
                escaped = False
                acc_tok += line[ct]
            else:
                acc_tok += line[ct]
        else:
            if line[ct] == "\"":
                quoted = True
                acc_tok += line[ct]
            elif line[ct].isspace():
                if acc_tok != "":
                    res.append((acc_tok, Loc(linenum, ct)))
                    acc_tok = ""
            else:
                acc_tok += line[ct]
        ct += 1
    if acc_tok != "":
        res.append((acc_tok, Loc(linenum + 1, ct + 1)))
    return res

def lex_line(line, linenum):
    res = []
    tokens = get_line_tokens(line, linenum)
    for (token, loc) in tokens:
        if token in preprocessor_macros:
            st = preprocessor_macros[token]
            for t in get_line_tokens(preprocessor_macros[token], 0):
                res.append(t)
        else:
            res.append((token, loc))
    return res

def build_ast_from_file(filepath, content = ""):
    program = []
    assert Op.COUNT == 28, "Exhaustive handling of Ops"
    for (linenum, l) in enumerate(read_lines_from_file(filepath, content = content)):
        for (token, loc) in lex_line(l, linenum):
# TODO: change to use map
            maptoken = {
                "+":        Op.Plus,
                "-":        Op.Sub,
                "*":        Op.Mul,
                "/":        Op.Div,
                "^":        Op.Pow,
                "=":        Op.Eq,
                ">":        Op.Gt,
                "<":        Op.Lt,
                "!":        Op.Not,
                ".":        Op.Push,
                "dup":      Op.Dup,
                "drop":     Op.Drop,
                "over":     Op.Over,
                "swap":     Op.Swap,
                ".":        Op.Dump,
                "if":       Op.If,
                "else":     Op.Else,
                "end":      Op.End,
                "while":    Op.While,
                "do":       Op.Do,
                "whileend": Op.WhileEnd,
                "break":    Op.Break,
                "continue": Op.Continue,
                "idx":      Op.Index,
                "setidx":   Op.StoreAtIndex,
                "set":      Op.SetVar,
                "get":      Op.GetVar,
                "???":      Op.Debug,
            }
            try:
                program.append(Op(maptoken[token], [], loc))
            except KeyError:
                if all(map(lambda c: c.isnumeric() or c == ".", token)): # Push Int 
                    program.append(Op(Op.Push, [eval(token)], loc))
                elif token[0] == token[-1] == "\"" and len(token) >= 2: # Push Str
                    program.append(Op(Op.Push, [token[1:-1]], loc))
                else:
                    raise Exception(f"Malformed token `{token}` at {loc}")
    return program

repl_quit = iota(True)
repl_load = iota()
repl_toggle = iota()
repl_stack = iota()
repl_help = iota()
repl_last = iota()
repl_alias = iota()
repl_unalias = iota()
repl_show_aliases = iota()
repl_save_aliases = iota()
repl_load_aliases = iota()
repl_remove_src = iota()
repl_reload_src = iota()
repl_show_srcs = iota()
repl_clear_stack = iota()
repl_cmd_count = iota()

def display_aliases():
    ret = ""
    ret += "{\n"
    for kv in preprocessor_macros:
        ret += f"    {repr(kv)} : {repr(preprocessor_macros[kv])},\n"
    ret += "}"
    return ret

showstack = False
lastline = ""
line = ""
print("\x1b[2H\x1b[2J", end="")

with open("aliases.py", "r") as a:
    ct = a.read()
    preprocessor_macros = eval(ct)

source_files = {}

while (True):
    lastline = line
    line = input(f"S: {len(stack)} | A: {len(preprocessor_macros)} | C: {len(source_files)} > ")
    assert repl_cmd_count == 15, "Exhaustive handling of commands in repl"
    if line == "!quit":
        break
    elif line.startswith("!load ") or line == "!load":
        try:
            filename = line.removeprefix("!load")
            if filename != "":
                with open(filename[1:], "r") as f:
                    source_files.update({ filename[1:]: 1 })
                    text = f.read()
                    for i in text.splitlines():
                        print(f"! {i}")
                try:
                    program = build_ast_from_file(filename[1:])
                    program = configure_blocks(program)
                    stack = simulate_program(program)
                except Exception as e:
                    print(e) 
            else:
                print("!load <filename>")
                print("  - Loads code in <filename> and executes it as code.")
        except Exception as e:
            print(e) 
    elif line.startswith("!toggle ") or line == "!toggle":
        if line == "!toggle":
            print("options: showstack")
        else:
            option = line.removeprefix("!toggle ")
            if option == "showstack": 
                showstack = not showstack
                print(f"showstack: {showstack}")
            else:
                print(f"option `{option}` does not exist!")
    elif line == "!stack":
        for (idx, i) in enumerate(stack[::-1]):
            print(f"! {idx}: {repr(i)}")
    elif line == "!last":
        line = lastline
        try:
            program = build_ast_from_file("", content = line + " ")
            program = configure_blocks(program)
            stack = simulate_program(program)
        except Exception as e:
            print(e) 
    elif line.startswith("!alias ") or line == "!alias":
        if line == "!alias":
            print("!alias <token> <tokens>")
            print("  - Creates alias in preprocessor.")
        else:
            toks = line.removeprefix("!alias ") + " "
            idx = toks.find(" ")
            name = toks[:idx]
            rest = toks[idx + 1:]
            preprocessor_macros.update({ name: rest })
            print(f"! `{name}` -> `{rest}`")
    elif line.startswith("!unalias "):
        if line == "!unalias":
            print("!unalias <token>")
            print("  - Removes alias in preprocessor.")
        else:
            name = line.removeprefix("!unalias ")
            try:
                del preprocessor_macros[name]
                print(f"! `{name}` unbound")
            except:
                print(f"! `{name}` was not aliased ever!")
    elif line == "!aliases":
        print("+++++++++++++++++++++++++++")
        print(display_aliases())
        print("+++++++++++++++++++++++++++")
    elif line == "!savealiases":
        al = display_aliases()
        with open("aliases.py", "w") as a:
            a.write(al)
        print("+++++++++++++++++++++++++++")
        print(al)
        print("+++++++++++++++++++++++++++")
    elif line == "!loadaliases":
        with open("aliases.py", "r") as a:
            ct = a.read()
            preprocessor_macros = eval(ct)
        print("+++++++++++++++++++++++++++")
        print(display_aliases())
        print("+++++++++++++++++++++++++++")
    elif line.startswith("!unload") or line == "!unload":
        if line == "!unload":
            print("!unload <src>")
            print("  - Unloads src from memory")
        else:
            filename = line.removeprefix("!unload ")
            try:
                del source_files[filename]
                print(f"! `{filename}` unloaded")
            except:
                print(f"! `{filename}` was never loaded!")
    elif line == "!reloadsrc":
        for filename in source_files:
            try:
                program = build_ast_from_file(filename)
                program = configure_blocks(program)
                stack = simulate_program(program)
            except Exception as e:
                print(f"Error in `{filename}`:")
                print(e) 
    elif line == "!showsrc":
        print("+++++++++++++++++++++++++++")
        for fn in source_files:
            try:
                size = os.path.getsize(fn)
                print(f"! {fn} :: {size}B")
            except:
                print(f"! {fn} :: INVALID")
        print("+++++++++++++++++++++++++++")
    elif line == "!clearstack":
        stack = []
        print("cleared!")
    elif line.startswith("!help ") or line == "!help":
        print("This is a repl, type in any code in this forth and it will evaluate it.")
        print("Commands (these don't work in actual interpreted code, these are repl primitives):")
        print("- !stack")
        print("  - Prints current stack")
        print("- !toggle <option>")
        print("  - Toggles <option> (see more by running `!toggle`).")
        print("- !load <filepath>")
        print("  - Loads file in <filepath> and executes as code")
        print("- !quit")
        print("  - Exits this program.")
        print("- !last")
        print("  - Repeats last line in the repl, running it as code.")
        print("- !help")
        print("  - Helps with topic. If no topic is provided, prints this message.")
        print("- !alias <token> <tokens>")
        print("  - Creates alias in preprocessor.")
        print("- !unalias <token>")
        print("  - Removes alias in preprocessor.")
        print("- !aliases")
        print("  - Shows all aliases.")
        print("- !savealiases")
        print("  - Saves all aliases.")
        print("- !loadaliases")
        print("  - Loads aliases from `./aliases.py`.")
        print("- !unload <src>")
        print("  - Unloads src from memory.")
        print("- !reloadsrc")
        print("  - Reloads all source files.")
        print("- !showsrc")
        print("  - Shows all source files.")
        print("- !clearstack")
        print("  - Clears the stack")
    else:
        try:
            program = build_ast_from_file("", content = line + " ")
            program = configure_blocks(program)
            stack = simulate_program(program)
        except Exception as e:
            print(e) 
    if showstack:
        for (idx, i) in enumerate(stack[::-1]):
            print(f"! {idx}: {repr(i)}")


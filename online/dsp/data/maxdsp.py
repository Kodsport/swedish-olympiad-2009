#!/usr/bin/python3

# Maximal test cases for "dsp".
#
# The binding limit is the number of executed instructions, not N.
# The four modes stress the four different ways of hitting that limit:
#
#   steps   the full step budget spent on arithmetic, almost no I/O
#           -> pure simulation speed (a slow per-instruction dispatch dies here)
#   output  the full step budget spent on OUTPUT
#           -> a large answer file, kills unbuffered/flushing printing
#   input   the full step budget spent on INPUT
#           -> a large DSP input file, kills slow token reading
#   g1      no JNZ, so at most N instructions ever execute; instead this
#           maximises N and packs in register aliasing (ADD x x, SUB x x, ...)
#
# All programs are built together with a simulator so that the generator knows
# exactly how many instructions execute and how much DSP input is consumed.

import sys
import random

def cmdlinearg(name, default=None):
    for arg in sys.argv:
        if arg.startswith(name + "="):
            return arg.split("=")[1]
    if default is None:
        print("missing parameter", name)
        sys.exit(1)
    return default

MAX_N = 255
# The statement's budget of executed instructions. Overridable so the effect of
# tightening the guarantee can be measured without editing the generator.
MAX_STEPS = int(cmdlinearg("steps", 10**5))

# Registers reserved by the loop skeleton below.
R_ONE, R_INNER, R_OUTER = 0, 1, 2


def simulate(prog, data):
    """Run the program, returning (steps, values consumed). Crashes loudly on
    anything the statement forbids, so a mis-built program can't slip through."""
    reg = [0] * 256
    pc = steps = inptr = 0
    while prog[pc][0] != "HALT":
        steps += 1
        if steps > MAX_STEPS:
            raise AssertionError("program executes more than %d instructions" % MAX_STEPS)
        op = prog[pc]
        if op[0] == "CONST":
            reg[op[2]] = op[1]
        elif op[0] == "ADD":
            reg[op[2]] += reg[op[1]]
            assert reg[op[2]] <= 255, "ADD overflow at instruction %d" % pc
        elif op[0] == "SUB":
            reg[op[2]] -= reg[op[1]]
            assert reg[op[2]] >= 0, "SUB underflow at instruction %d" % pc
        elif op[0] == "JNZ":
            if reg[op[1]] != 0:
                pc = op[2]
                continue
        elif op[0] == "INPUT":
            assert inptr < len(data), "ran out of DSP input data"
            reg[op[1]] = data[inptr]
            inptr += 1
        pc += 1
        assert pc < len(prog), "ran past the last instruction without halting"
    return steps, inptr


def build_loop(pre, body, post, inner, outer):
    """Wrap `body` in a doubly nested counted loop.

    Register 0 holds 1, register 1 is the inner counter, register 2 the outer
    counter; `body` must leave those three alone. The program ends in HALT, and
    the loop back-edges make the last executed instruction a taken JNZ."""
    prog = [("CONST", 1, R_ONE)] + list(pre)
    prog.append(("CONST", outer, R_OUTER))
    outer_start = len(prog)
    prog.append(("CONST", inner, R_INNER))
    inner_start = len(prog)
    prog += body
    prog.append(("SUB", R_ONE, R_INNER))
    prog.append(("JNZ", R_INNER, inner_start))
    prog.append(("SUB", R_ONE, R_OUTER))
    prog.append(("JNZ", R_OUTER, outer_start))
    prog += list(post)
    prog.append(("HALT",))
    assert len(prog) <= MAX_N, "program has %d > %d instructions" % (len(prog), MAX_N)
    return prog


def pick_loop_counts(pre, body, post):
    """Largest (inner, outer) whose step count still fits in the step budget."""
    fixed = 1 + len(pre) + 1 + len(post)
    per_inner = len(body) + 2
    best = None
    for outer in range(1, 256):
        # fixed + outer * (1 + inner * per_inner + 2) <= MAX_STEPS
        inner = (MAX_STEPS - fixed - 3 * outer) // (outer * per_inner)
        inner = min(inner, 255)
        if inner < 1:
            continue
        steps = fixed + outer * (1 + inner * per_inner + 2)
        if best is None or steps > best[0]:
            best = (steps, inner, outer)
    assert best is not None
    return best[1], best[2]


def emit(prog, data):
    out = [str(len(prog))]
    for op in prog:
        out.append(" ".join(str(t) for t in op))
    out += [str(v) for v in data]
    sys.stdout.write("\n".join(out) + "\n")


# ---------------------------------------------------------------- mode: steps

def gen_steps(rnd):
    """A straight-line arithmetic body filling N, run as often as the budget allows.

    Every scratch register is re-initialised by a CONST at the top of the body,
    so the body is a pure function and is safe on every iteration. Two OUTPUTs
    per iteration (one of them the inner counter, so it varies) make the answer
    file witness that the arithmetic and the loop counting are both right."""
    scratch = list(range(200, 208))
    R_ECHO = 253

    reg = {r: 0 for r in scratch}
    body = [("CONST", rnd.randint(0, 255), r) for r in scratch]
    for r in scratch:
        reg[r] = body[scratch.index(r)][1]

    body.append(("INPUT", R_ECHO))
    body.append(("OUTPUT", R_ECHO))
    body.append(("OUTPUT", R_INNER))

    while len(body) < MAX_N - 8:
        choices = []
        for a in scratch:
            for b in scratch:
                if reg[a] + reg[b] <= 255:
                    choices.append(("ADD", a, b))
                if reg[b] - reg[a] >= 0:
                    choices.append(("SUB", a, b))
        choices.append(("CONST", rnd.randint(0, 255), rnd.choice(scratch)))
        op = rnd.choice(choices)
        if op[0] == "CONST":
            reg[op[2]] = op[1]
        elif op[0] == "ADD":
            reg[op[2]] += reg[op[1]]
        else:
            reg[op[2]] -= reg[op[1]]
        body.append(op)

    # An OUTPUT of a scratch register at the very end pins down the whole chain.
    body[-1] = ("OUTPUT", rnd.choice(scratch))

    inner, outer = pick_loop_counts([], body, [])
    prog = build_loop([], body, [], inner, outer)
    data = [rnd.randint(0, 255) for _ in range(inner * outer + 8)]
    return prog, data


# --------------------------------------------------------------- mode: output

def gen_output(rnd):
    """Spends ~99% of the step budget on OUTPUT.

    The eight source registers are loaded with three-digit values before the
    loop, so essentially every output line is four bytes wide."""
    srcs = list(range(240, 248))
    pre = [("CONST", rnd.randint(100, 255), r) for r in srcs]
    body = [("OUTPUT", srcs[i % len(srcs)]) for i in range(MAX_N - 8 - len(pre))]
    rnd.shuffle(body)
    inner, outer = pick_loop_counts(pre, body, [])
    prog = build_loop(pre, body, [], inner, outer)
    return prog, []


# ---------------------------------------------------------------- mode: input

def gen_input(rnd):
    """Spends ~97% of the step budget on INPUT, so the DSP input data is as
    large as the problem allows. Six OUTPUTs per iteration echo a just-read register,
    so the answer detects any loss of synchronisation with the input stream."""
    body = []
    last = 3
    for i in range(MAX_N - 8):
        if i % 40 == 39:
            body.append(("OUTPUT", last))
        else:
            last = 3 + (i % 200)
            body.append(("INPUT", last))
    inner, outer = pick_loop_counts([], body, [])
    prog = build_loop([], body, [], inner, outer)
    n_reads = sum(1 for op in body if op[0] == "INPUT") * inner * outer
    # A few unused values are left at the end; the statement only promises that
    # there is *enough* input data, not that it is exactly consumed.
    data = [rnd.randint(0, 255) for _ in range(n_reads + 7)]
    return prog, data


# ------------------------------------------------------------------- mode: g1

def gen_g1(rnd):
    """No JNZ, so execution is straight-line and N is the whole budget.

    Packs in the aliasing cases: ADD x x (doubling), SUB x x (self-clearing),
    OUTPUT of a register that was never written (must be 0), and a final HALT
    reached by falling through."""
    prog, data = [], []
    reg = [0] * 256
    used = list(range(1, 40))
    never_written = [200, 201, 202]

    while len(prog) < MAX_N - 1:
        choices = ["const", "add", "sub", "input", "output"]
        kind = rnd.choice(choices)
        if kind == "input":
            r = rnd.choice(used)
            v = rnd.randint(0, 255)
            prog.append(("INPUT", r))
            data.append(v)
            reg[r] = v
        elif kind == "output":
            r = rnd.choice(used + never_written)
            prog.append(("OUTPUT", r))
        elif kind == "const":
            r = rnd.choice(used)
            v = rnd.randint(0, 255)
            prog.append(("CONST", v, r))
            reg[r] = v
        elif kind == "add":
            a, b = rnd.choice(used), rnd.choice(used)
            if rnd.random() < 0.25:
                b = a  # doubling
            if reg[a] + reg[b] > 255:
                continue
            prog.append(("ADD", a, b))
            reg[b] += reg[a]
        else:
            a, b = rnd.choice(used), rnd.choice(used)
            if rnd.random() < 0.25:
                b = a  # self-clearing
            if reg[b] - reg[a] < 0:
                continue
            prog.append(("SUB", a, b))
            reg[b] -= reg[a]

    prog.append(("HALT",))
    data += [rnd.randint(0, 255) for _ in range(5)]
    return prog, data


MODES = {"steps": gen_steps, "output": gen_output, "input": gen_input, "g1": gen_g1}

rnd = random.Random(int(cmdlinearg("seed", sys.argv[-1])))
mode = cmdlinearg("mode")
assert mode in MODES, "unknown mode " + mode
prog, data = MODES[mode](rnd)
steps, consumed = simulate(prog, data)
assert consumed <= len(data)
print("%s: N=%d, %d steps, %d/%d input values consumed"
      % (mode, len(prog), steps, consumed, len(data)), file=sys.stderr)
emit(prog, data)

#!/usr/bin/python3

import sys
import random

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAXLEN = 20


def cmdlinearg(name, default=None):
    for arg in sys.argv:
        if arg.startswith(name + "="):
            return arg.split("=")[1]
    if default is None:
        print("missing parameter", name)
        sys.exit(1)
    return default


def game_win(words):
    """words: the >=2-letter dictionary words for one starting letter L.
    Returns True iff the player to move after 'L' has been said wins."""
    root = {}
    for w in words:
        t = root
        for ch in w:
            t = t.setdefault(ch, {})
    L = next(iter(words))[0]

    def win(node, prefix):
        for ch, sub in node.items():
            np = prefix + ch
            if np in words:
                continue  # saying ch completes a word: losing move
            if not win(sub, np):
                return True
        return False

    return win(root[L], L)


def gen_subtree(L, m, nsecond):
    """m random words starting with L, sharing nsecond distinct second letters."""
    sub = random.sample(ALPHA, random.randint(3, 7))
    pool = [L + s for s in random.sample(ALPHA, nsecond)]
    words = set()
    while len(words) < m:
        w = random.choice(pool)
        target = random.randint(len(w), MAXLEN)
        while len(w) < target:
            w += random.choice(sub)
            if random.random() < 0.3:
                pool.append(w)
        if len(w) >= 2:
            words.add(w)
    return words


def gen_with_value(L, m, want_win):
    """Subtree of m words for letter L whose game value for the player to
    move after 'L' is want_win."""
    for _ in range(300):
        nsecond = random.randint(2, 4) if want_win else random.randint(1, 3)
        words = gen_subtree(L, m, nsecond)
        if game_win(words) == want_win:
            return words
    if want_win:
        raise RuntimeError(f"could not reach a mover-wins subtree for {L}")
    # Fallback, guaranteed mover-loses: a single second letter s where L+s is
    # itself a word, so the mover is forced to complete it.
    words = gen_subtree(L, m, 1)
    forced = next(iter(words))[:2]
    if forced not in words:
        words.discard(max(words))
        words.add(forced)
    return words


random.seed(int(cmdlinearg('seed', sys.argv[-1])))
n = int(cmdlinearg('n'))
if n < 2000:
    raise RuntimeError("gen_letter_traps is meant for large cases")

letters = list(ALPHA)
random.shuffle(letters)
# traps: the 1-letter word makes L unsafe, but the subtree alone is an
# Anna-win -- solutions that ignore 1-letter words output L and die.
traps = letters[:6]
decoys = letters[6:10]   # 1-letter word, subtree already a Bosse-win
bare = letters[10]       # a 1-letter word with no longer words at all
safe = letters[11:15]    # no 1-letter word, Anna-win: the actual answer
plain = letters[15:]

one_letter = traps + decoys + [bare]
subtree_letters = [c for c in letters if c != bare]
counts = {c: (n - len(one_letter)) // len(subtree_letters) for c in subtree_letters}
for c in random.sample(subtree_letters, (n - len(one_letter)) % len(subtree_letters)):
    counts[c] += 1

words = set(one_letter)
for c in subtree_letters:
    want_win = c not in traps and c not in safe
    words |= gen_with_value(c, counts[c], want_win)

print(len(words))
print("\n".join(sorted(words)))

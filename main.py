from sys import argv
from typing import Self

equation = argv[1].replace(" ", "")


class Tree:
    left: float | Self | None
    right: float | Self | None
    op: str | None
    parent: Self | None

    def __init__(self):
        self.left = None
        self.right = None
        self.op = None
        self.parent = None

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"


parts = []
digit = ""
for i, chr in enumerate(equation):
    if chr in "+/*" or (chr == "-" and len(digit) > 0):
        parts.append(float(digit))
        digit = ""
        parts.append(chr)
    elif chr.isdigit():
        digit += chr
    elif chr == ".":
        if "." in digit:
            print("multiple dots in number")
            exit(1)
        digit += chr
    elif chr == "-":
        if i == 0:
            parts += chr
        elif equation[i - 1] not in "+-*/":
            parts += chr
        elif i == 1:
            print("there are 2 symbols following each other")
            exit(1)
        elif equation[i - 2] not in "+-*/":
            parts += chr
        else:
            print("there are 2 symbols following each other")
            exit(1)
    else:
        print("invalid character used in calulation")
        exit(1)
parts.append(float(digit))

for i, part in enumerate(parts):
    if i % 2 == 0:
        if not isinstance(part, float):
            print(f"position {i} should be a number")
            exit(1)
    else:
        if not isinstance(part, str):
            print(f"position {i} should be an operation")
            exit(1)


def presedence(op: str) -> int:
    return 0 if op in "+-" else 1


working = Tree()
for part in parts:
    if working.left is None:
        working.left = part
    elif working.op is None:
        working.op = part
    elif working.right is None:
        working.right = part
    elif presedence(part) > presedence(working.op):
        right = Tree()
        right.left = working.right
        right.op = part
        right.parent = working
        working.right = right
        working = right
    else:
        right = Tree()
        right.op = part
        # TODO: correct swaps; ugh pointer arihmetic
        while working.parent is not None and presedence(working.parent.op) > presedence(
            part
        ):
            working = working.parent
        working.parent = right
        right.left = working
        working = right


def depth_first(tree: Tree) -> float:
    left = depth_first(tree.left) if isinstance(tree.left, Tree) else tree.left
    right = depth_first(tree.right) if isinstance(tree.right, Tree) else tree.right
    match tree.op:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            return left / right


while working.parent is not None:
    working = working.parent

print(working)

print(depth_first(working))

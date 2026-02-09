import random
from itertools import cycle

quote: list[str] = [
    "CAD: Crying after drawing",
    "Constraints ruin my creativity",
    "That line? Just emotional support",
    "File corrupted like my soul",
    "Ctrl + z can't fix my life",
    "It fits... Kinda",
    "Sketch broke. So did I",
    "Click. Crash. Cry. Repeat.",
    "Origin? Never heard of her.",
    "Axis wrong. career gone",
    "Where is the undo button..."
]
bonus: list[str] = [
    "SolidWorks... More like SolidDoesntWorks",
    "I don't need sleep... I need answers",
    "Why? Why? Why? Oh, that's why...",
    "I clicked... And it vanished......",
    "Unexpected error, as expected",
    "One misclick, A new project",
    "Can I just draw by hand?",
    "I thought I saved it...",
    "It was fine five clicks ago"
]

cycleQuote = cycle(quote)
cycleBonus = cycle(bonus)

def randomQuote() -> tuple[str, int]:
    if random.randint(1,11) < 3:
        return (random.choice(bonus), 1)
    return (random.choice(quote), 0)

def nextQuote() -> tuple[str, int]:
    if random.randint(1,11) < 3:
        return (next(cycleBonus), 1)
    return (next(cycleQuote), 0)

def main() -> None:
    n: int = 0
    for _ in range(100):
        s, i = randomQuote()
        print(f"{s:_^30},{i}")
        n += i
    print(n)
    n = 0
    for _ in range(100):
        s, i = nextQuote()
        print(f"{s:_^30},{i}")
        n += i
    print(n)
    

if __name__ == "__main__":
    main()

with open("Selected Notes.txt") as f:
    note_collection_by_hiragana = {line.split()[0] : line.rstrip() for line in f}
with open("Kata.txt") as f:
    for line in f:
        entries = line.split()
        katakana = entries[0]
        hiragana = entries[1]
        note_collection_by_hiragana[hiragana] += "\t" + katakana
with open("output.txt", "w") as f:
    print(*note_collection_by_hiragana.values(), sep="\n", file=f)

from error import AppError

def readInputText():
    #read input.txt and extract title, description, and words
    f = open("./input.txt", 'r')
    lines = [line.strip() for line in f.readlines()]
    f.close()

    # if not enough lines, then raise error 
    if len(lines) <= 4:
        raise AppError("There should be at least TITLE, DESCRIPTION, and TWO WORDS")
    title, description, words = lines[0], lines[1], lines[2:]

    return (title, description, words)
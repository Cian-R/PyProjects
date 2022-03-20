import fnmatch
import string
from itertools import chain


def get_words():
    with open('allwords.txt', 'r') as f:
        words = f.read().splitlines()
    return words


def get_frequencies():
    with open('frequencies.txt', 'r') as f:
        freq = f.read().splitlines()
        freq = [freqitem.split(",") for freqitem in freq]
    return freq


def grabInputs():
    guessInput = input("\nGuessed word: ").upper().strip()
    if guessInput == "R":
        return "", ""
    while len(guessInput) != 5:
        print("Invalid.")
        guessInput = input("Guessed word: ").upper().strip()

    resultInput = input("Enter the result: ").upper().strip()
    while (resultInput.replace("X", "").replace("Y", "").replace("G", "") != "") or len(resultInput) != 5:
        print("Invalid.")
        resultInput = input("Enter the result: ").upper().strip()

    return guessInput, resultInput


FreqList = get_frequencies()
print("WARNING! Program break if you enter a word with 3 of the same letter (e.g. swiss, daddy, fluff).")
print("I cant be bothered to fix it right now. These words should still show up in the results.")
while True:

    possibleLetters = list(string.ascii_uppercase)
    WordList = [word.upper() for word in get_words()]
    WordList.sort()


    discovered = ["?", "?", "?", "?", "?"]
    exclusions = [[], [], [], [], []]
    flag = True

    while flag:
        guess, result = grabInputs()
        if guess == "":
            flag = False
            print("\n\n=============================NEW GAME=============================\n")

        holding = []

        if flag:
            for i in range(len(result)):

                if result[i] == "X":
                    if guess.count(guess[i]) == 1:  # If only one of the letter, remove the letter
                        if guess[i] in possibleLetters: possibleLetters.remove(guess[i])
                        WordList = [word for word in WordList if guess[i] not in word]
                    else:
                        for e in range(len(guess)):
                            if (guess[e] == guess[i]) and (e != i):
                                if result[e] == "X":  # If two letters, both grey, remove the letter
                                    if guess[e] in possibleLetters: possibleLetters.remove(guess[i])
                                    WordList = [word for word in WordList if guess[i] not in word]
                                else:  # If there's two of a letter, one grey and one not, filter for words with only
                                    # 1 of the letter
                                    WordList = [word for word in WordList if word.count(guess[i]) == 1]

                if result[i] == "G":
                    discovered[i] = guess[i]  # Add green letters to our 'discovered' array.

                if result[i] == "Y":
                    exclusions[i].append(guess[i])  # Add yellow letters to the 'exclusions' array.

            # ==========================================================================================================

            print("\nCalculating...")

            # Filter by green letters
            WordList = fnmatch.filter(WordList, "".join(discovered))

            # Filter by Exclusions (includes letter)
            if len("".join(list(chain.from_iterable(exclusions)))) != 0:
                for letter in list(chain.from_iterable(exclusions)):
                    WordList = fnmatch.filter(WordList, "*" + letter + "*")

            # Filter by exclusions (letter in yellow spot)
            for indexA in range(len(exclusions)):
                for indexB in range(len(exclusions[indexA])):
                    WordList = [word for word in WordList if word[indexA] != exclusions[indexA][indexB]]

            # print_data(possibleLetters, discovered, exclusions)
            print("\nAll possible words (not very useful):\n", WordList)

            # ==========================================================================================================

            # Run through all the words in the sorted frequency list, append to 'BestWords' if they show up in our
            # list of possible words. Display the first 5 found.
            BestWords = []
            index = 0
            while len(BestWords) < 5:
                if FreqList[index] == FreqList[-1]:
                    break
                if FreqList[index][0].upper() in WordList:
                    BestWords.append(FreqList[index][0])
                index += 1

            print("\nTop words by popularity (try these):\n", BestWords)

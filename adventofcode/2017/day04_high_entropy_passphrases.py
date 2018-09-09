"""
--- Day 4: High-Entropy Passphrases ---
A new system policy has been put in place
that requires all accounts to use a passphrase instead of simply a password.
A passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

aa bb cc dd ee is valid.
aa bb cc dd aa is not valid - the word aa appears more than once.
aa bb cc dd aaa is valid - aa and aaa count as different words.
The system's full passphrase list is available as your puzzle input.
How many passphrases are valid?
"""


def part01(fpath):
    is_valid = []
    with open(fpath, 'r') as f:
        for line  in f:
            tokens = line.strip().split()
            is_valid.append(len(tokens) == len(set(tokens)))

    print('- Part01 Answer:', sum(is_valid))


"""
--- Part Two ---
For added security, yet another system policy has been put in place.
Now, a valid passphrase must contain no two words that are anagrams of each other
- that is, a passphrase is invalid if any word's letters can be rearranged to form any other word in the passphrase.

For example:

abcde fghij is a valid passphrase.
abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
iiii oiii ooii oooi oooo is valid.
oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
Under this new system policy, how many passphrases are valid?
"""


def part02(fpath):
    num_valid = 0
    with open(fpath, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            uniques = {''.join(sorted(tok)) for tok in tokens}

            if len(tokens) == len(uniques):
                num_valid += 1

    print('- Part02 Answer:', num_valid)


if __name__ == '__main__':

    part01('./day04_part01_input.txt')  # 477
    part02('./day04_part01_input.txt')  # 167

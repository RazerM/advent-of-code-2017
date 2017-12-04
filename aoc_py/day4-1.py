def check_passphrase(phrase):
    words = phrase.split()
    return len(words) == len(set(words))


with open('../input/4.txt') as fp:
    lines = fp.readlines()

valid = sum(check_passphrase(line) for line in lines)
print(valid)

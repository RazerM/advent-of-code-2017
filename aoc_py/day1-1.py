with open('input/1.txt') as fp:
    data = [int(x) for x in fp.read().strip()]


def captcha(iterable):
    iterator = iter(iterable)
    sentinel = object()
    current = next(iterator, sentinel)

    # First digit is after the last, yield as ahead at the end
    first = current

    while current is not sentinel:
        ahead = next(iterator, sentinel)
        if ahead is sentinel:
            yield current, first
        else:
            yield current, ahead
        current = ahead


total = 0

for current, ahead in captcha(data):
    if current == ahead:
        total += current

print(total)

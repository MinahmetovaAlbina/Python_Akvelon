def find_most_frequency(func):
    def wrapper(*args):
        key = ''
        count = -1
        res = func(*args)
        for k, v in res.items():
            if v > count:
                count = v
                key = k
        print(key, count)
        return res
    return wrapper


@find_most_frequency
def frequency(string):
    counts = {}
    words = string.split(' ')
    for word in words:
        word = word.lower()
        counts.setdefault(word, 0)
        counts[word] += 1
    return counts


if __name__ == '__main__':
    lyrics = "We are no strangers to love You know the rules and so do I " \
        "A full commitment is what I am thinking of You would not get this from any other guy " \
        "I just wanna tell you how I am feeling Gotta make you understand " \
        "Never gonna give you up Never gonna let you down Never gonna run around and desert you " \
        "Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you " \
        "We have known each other for so long Your heart has been aching, but you are too shy to say it " \
        "Inside we both know what has been going on We know the game and we are gonna play it " \
        "And if you ask me how I'm feeling Do not tell me you are too blind to see " \
        "Never gonna give you up Never gonna let you down Never gonna run around and desert you " \
        "Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you " \
        "Never gonna give you up Never gonna let you down Never gonna run around and desert you " \
        "Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you " \
        "Ooh Give you up oh-ooh Give you up oh-ooh " \
        "Never gonna give never gonna give Give you up Ooh-ooh Never gonna give never gonna give Give you up " \
        "We have known each other for so long Your heart has been aching, but you are too shy to say it " \
        "Inside we both know what has been going on We know the game and we are gonna play it " \
        "I just wanna tell you how I am feeling Gotta make you understand " \
        "Never gonna give you up Never gonna let you down Never gonna run around and desert you " \
        "Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you " \
        "Never gonna give you up Never gonna let you down Never gonna run around and desert you " \
        "Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you " \
        "Never gonna give you up Never gonna let you down Never gonna run around and desert you " \
        "Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you"
    print(frequency(lyrics))


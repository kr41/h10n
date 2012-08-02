# helpers.py


def a(lang, country):
    if lang != 'en':
        raise ValueError('Unsupported language "{0}"'.format(lang))

    def helper_a(word):
        if word[0].lower() in ('a', 'o', 'i', 'e'):
            return 'an'
        return 'a'
    return helper_a

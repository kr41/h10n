""" The tests for Filter Compiler """

from nose import tools

from h10n._compiler import compile_filter


class Person(object):
    """ Test class -- Person """
    def __init__(self, first_name, last_name, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

def title(gender):
    """ Test filter function that returns person title according to gender """
    return {'male': 'Mr.', 'female': 'Ms.'}[gender]

def hello(**kw):
    """ Test filter function that returns salutation of person """
    return 'Hello, {title} {name}'.format(**kw)


def test():
    """ Filter Compiler """
    person = Person('John', 'Doe', 'male')
    kw = {'person': person}
    get_title = compile_filter(title, '{person}.gender', '{title}')
    say_hello = compile_filter(hello,
                {'name': '{person}.last_name', 'title': '{title}'},
                '{hello}')
    get_title(kw)
    tools.eq_(kw, {'person': person, 'title': 'Mr.'})
    say_hello(kw)
    tools.eq_(kw, {'person': person, 'title': 'Mr.', 'hello': 'Hello, Mr. Doe'})

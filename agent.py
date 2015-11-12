from __future__ import print_function
import types
import inspect
from functools import wraps


def coroutine(func):
    '''from dabeaz '''
    @wraps(func)
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


class self_aware(object):
    """Decorator class for coroutines with a self parameter."""
    # http://stackoverflow.com/questions/21808113/is-there-anything-similar-to-self-inside-a-python-generator
    def __new__(cls, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            o = object.__new__(cls)
            o.__init__(func, args, kwargs)
            return o
        return decorated

    def __init__(self, generator, args, kw):
        self.generator = generator(self, *args, **kw)
        next(self.generator)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.generator)

    next = __next__

    def send(self, value):
        return self.generator.send(value)


def self_aware(func):
    '''from dabeaz '''
    @wraps(func)
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        cr.send(cr)
        return cr
    return start


#def agent(self, name, boss):
@self_aware
def agent(name, boss):
    self = yield
    boss.send('agent %s reporting.  reply to %s' % (name, self))
    # TODO send self along with message.
    # and then verify that the boss can reply successfully.
    while True:
        job = (yield)
        boss.send('agent %s reporting on %s' % (name, job))


@coroutine
def boss(name):
    title = 'boss'
    underlings = []
    while True:
        thing = (yield)
        if type(thing) is types.GeneratorType:
            underlings.append(thing)
        if type(thing) is str:
            print(thing)


m = boss('m')
bond = agent('007', m)
moneypenny = agent('desk', m)
radley = agent('radley', m)

# TODO possible to do same with inspect or some other way, thus not defining a
# new class?
# TODO If not then might as well just switch over to a more explicitly OO
# version?    Not sure about it.   Because note:  the methods of self_aware are
# (almost) all overriding builtins.   So the class is simply implementing the
# generator/coroutine protocol.   Interesting.   Learn more.
# otoh it's a very lightweight object.
# otoh I **like** the way he does it right off. !!!!!!


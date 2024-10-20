# Source Generated with Decompyle++
# File: random.pyc (Python 3.8)

'''Random variable generators.

    bytes
    -----
           uniform bytes (values between 0 and 255)

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           pick weighted random sample
           generate random permutation

    distributions on the real line:
    ------------------------------
           uniform
           triangular
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence.
* The random() method is implemented in C, executes in a single Python step,
  and is, therefore, threadsafe.

'''
from warnings import warn as _warn
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from math import tau as TWOPI, floor as _floor
from os import urandom as _urandom
from _collections_abc import Set as _Set, Sequence as _Sequence
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect
import os as _os
import _random

try:
    from _sha512 import sha512 as _sha512
finally:
    pass
except ImportError:
    from hashlib import sha512 as _sha512


__all__ = [
    'Random',
    'SystemRandom',
    'betavariate',
    'choice',
    'choices',
    'expovariate',
    'gammavariate',
    'gauss',
    'getrandbits',
    'getstate',
    'lognormvariate',
    'normalvariate',
    'paretovariate',
    'randbytes',
    'randint',
    'random',
    'randrange',
    'sample',
    'seed',
    'setstate',
    'shuffle',
    'triangular',
    'uniform',
    'vonmisesvariate',
    'weibullvariate']
NV_MAGICCONST = 4 * _exp(-0.5) / _sqrt(2)
LOG4 = _log(4)
SG_MAGICCONST = 1 + _log(4.5)
BPF = 53
RECIP_BPF = 2 ** (-BPF)

class Random(_random.Random):
    """Random number generator base class used by bound module functions.

    Used to instantiate instances of Random to get generators that don't
    share state.

    Class Random can also be subclassed if you want to use a different basic
    generator of your own devising: in that case, override the following
    methods:  random(), seed(), getstate(), and setstate().
    Optionally, implement a getrandbits() method so that randrange()
    can cover arbitrarily large ranges.

    """
    VERSION = 3
    
    def __init__(self, x = ('flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}',)):
        '''Initialize an instance.

        Optional argument x controls seeding, as for Random.seed().
        '''
        self.seed(x)
        self.gauss_next = None

    
    def seed(self = None, a = None, version = None):
        '''Initialize internal state from a seed.

        The only supported seed types are None, int, float,
        str, bytes, and bytearray.

        None or no argument seeds from current time or from an operating
        system specific randomness source if available.

        If *a* is an int, all bits are used.

        For version 2 (the default), all of the bits are used if *a* is a str,
        bytes, or bytearray.  For version 1 (provided for reproducing random
        sequences from older versions of Python), the algorithm for str and
        bytes generates a narrower range of seeds.

        '''
        if version == 1 and isinstance(a, (str, bytes)):
            a = a.decode('latin-1') if isinstance(a, bytes) else a
            x = ord(a[0]) << 7 if a else 0
            for c in map(ord, a):
                x = (1000003 * x ^ c) & 0xFFFFFFFFFFFFFFFF
            x ^= len(a)
            a = -2 if x == -1 else x
        elif version == 2 and isinstance(a, (str, bytes, bytearray)):
            if isinstance(a, str):
                a = a.encode()
            a = int.from_bytes(a + _sha512(a).digest(), 'big')
        elif not isinstance(a, (type(None), int, float, str, bytes, bytearray)):
            _warn('Seeding based on hashing is deprecated\nsince Python 3.9 and will be removed in a subsequent version. The only \nsupported seed types are: None, int, float, str, bytes, and bytearray.', DeprecationWarning, 2)
        super().seed(a)
        self.gauss_next = None

    
    def getstate(self = None):
        '''Return internal state; can be passed to setstate() later.'''
        return (self.VERSION, super().getstate(), self.gauss_next)

    
    def setstate(self = None, state = None):
        '''Restore internal state from object returned by getstate().'''
        version = state[0]
        if version == 3:
            (version, internalstate, self.gauss_next) = state
            super().setstate(internalstate)
    # WARNING: Decompyle incomplete

    
    def __getstate__(self):
        return self.getstate()

    
    def __setstate__(self, state):
        self.setstate(state)

    
    def __reduce__(self):
        return (self.__class__, (), self.getstate())

    
    def __init_subclass__(cls, **kwargs):
        '''Control how subclasses generate random integers.

        The algorithm a subclass can use depends on the random() and/or
        getrandbits() implementation available to it and determines
        whether it can generate random integers from arbitrarily large
        ranges.
        '''
        for c in cls.__mro__:
            if '_randbelow' in c.__dict__:
                pass
            elif 'getrandbits' in c.__dict__:
                cls._randbelow = cls._randbelow_with_getrandbits
            elif 'random' in c.__dict__:
                cls._randbelow = cls._randbelow_without_getrandbits
            
            return None

    
    def _randbelow_with_getrandbits(self, n):
        '''Return a random int in the range [0,n).  Returns 0 if n==0.'''
        if not n:
            return 0
        getrandbits = None.getrandbits
        k = n.bit_length()
        r = getrandbits(k)
        if r >= n:
            r = getrandbits(k)
            continue
        return r

    
    def _randbelow_without_getrandbits(self, n, maxsize = (1 << BPF,)):
        '''Return a random int in the range [0,n).  Returns 0 if n==0.

        The implementation does not use getrandbits, but only random.
        '''
        random = self.random
        if n >= maxsize:
            _warn('Underlying random() generator does not supply \nenough bits to choose from a population range this large.\nTo remove the range limitation, add a getrandbits() method.')
            return _floor(random() * n)
        if None == 0:
            return 0
        rem = None % n
        limit = (maxsize - rem) / maxsize
        r = random()
        if r >= limit:
            r = random()
            continue
        return _floor(r * maxsize) % n

    _randbelow = _randbelow_with_getrandbits
    
    def randbytes(self, n):
        '''Generate n random bytes.'''
        return self.getrandbits(n * 8).to_bytes(n, 'little')

    
    def randrange(self, start, stop, step = (None, 1)):
        '''Choose a random item from range(start, stop[, step]).

        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.

        '''
        istart = int(start)
        if istart != start:
            raise ValueError('non-integer arg 1 for randrange()')
        if None is None:
            if istart > 0:
                return self._randbelow(istart)
            raise None('empty range for randrange()')
        istop = None(stop)
        if istop != stop:
            raise ValueError('non-integer stop for randrange()')
        width = None - istart
        if step == 1 and width > 0:
            return istart + self._randbelow(width)
        if None == 1:
            raise ValueError('empty range for randrange() (%d, %d, %d)' % (istart, istop, width))
        istep = None(step)
        if istep != step:
            raise ValueError('non-integer step for randrange()')
        if None > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError('zero step for randrange()')
        if None <= 0:
            raise ValueError('empty range for randrange()')
        return None + istep * self._randbelow(n)

    
    def randint(self, a, b):
        '''Return random integer in range [a, b], including both end points.'''
        return self.randrange(a, b + 1)

    
    def choice(self, seq):
        '''Choose a random element from a non-empty sequence.'''
        return seq[self._randbelow(len(seq))]

    
    def shuffle(self, x, random = (None,)):
        '''Shuffle list x in place, and return None.

        Optional argument random is a 0-argument function returning a
        random float in [0.0, 1.0); if it is the default None, the
        standard random.random will be used.

        '''
        if random is None:
            randbelow = self._randbelow
            for i in reversed(range(1, len(x))):
                j = randbelow(i + 1)
                x[i] = x[j]
                x[j] = x[i]
        else:
            _warn('The *random* parameter to shuffle() has been deprecated\nsince Python 3.9 and will be removed in a subsequent version.', DeprecationWarning, 2)
            floor = _floor
            for i in reversed(range(1, len(x))):
                j = floor(random() * (i + 1))
                x[i] = x[j]
                x[j] = x[i]

    
    def sample(self, population = None, k = {
        'counts': None }, *, counts):
        """Chooses k unique random elements from a population sequence or set.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        Repeated elements can be specified one at a time or with the optional
        counts parameter.  For example:

            sample(['red', 'blue'], counts=[4, 2], k=5)

        is equivalent to:

            sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)

        To choose a sample from a range of integers, use range() for the
        population argument.  This is especially fast and space efficient
        for sampling from a large population:

            sample(range(10000000), 60)

        """
        if isinstance(population, _Set):
            _warn('Sampling from a set deprecated\nsince Python 3.9 and will be removed in a subsequent version.', DeprecationWarning, 2)
            population = tuple(population)
        if not isinstance(population, _Sequence):
            raise TypeError('Population must be a sequence.  For dicts or sets, use sorted(d).')
        n = None(population)
        if counts is not None:
            cum_counts = list(_accumulate(counts))
            if len(cum_counts) != n:
                raise ValueError('The number of counts does not match the population')
            total = None.pop()
            if not isinstance(total, int):
                raise TypeError('Counts must be integers')
            if None <= 0:
                raise ValueError('Total of counts must be greater than zero')
            selections = None.sample(range(total), k, **('k',))
            bisect = _bisect
            return (lambda .0 = None: [ population[bisect(cum_counts, s)] for s in .0 ])(selections)
        randbelow = None._randbelow
        if not k <= k or k <= n:
            pass
        else:
            0
        raise ValueError('Sample larger than population or is negative')
        result = [
            None] * k
        setsize = 21
        if
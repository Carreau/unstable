"""
Unstable
========

Because sometime documenting a function is unstable is not
enough.

Because often, reaching to the documentation to know if something is stable
takes too much time.

Because once it's stable, you'll forget to re-check again.

Utility
=======

This module provides a decorator to mark function as `unstable`. Unstable
function will **raise** an ``UnstableWarning``unless used in an `unstable`
context. Thus preventing you from using an unstable function by mistake.

Provide an `with unstable()` context manger which silence (or log) the
exceptions raised by unstable functions. By default an `unstable` context
manager that does not detect any use of `unstable` functions will log a
`StableWarning`.

See Readme for more information.
"""

version_info = (0,5,0)
__version__ = '.'.join(map(str, version_info))

import warnings
from functools import wraps

__all__ = ('UnstableWarning', 'StableWarning', 'unstable')
    
class UnstableWarning(FutureWarning):
    pass

class StableWarning(Warning):
    pass

warnings.filterwarnings('error', category=UnstableWarning)

class Unstable(object):
    
    def __init__(self):
        self._params = []
        self._catch = []
        self._warns = []
        
    def __repr__(self):
        return '<unstable "decorator and context manager">'
    
    def __call__(self, maybe_function=None):
        if  callable(maybe_function):
            ### called as a context manager
            
            @wraps(maybe_function)
            def function(*args, **kwargs):
                self.here_be_dragons(maybe_function)
                return maybe_function(*args, **kwargs)
            return function
        else:
            if maybe_function:
                self._params.append(maybe_function)
            return self
    
    def here_be_dragons(self, what):
        warnings.warn('You are using an unstable feature (%r, %r), please wrap '
                      'with the appropriate `unstable` context manager.'% (what, what.__qualname__),
                      UnstableWarning, stacklevel=3)
            
    def __enter__(self):
        catcher = warnings.catch_warnings(record=True)
        self._catch.append(catcher)
        self._warns.append(catcher.__enter__())
        if self._params:
            p = self._params.pop()
        else:
            p = 'count'

            
        catcher.param = p
        if p == 'count':
            p = 'always'
            
        
        warnings.filterwarnings(p, category=UnstableWarning, append=False)


    
    def __exit__(self, a,b,c):
        catcher = self._catch.pop()
        warns = self._warns.pop()
        catcher.__exit__(a,b,c)
        if catcher.param not in ('ignore', 'count'):
            for w in warns:
                warnings.showwarning(w.message, w.category, w.filename, w.lineno, w.file, w.line)
        if catcher.param == 'count' and len(warns) == 0:
            warnings.warn("An unstable context manager has caught no use of "
                         "unstable features, these feature may stable now.", 
                         category=StableWarning, stacklevel=1)
            print('this seem tobe stable now', len(warns))
            



unstable = Unstable()


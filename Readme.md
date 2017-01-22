# Unstable

Because sometime documenting a function is unstable is not
enough.

Because often, reaching to the documentation to know if something is stable
takes too much time.

Because once it's stable, you'll forget to re-check again.

# Installation

    $ pip install unstable

# Utility

This module provides a decorator to mark function as `unstable`. Unstable
function will **raise** an ``UnstableWarning``unless used in an `unstable`
context. Thus preventing you from using an unstable function by mistake.

Provide an `with unstable()` context manger which silence (or log) the
exceptions raised by unstable functions. By default an `unstable` context
manager that does not detect any use of `unstable` functions will log a
`StableWarning`.

See Readme for more information.


# Usage

## Mark a function as unstable

```python
from unstable import unstable

@unstable
def frobulate(frumious, bandersnatch):
    galumphing(frumious) + bandersnatch

```


## Mark a branch as being unstable

```python
from unstable import unstable

def galumphing(frumious):
    if frumious:
        unstable.here_be_dragons(reason='frumious=True')
        # ...
    else:
        # ...
```

## Using unstable code

By default unstable code will raise an `UnstableWarning`, wrap unstable code in
an `unstable` context manager.

```python
from unstable import unstable

with unstable:
    fumious(True, 25) # Will Behave

frumious(False, 18) # will Fail with UnstableWarning

galumphing(False) # fine

with unstable:
    galumphing(True) # fine
```

# Context manager or decorator ?

Q : Is unstable a context manager or decorator ?
A : Both. It's magic.


# Advance usage:

I need to write the doc, PR welcome.


# Why ?

Inspired by Rust's `#[Unstable]`, which allows you to use it only explicitly
(and I'm not talking about safety here). This mimick it (as much as it can).

I want to be able to "ship" unstable code and N.x version of a library and tell
users "Use at your own risk", though no-one read the doc. Here it make things
obvious, don't use it unless you __meant__ to. Also the "instability" in
contagious as function using unstable functions will become (partially)
unstable. The instability boundary is obvious, it's the context manager.

## What about try/except ?

It will/can catch the exception, though the called function will not run.

# Todo

Add a plugin for sphinx which automatically mark the function in the doc as
unstable. 


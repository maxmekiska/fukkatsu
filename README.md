# fukkatsu 復活 [![Downloads](https://pepy.tech/badge/fukkatsu)](https://pepy.tech/project/fukkatsu) [![PyPi](https://img.shields.io/pypi/v/fukkatsu.svg?color=blue)](https://pypi.org/project/fukkatsu/) [![GitHub license](https://img.shields.io/github/license/maxmekiska/fukkatsu?color=black)](https://github.com/maxmekiska/fukkatsu/blob/main/LICENSE) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/fukkatsu.svg)](https://pypi.python.org/project/fukkatsu/)

<br>

| Build | Status|
|---|---|
| `MAIN BUILD`  |  ![master](https://github.com/maxmekiska/fukkatsu/actions/workflows/main.yml/badge.svg?branch=main) |
|  `DEV BUILD`   |  ![development](https://github.com/maxmekiska/fukkatsu/actions/workflows/main.yml/badge.svg?branch=development) |

<br>

<p align="center">
  <img src="assets/fukkatsu.png" alt="fukkatsu Logo" height="300">
</p>

```
pip install fukkatsu
```

## OpenAI API

fukkatsu requires the environmental variable `OPENAI_API_KEY` to be set with your OpenAI API key.

## Description

This is a proof of concept for a library that will leverage LLMs to dynamically fix and improve code during execution. Fukkatsu is the japanese word, `復活`, for "resurrection" or "revival". Metaphorically speaking, this library will attempt to fix your cars tire while you are driving it at 300 km/h. 

Insane? Yes. Possible? Maybe. Fun? Definitely.


Here is a representation of what I am trying to do: https://giphy.com/gifs/tire-kNRqJCLOe6ri8/fullscreen 


This concept currently only applies to interpreted languages such as Python and not to compiled languages such as C++. The very nature of interpreted languages allows us to dynamically change the code during runtime.


## MVP

<details>
  <summary>Expand</summary>
  <br>


You can find a MVP within the `poc` folder. You can simply run the code via `python mvp.py`. The code will simulate a failing function, which will be repaird during execution. The mvp.py code will not request a correction to an OpenAi LLM but simply ueses a mock corrected function.

### Foundation

#### Example:

- we have a function called `my_function` which takes accepts three arguments: 'x', 'y', 'z' and returns a value calculated via `x / y + z`
- lets assume the function `my_function` accidentally receives the value 0 for the argument 'y'
- this will cause the function to fail with a `ZeroDivisionError` becaue it was not accounted for in the original function
- fukkatsu offers a second chance here via the @mvp_reanimate decorator
- the decorator will catch the error and request a correction from an OpenAi LLM such as `gpt-3.5-turbo`.
- the corrected function will recieve the orignal arguments and handle the error as intended
- to get the most of the correction ability of fukkatsu, it will be paramount for the user to provide a good description of the function and its intended purpose via a well defined docstring
- fukkatsu makes sure that the LLM will receive all the necessary information to correct the function without changing its original purpose:
  - Full error traceback
  - original function code
  - passed arguments


```python
@mvp_reanimate
def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result

print(my_function(x = 1, y = 0, z= 2)) # would fail, but is corrected and returns 2
print(my_function(x = 2, y = 0, z= 10)) # would fail, but is corrected and returns 10
print(my_function(x = 9, y = 1, z= 2) + 10 )  # would not fail, returns 21.0
```

Please note, the example in the above is trivial however LLMs such as `gpt-3.5-turbo` are able to correct more complex functions. Once the library is more mature, more experiments and examples will show if such a use case for LLMs is worthwhile.


### Extra life

Here is again a representation of what I am trying to achieve: https://media.tenor.com/r5nBe8Ft6yEAAAAC/ready-player-one-extra-life.gif

The code mvp code offers now the concept of `extra lives`. The idea of extra lives is to allow the user to define, per function, how often a LLM should attempt to fix errors. This will allow LLMs to futher explore other paths of fixing the code at runtime however it will also make sure to bound the runtime of the LLM.

#### Example:

```python
@mvp_reanimate(lives=2)
def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result
```

The above example will allow the LLM to attempt to fix the function twice. If the LLM fails to fix the function after two attempts, a `flatline error` will be raised which indicates that the LLM was not able to fix the function during runtime.

</details>


## fukkatsu 0.0.1

<details>
  <summary>Expand</summary>
  <br>


fukkatsu 0.0.1 incorporates all the features demonstrated within the MVP section and introduces the concept of additional requests. Additional requests provide users with an alternative means of giving specific instructions to the LLM when a correction to a function is required. These additional requests act as a safeguard against potential misinterpretations by the LLM.


```python
@resurrect(lives=1, additional_req = "multiply any result by 1000")
def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result

print(my_function(x = 1, y = 0, z= 2))
print(my_function(x = 1, y = 0, z= 2)) # second function will trigger short term memory capabilities
```


```
ERROR:root:division by zero
Traceback (most recent call last):
  File "xxxxxxxxxxxxxxxxxxxxx", line 20, in wrapper
    result = func(*args, **kwargs)
  File "xxxxxxxxxxxxxxxxxxxxx", line 6, in my_function
    result = x / y + z
ZeroDivisionError: division by zero
WARNING:root:Input arguments: {'x': 1, 'y': 0, 'z': 2}
WARNING:root:
Source Code: 
 def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result

WARNING:root:Requesting INITIAL correction
WARNING:root:Received INITIAL suggestion: def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    if y == 0:
        return z + 1000
    else:
        result = x / y + z
        return result + 1000
WARNING:root:Attempt 1 to reanimate
WARNING:root:Reanimation successful, using def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    if y == 0:
        return z + 1000
    else:
        result = x / y + z
        return result + 1000
ERROR:root:division by zero
Traceback (most recent call last):
  File "xxxxxxxxxxxxxxxxxxxxxxx", line 20, in wrapper
    result = func(*args, **kwargs)
  File "xxxxxxxxxxxxxxxxxxxxxxx", line 6, in my_function
    result = x / y + z
ZeroDivisionError: division by zero
WARNING:root:Input arguments: {'x': 1, 'y': 0, 'z': 2}
WARNING:root:
Source Code: 
 def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result

WARNING:root:Correction already in memory
WARNING:root:Attempt 1 to reanimate
WARNING:root:Reanimation successful, using def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    if y == 0:
        return z + 1000
    else:
        result = x / y + z
        return result + 1000
```

```
1002
1002
```
</details>
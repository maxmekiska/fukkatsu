# fukkatsu

## Released

### 0.0.1

- proof of concept library
- implementation of `resurrect` decorator

### 0.0.2

- improved global and local variable handling within exec statements
- improved logging
- new short term memory functions: save memory to a json file, get current memory content, reset current memory content
- implementation of `mutate` decorator

### 0.0.3

- added `allow_installs` argument to `mutate` and `resurrect` decorator. Allows LLM to install non installed python libraries

### 0.0.4

- fixed a bug that caused input variables to be modified if a function performs in-place operations. I have added a deepcopy of the arguments
- changed the name of `extract_text_between_backticks` to `extract_text_between_pipes`
- added additional functions for response sanitation in LLM: `standardize_delimiters` and `add_delimiters`, which handle edge case answers from LLM

### 0.0.5

- added control arguments for OpenAi model and temperature
- added `twin` for review capabilities
- improved prompt clarity on code indicator tags `|||`

### 0.0.6

- short-term-memory fix
    - short-term-memory will now only save functions that executed successfully
- live counter fix
    - removed unintended extra live
- logging formatting enhanced + api call logging added

### 0.0.7

- fix of "Attempt `x` to reanimate" logging message


### 0.0.8

- new `stalk` decorator
- increased unittest coverage
- provided more examples in documentation
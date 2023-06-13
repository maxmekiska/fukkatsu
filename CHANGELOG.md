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
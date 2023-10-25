# fukkatsu [![PyPi](https://img.shields.io/pypi/v/fukkatsu.svg?color=blue)](https://pypi.org/project/fukkatsu/) [![GitHub license](https://img.shields.io/github/license/maxmekiska/fukkatsu?color=black)](https://github.com/maxmekiska/fukkatsu/blob/main/LICENSE) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/fukkatsu.svg)](https://pypi.python.org/project/fukkatsu/)

<br>

| Build | Status|
|---|---|
| `MAIN BUILD`  |  ![master](https://github.com/maxmekiska/fukkatsu/actions/workflows/main.yml/badge.svg?branch=main) |
|  `DEV BUILD`   |  ![development](https://github.com/maxmekiska/fukkatsu/actions/workflows/main.yml/badge.svg?branch=development) |

<br>


```
pip install fukkatsu
```

## OpenAI API

fukkatsu requires the environmental variable `OPENAI_API_KEY` to be set with your OpenAI API key.

## Description

This is a proof of concept for a library that will leverage LLMs to dynamically fix and improve code during execution. fukkatsu is the japanese word, `復活`, for "resurrection" or "revival". Metaphorically speaking, this library will attempt to fix your cars tire while you are driving it at 300 km/h. 


This concept currently only applies to interpreted languages such as python and not to compiled languages such as C++. The very nature of interpreted languages allows us to dynamically change the code during runtime.

Furthermore, fukkatsu introduces a method to enhance ordinary functions with the power of LLMs. By decorating ordinary functions with natural language prompts, they can now dynamically adapt to unforeseen inputs.

## Quick Start

```python
import pandas as pd
from datetime import datetime
from typing import List

from fukkatsu import resurrect

@resurrect(
    lives=3,
    allow_installs = True,
    additional_req = "Account for multiple date formats if necessary.",
    active_twin = True,
    primary_model_api = "openai",
    secondary_model_api = "openai",
    primary_config = {"model": "gpt-3.5-turbo", "temperature": 0.01},
    secondary_config = {"model": "gpt-3.5-turbo", "temperature": 0.10}
)
def perform_data_transformation(data:List):
    """takes in list of date strings and transforms them into datetime objects.
    """
    date_format = '%Y-%m-%d'
    
    for idx, date in enumerate(data):
        data[idx] = datetime.strptime(date, date_format)
        
    return data

if __name__ == "__main__":

  data = [
          "2023-07-07", "1 June 2020",
          "2023.07.07", "2023-12-01",
          "2020/01/01", "Nov 11 1994"
          ]
  
  transformed_data = perform_data_transformation(data)
  
  transformed_data
```

## fukkatsu 0.0.1 - `Extra Life`

<details>
  <summary>Expand</summary>
  <br>


fukkatsu 0.0.1 incorporates all the features demonstrated within the MVP section and introduces the concept of additional requests. Additional requests provide users with an alternative means of giving specific instructions to the LLM when a correction to a function is required. These additional requests act as a safeguard against potential misinterpretations by the LLM.


```python
@resurrect(lives=1, additional_req = "add to any result 1000")
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

## fukkatsu 0.0.2 - `The Ghost in the Machine`

<details>
  <summary>Expand</summary>
  <br>

The `mutate` decorator introduces a new way to enhance ordinary functions dynamically via the power of LLMs, enabling them to adapt to specific inputs. It provides users with the ability to extend the capabilities of functions through natural language prompts. Additionally, the decorator can be further extended using the `resurrect` decorator. The `mutate` decorator enables users to program and account for cases that are challenging or impossible to anticipate.

```python
@resurrect(lives=1)
@mutate(request= "Check the inputs closely. Given the inputs, make sure that the function is able to handle different formats if neccessary")
def my_mutated_function(file_path: str) -> pd.DataFrame():
    """
    function to read files and output a dataframes.
    """
    pd.read_csv(file_path)
    
my_mutated_function("test_file.xlsx")
```
</details>

## fukkatsu 0.0.3 - `Laissez-faire`

<details>
  <summary>Expand</summary>
  <br>

The `mutate` and `resurrect` decorators now support a new argument called allow_installs. By default, `allow_installs` is set to `False`. However, when set to `True`, the LLM will be able to test whether suggested or used python libraries are installed on the system. If any of the libraries are not installed, the LLM will install them before continuing code execution. This argument enables the LLM to have even more freedom. Therefore, setting the argument to True should be considered carefully.

### `resurrect`
```python
def resurrect(lives: int = 1, additional_req: str = "", allow_installs: bool = False):
  ...
```

### `mutate`
```python
def mutate(request: str = "", allow_installs: bool = False):
  ...
```
</details>


## fukkatsu 0.0.5 - `Not so Evil Twin`

<details>
  <summary>Expand</summary>
  <br>

The `mutate` and `resurrect` decorators now support new arguments `active_twin`, `llm`, and `temperature`. By default, `active_twin` is set to `False`, `llm` is set to `{"primary": "gpt-3.5-turbo", "secondary": "gpt-3.5-turbo"}`, and `temperature` is set to `{"primary": 0.1, "secondary": 0.1}`. This allows the user to configure the two decorators in a more granular way.

If `active_twin` is set to `True`, another LLM, the `TWIN`, will crosscheck the answer of the first LLM and make corrections if deemed necessary. This is highly experimental but might become very powerful as soon as more diverse LLMs become available.

### `resurrect`
```python
def resurrect(
    lives: int = 1,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    llm: dict = {"primary": "gpt-3.5-turbo", "secondary": "gpt-3.5-turbo"},
    temperature: dict = {"primary": 0.1, "secondary": 0.1},
):
  ...
```

### `mutate`
```python
def mutate(
    request: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    llm: dict = {"primary": "gpt-3.5-turbo", "secondary": "gpt-3.5-turbo"},
    temperature: dict = {"primary": 0.1, "secondary": 0.1},
):
  ...
```
</details>


## fukkatsu 0.0.8 - `I can see you`

<details>
  <summary>Expand</summary>
  <br>

This release features a new decorator called `stalk`. The `stalk` decorator enables you to quality-check your functions during runtime. Stalk will randomly execute when your target function is called. The primary objective is to check if your target functions are still working as intended during your program execution. If stalk deems your function as behaving illogically, stalk will perform modifications and enhancements similar to the `mutate` decorator. You can decide how frequent stalk will check a particular function by setting the likelihood parameter. By default, the likelihood parameter is set to 1. A value of 1 indicates that stalk will quality-check the function every time it is called. A value of 0.5 indicates that stalk will quality-check the function half of the time it is called.


### `stalk`
```python
def stalk(
    likelihood: float = 1,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    llm: dict = {"primary": "gpt-3.5-turbo", "secondary": "gpt-3.5-turbo"},
    temperature: dict = {"primary": 0.1, "secondary": 0.1},
):
  ...
```


</details>


## fukkatsu 0.0.10 - `Sharing is Caring`

<details>
  <summary>Expand</summary>
  <br>


This release includes new updates to the three decorators: `resurrect`, `mutate`, and `stalk`. Each decorator is now ready to support language model providers other than OpenAI in the future. To enable this, various changes have been made to the arguments. Please see below for the new arguments. By default, all models will be set to OpenAI. Support for new providers will be added as soon as they become available.


Configurating the `openai` model API via:

```python
@dataclass
class OpenaiChatCompletionConfig:
    model: str
    temperature: float
    max_tokens: int
    n: int
    stop: Optional[str]
```

The default values set for the `openai` model API:

```python
model: str = "gpt-3.5-turbo",
temperature: float = 0.1,
max_tokens: int = 1024,
n: int = 1,
stop: str = None,
```


### `resurrect`
```python
def resurrect(
    lives: int = 1,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
):
  ...
```

### `mutate`
```python
def mutate(
    request: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
):
  ...
```

### `stalk`
```python
def stalk(
    likelihood: float = 1.0,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
):
  ...
```

### Appendix: How to use fukkatsu in a python class?

fukkatsu wrappers can be used in python classes in the following way:

```python
from typing import List
import pandas as pd
from datetime import datetime

from fukkatsu import resurrect, mutate, stalk, reset_openai_key

@resurrect(
    lives=3,
    allow_installs = True,
    additional_req = "Account for multiple dateformats if necessary.",
    active_twin = True,
    primary_model_api = "openai",
    secondary_model_api = "openai",
    primary_config = {"model": "gpt-3.5-turbo", "temperature": 0.88},
    secondary_config = {"model": "gpt-3.5-turbo", "temperature": 0.33}
)
def perform_data_transformation(data:list):
    """takes in list of datestrings, transforms into datetime objects.
    """
    date_format = '%Y-%m-%d'
    
    for idx, date in enumerate(data):
        data[idx] = datetime.strptime(date, date_format)
        
    return data

data = ["2023-07-07", "1 June 2020", "2023.07.07", "2023-12-01", "2020/01/01", "Nov 11 1994"]



class TestClass:
    def __init__(self):
        self.test = "test"
        
    def test_wrapper_in_class(self, data: List):
        return perform_data_transformation(data)

test = TestClass()
test.test_wrapper_in_class(data)
```

</details>



## fukkatsu 0.0.11 - `The Humans are back`

<details>
  <summary>Expand</summary>
  <br>

Feature to get human-in-the-loop functionality. Once a successful correction was determind, the user will be asked to confirm the correction suggestion via a simple "y" or "n" command line input.


### `resurrect`
```python
def resurrect(
    lives: int = 1,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
    human_action: bool = False,
    active_memory: bool = True,    
):
  ...
```

### `mutate`
```python
def mutate(
    request: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
    human_action: bool = False,
):
  ...
```

### `stalk`
```python
def stalk(
    likelihood: float = 1.0,
    additional_req: str = "",
    allow_installs: bool = False,
    active_twin: bool = False,
    primary_model_api: str = "openai",
    secondary_model_api: str = "openai",
    primary_config: dict = {},
    secondary_config: dict = {},
    human_action: bool = False,
):
  ...
```



## Appendix

Added `active_memory` parameter to control the activation of the short term memory. Setting the `active_memory` parameter to `False` will prevent the `resurrect` decorator from remembering past solutions.

</details>


## Samples - `Synthetic` Code in Action

<details>
  <summary>Expand</summary>
  <br>

### `resurrect` - Twin not active


```python
file_path = "status_field.xlsx"

@resurrect(lives=3, additional_req = "make sure that the function returns a DataFrame", allow_installs = True, active_twin = False)
def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_csv(file_path)
    return df

read_file(file_path)
```

#### logs


<details>
  <summary>Show Full Logs</summary>
  <br>

```
2023-06-22 00:16:37,701 - 'utf-8' codec can't decode bytes in position 15-16: invalid continuation byte
Traceback (most recent call last):
  File "c:\users\max\documents\research\fukkatsu\fukkatsu\fukkatsu\__init__.py", line 34, in wrapper
    result = func(*args_copy, **kwargs_copy)
  File "C:\Users\Max\AppData\Local\Temp\ipykernel_9256\8051789.py", line 8, in read_file
    df = pd.read_csv(file_path)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 912, in read_csv
    return _read(filepath_or_buffer, kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 577, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1407, in __init__
    self._engine = self._make_engine(f, self.engine)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1679, in _make_engine
    return mapping[engine](f, **self.options)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\c_parser_wrapper.py", line 93, in __init__
    self._reader = parsers.TextReader(src, **kwds)
  File "pandas\_libs\parsers.pyx", line 548, in pandas._libs.parsers.TextReader.__cinit__
  File "pandas\_libs\parsers.pyx", line 637, in pandas._libs.parsers.TextReader._get_header
  File "pandas\_libs\parsers.pyx", line 848, in pandas._libs.parsers.TextReader._tokenize_rows
  File "pandas\_libs\parsers.pyx", line 859, in pandas._libs.parsers.TextReader._check_tokenize_status
  File "pandas\_libs\parsers.pyx", line 2017, in pandas._libs.parsers.raise_parser_error
UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 15-16: invalid continuation byte
2023-06-22 00:16:37,705 - Input arguments: {'file_path': 'status_field.xlsx'}

2023-06-22 00:16:37,705 - 
Source Code: 
 def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_csv(file_path)
    return df


2023-06-22 00:16:37,706 - Requesting INITIAL correction - Attempt 1

2023-06-22 00:16:37,707 - API REQUEST to gpt-3.5-turbo
2023-06-22 00:16:42,114 - Received INITIAL RAW suggestion:
|||
import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    df = pd.read_csv(file_path, encoding='utf-8')
    return df
|||

2023-06-22 00:16:42,114 - Received INITIAL CLEANED suggestion:
import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    """
    Read a CSV file and return a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    df = pd.read_csv(file_path, encoding='utf-8')
    return df

2023-06-22 00:16:42,114 - Import block added to suggested code:
 import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    import pandas as pd
    """
    Read a CSV file and return a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    df = pd.read_csv(file_path, encoding='utf-8')
    return df

2023-06-22 00:16:42,114 - Attempt 1 to reanimate

2023-06-22 00:16:42,120 - 'utf-8' codec can't decode bytes in position 0-1: invalid continuation byte
Traceback (most recent call last):
  File "c:\users\max\documents\research\fukkatsu\fukkatsu\fukkatsu\__init__.py", line 34, in wrapper
    result = func(*args_copy, **kwargs_copy)
  File "C:\Users\Max\AppData\Local\Temp\ipykernel_9256\8051789.py", line 8, in read_file
    df = pd.read_csv(file_path)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 912, in read_csv
    return _read(filepath_or_buffer, kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 577, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1407, in __init__
    self._engine = self._make_engine(f, self.engine)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1679, in _make_engine
    return mapping[engine](f, **self.options)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\c_parser_wrapper.py", line 93, in __init__
    self._reader = parsers.TextReader(src, **kwds)
  File "pandas\_libs\parsers.pyx", line 548, in pandas._libs.parsers.TextReader.__cinit__
  File "pandas\_libs\parsers.pyx", line 637, in pandas._libs.parsers.TextReader._get_header
  File "pandas\_libs\parsers.pyx", line 848, in pandas._libs.parsers.TextReader._tokenize_rows
  File "pandas\_libs\parsers.pyx", line 859, in pandas._libs.parsers.TextReader._check_tokenize_status
  File "pandas\_libs\parsers.pyx", line 2017, in pandas._libs.parsers.raise_parser_error
UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 15-16: invalid continuation byte

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\users\max\documents\research\fukkatsu\fukkatsu\fukkatsu\__init__.py", line 116, in wrapper
    output = new_function(*args_copy, **kwargs_copy)
  File "<string>", line 14, in read_file
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 912, in read_csv
    return _read(filepath_or_buffer, kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 577, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1407, in __init__
    self._engine = self._make_engine(f, self.engine)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1679, in _make_engine
    return mapping[engine](f, **self.options)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\c_parser_wrapper.py", line 93, in __init__
    self._reader = parsers.TextReader(src, **kwds)
  File "pandas\_libs\parsers.pyx", line 548, in pandas._libs.parsers.TextReader.__cinit__
  File "pandas\_libs\parsers.pyx", line 665, in pandas._libs.parsers.TextReader._get_header
UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 0-1: invalid continuation byte
2023-06-22 00:16:42,124 - Reanimation failed, requesting new correction

2023-06-22 00:16:42,124 - API REQUEST to gpt-3.5-turbo
2023-06-22 00:16:45,294 - Received attempt RAW suggestion:
|||
import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_excel(file_path)
    return df
|||

2023-06-22 00:16:45,294 - Received attempt CLEANED suggestion:
import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_excel(file_path)
    return df

2023-06-22 00:16:45,294 - Import block added to suggested code:
 import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    import pandas as pd
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_excel(file_path)
    return df

2023-06-22 00:16:45,294 - Attempt 2 to reanimate

2023-06-22 00:16:45,308 - Reanimation successful, using:
import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    import pandas as pd
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_excel(file_path)
    return df
```
</details>

#### Output

```
ID	Field	Cost	Country	Status
0	1	Eng	200000	Germany	active
1	1	Eng	200000	Italy	active
2	1	Eng	200000	UK	active
3	1	Eng	400500	US	active
4	1	Eng	100500	Italy	active
5	1	Eng	100500	Italy	deactivated
6	1	Eng	100500	Spain	active
```


### `resurrect` - Twin active

```python
file_path = "status_field.xlsx"

@resurrect(lives=3, additional_req = "make sure that the function returns a DataFrame", allow_installs = True, active_twin = True)
def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_csv(file_path)
    return df

read_file(file_path)
```

#### logs


<details>
<summary>Show Full Logs</summary>
<br>

```
2023-06-22 00:19:40,599 - 'utf-8' codec can't decode bytes in position 15-16: invalid continuation byte
Traceback (most recent call last):
  File "c:\users\max\documents\research\fukkatsu\fukkatsu\fukkatsu\__init__.py", line 34, in wrapper
    result = func(*args_copy, **kwargs_copy)
  File "C:\Users\Max\AppData\Local\Temp\ipykernel_9256\423974772.py", line 8, in read_file
    df = pd.read_csv(file_path)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 912, in read_csv
    return _read(filepath_or_buffer, kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 577, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1407, in __init__
    self._engine = self._make_engine(f, self.engine)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\readers.py", line 1679, in _make_engine
    return mapping[engine](f, **self.options)
  File "C:\Users\Max\anaconda3\lib\site-packages\pandas\io\parsers\c_parser_wrapper.py", line 93, in __init__
    self._reader = parsers.TextReader(src, **kwds)
  File "pandas\_libs\parsers.pyx", line 548, in pandas._libs.parsers.TextReader.__cinit__
  File "pandas\_libs\parsers.pyx", line 637, in pandas._libs.parsers.TextReader._get_header
  File "pandas\_libs\parsers.pyx", line 848, in pandas._libs.parsers.TextReader._tokenize_rows
  File "pandas\_libs\parsers.pyx", line 859, in pandas._libs.parsers.TextReader._check_tokenize_status
  File "pandas\_libs\parsers.pyx", line 2017, in pandas._libs.parsers.raise_parser_error
UnicodeDecodeError: 'utf-8' codec can't decode bytes in position 15-16: invalid continuation byte
2023-06-22 00:19:40,604 - Input arguments: {'file_path': 'status_field.xlsx'}

2023-06-22 00:19:40,605 - 
Source Code: 
 def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_csv(file_path)
    return df


2023-06-22 00:19:40,606 - Requesting INITIAL correction - Attempt 1

2023-06-22 00:19:40,607 - API REQUEST to gpt-3.5-turbo
2023-06-22 00:19:44,843 - Received INITIAL RAW suggestion:
|||
import pandas as pd

def read_file(file_path: str) -> pd.DataFrame:
    """Reads a CSV file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The pandas DataFrame containing the data from the CSV file.
    """
    df = pd.read_csv(file_path, encoding='utf-8')
    return df
|||

2023-06-22 00:19:44,843 - Requesting TWIN review

2023-06-22 00:19:44,843 - API REQUEST to gpt-3.5-turbo
2023-06-22 00:19:50,260 - TWIN review complete:
|||
import pandas as pd

def read_file(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    """
    Reads an Excel file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str, optional): The name of the sheet to read. Defaults to None.

    Returns:
        pd.DataFrame: The pandas DataFrame containing the data from the Excel file.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df
|||
2023-06-22 00:19:50,260 - Twin Safeguard: Function name changed to |||
import pandas as pd

def read_file(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    """
    Reads an Excel file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str, optional): The name of the sheet to read. Defaults to None.

    Returns:
        pd.DataFrame: The pandas DataFrame containing the data from the Excel file.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df
|||

2023-06-22 00:19:50,260 - Received INITIAL CLEANED suggestion:
import pandas as pd

def read_file(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    """
    Reads an Excel file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str, optional): The name of the sheet to read. Defaults to None.

    Returns:
        pd.DataFrame: The pandas DataFrame containing the data from the Excel file.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

2023-06-22 00:19:50,260 - Import block added to suggested code:
 import pandas as pd

def read_file(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    import pandas as pd
    """
    Reads an Excel file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str, optional): The name of the sheet to read. Defaults to None.

    Returns:
        pd.DataFrame: The pandas DataFrame containing the data from the Excel file.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

2023-06-22 00:19:50,260 - Attempt 1 to reanimate

2023-06-22 00:19:50,275 - Reanimation successful, using:
import pandas as pd

def read_file(file_path: str, sheet_name: str = None) -> pd.DataFrame:
    import pandas as pd
    """
    Reads an Excel file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str, optional): The name of the sheet to read. Defaults to None.

    Returns:
        pd.DataFrame: The pandas DataFrame containing the data from the Excel file.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df
```

</details>

#### Output

```
{'Sheet1':    ID Field    Cost  Country       Status
 0   1   Eng  200000  Germany       active
 1   1   Eng  200000    Italy       active
 2   1   Eng  200000      UK        active
 3   1   Eng  400500       US       active
 4   1   Eng  100500    Italy       active
 5   1   Eng  100500    Italy  deactivated
 6   1   Eng  100500    Spain       active}
```

### `mutate` - Twin not active


```python
file_path = "status_field.xlsx"

@mutate(request="look at the input file, make sure to change the function according to the file.")
def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_csv(file_path)
    return df

read_file(file_path)
```

#### logs


<details>
<summary>Show Full Logs</summary>
<br>


```
2023-06-22 00:30:25,589 - Input arguments: {'file_path': 'status_field.xlsx'}

2023-06-22 00:30:25,590 - 
Source Code: 
 def read_file(file_path: str):
    """read file and return a data frame"""
    df = pd.read_csv(file_path)
    return df


2023-06-22 00:30:25,592 - Requesting mutation

2023-06-22 00:30:25,592 - API REQUEST to gpt-3.5-turbo
2023-06-22 00:30:31,373 - Received RAW suggestion mutation:
||| 
import pandas as pd

def read_file(file_path: str):
    """
    Read file and return a data frame.
    
    Args:
    file_path (str): The path of the file to be read.
    
    Returns:
    pandas.DataFrame: The data frame containing the data from the file.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError('File format not supported. Please provide a CSV or Excel file.')
    return df
|||

2023-06-22 00:30:31,373 - Received CLEANED suggestion mutation: import pandas as pd

def read_file(file_path: str):
    """
    Read file and return a data frame.
    
    Args:
    file_path (str): The path of the file to be read.
    
    Returns:
    pandas.DataFrame: The data frame containing the data from the file.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError('File format not supported. Please provide a CSV or Excel file.')
    return df

2023-06-22 00:30:31,373 - Import block added to suggested code:
 import pandas as pd

def read_file(file_path: str):
    import pandas as pd
    """
    Read file and return a data frame.
    
    Args:
    file_path (str): The path of the file to be read.
    
    Returns:
    pandas.DataFrame: The data frame containing the data from the file.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError('File format not supported. Please provide a CSV or Excel file.')
    return df

2023-06-22 00:30:31,386 - Mutation successful, using import pandas as pd

def read_file(file_path: str):
    import pandas as pd
    """
    Read file and return a data frame.
    
    Args:
    file_path (str): The path of the file to be read.
    
    Returns:
    pandas.DataFrame: The data frame containing the data from the file.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError('File format not supported. Please provide a CSV or Excel file.')
    return df
```
</details>

#### Output

```
ID	Field	Cost	Country	Status
0	1	Eng	200000	Germany	active
1	1	Eng	200000	Italy	active
2	1	Eng	200000	UK	active
3	1	Eng	400500	US	active
4	1	Eng	100500	Italy	active
5	1	Eng	100500	Italy	deactivated
6	1	Eng	100500	Spain	active
```


### `stalk` - Twin not active

```python
@stalk(likelihood = 0.6, additional_req = "", allow_installs = False, active_twin = False, llm = {"primary": "gpt-3.5-turbo", "secondary": "gpt-3.5-turbo"}, temperature = {"primary": 0.1, "secondary": 0.1})
def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result

print(my_function(x = 1, y = 0, z= 2))
```

#### logs

<details>
<summary>Show Full Logs</summary>
<br>

```
2023-06-22 00:39:25,914 - Random number: 0.2695059864882857, Likelihood: 0.6
2023-06-22 00:39:25,916 - Input arguments: {'x': 1, 'y': 0, 'z': 2}

2023-06-22 00:39:25,918 - 
Source Code: 
 def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result


2023-06-22 00:39:25,919 - Stalking function

2023-06-22 00:39:25,920 - API REQUEST to gpt-3.5-turbo
2023-06-22 00:39:30,115 - Received RAW suggestion from Stalker:
|||
def my_function(x, y, z):
    """
    This function divides x by y and adds to the result z. If y is 0, it returns z.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    if y == 0:
        return z
    result = x / y + z
    return result
|||

2023-06-22 00:39:30,115 - Received CLEANED suggestion review: def my_function(x, y, z):
    """
    This function divides x by y and adds to the result z. If y is 0, it returns z.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    if y == 0:
        return z
    result = x / y + z
    return result

2023-06-22 00:39:30,115 - Import block added to suggested code:
 def my_function(x, y, z):

    """
    This function divides x by y and adds to the result z. If y is 0, it returns z.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    if y == 0:
        return z
    result = x / y + z
    return result

2023-06-22 00:39:30,115 - Review successful, using def my_function(x, y, z):

    """
    This function divides x by y and adds to the result z. If y is 0, it returns z.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    if y == 0:
        return z
    result = x / y + z
    return result
```

</details>

#### Output

```
2
```




</details>





## Testing and measuring fukkatsu's Capabilities

The following section delves into a series of simulations aimed at gaining a deeper understanding of fukkatsu's potential capabilities.

Please follow this [Link](https://github.com/maxmekiska/fukkatsu/blob/main/research/SIMULATIONS.md) for more information on fukkatsu's performance.


## Legacy MVP

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


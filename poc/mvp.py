import logging
import inspect
import traceback
import re

shortTermMemory = {}

suggested_code = """
def my_function(x, y, z):
    try:
        result = x / y + z
        return result
    except ZeroDivisionError:
        return None
"""

def remove_trace_lines(trace_error: str) -> str:
    pattern = r"\b\w*line\s\d+\w*\b"
    output_str = re.sub(pattern, "", trace_error)
    return output_str

def remove_wrapper_name(source_code: str) -> str:
    start_index = source_code.index("def")
    source_code = source_code[start_index:]
    return source_code



def request_correction() -> str:
    return suggested_code

def return_source_code(func: callable) -> str:
    source = (inspect.getsource(func))
    return source

def return_input_arguments(func: callable, *args, **kwargs) -> dict:
    signature = inspect.signature(func)
    bound_args = signature.bind(*args, **kwargs)
    input_args = {k: bound_args.arguments[k] for k in signature.parameters.keys()}
    return input_args


def function_logger(func):
    def wrapper(*args, **kwargs):


        try:
            result = func(*args, **kwargs)
            return result
        

        except Exception as e:
            logging.exception(e)
            trace = traceback.format_exc()
            trace = remove_trace_lines(trace) # pass to ChatGPT

            input_args = return_input_arguments(func, *args, **kwargs) # pass to ChatGPT
            source = return_source_code(func)
            source = remove_wrapper_name(source) # pass to ChatGPT

            logging.warning(f'Input arguments: {input_args}')
            logging.warning(f'\nSource Code: \n {source}')

            if trace in shortTermMemory.keys():
                logging.warning('Correction already in memory')
                suggested_code = shortTermMemory[trace]


            else:
                logging.warning('Requesting correction')
                suggested_code = request_correction()

            shortTermMemory[trace] = suggested_code

            logging.warning(f'Short term memory: \n Suggested code: {suggested_code} \n Traceback: {trace}')


            
            global_dict = globals().copy()
            local_dict = locals().copy()


            compiled_code = compile(suggested_code, '<string>', 'exec')


            exec(compiled_code, global_dict, local_dict)
            new_function = local_dict[func.__name__]




            return new_function(*args, **kwargs)
        

    return wrapper


if __name__ == "__main__":


    @function_logger
    def my_function(x, y, z):
        """function to add three variables."""
        result = x + y + z + o
        return result

    print(my_function(x = 1, y = 2, z= 2))
    print(my_function(x = 2, y = 8, z= 2))
    print(my_function(x = 9, y = 8, z= 2) + 10 )

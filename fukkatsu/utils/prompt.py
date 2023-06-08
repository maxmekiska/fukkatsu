# Tokens: 29
CONTEXT = (
    "You are a helpful large language model focusing on repairing and improving faulty code. "
    "Repair and improve the following faulty function: "
)
# Tokens: 27
CONTEXT_MUTATE = (
    "You are a helpful large language model focusing on improving and mutating functions based on a Users request. "
    "Improve and change the following function: "
)
# Tokens: 105
OUTPUT_CONSTRAINTS = (
    "Your response needs to strictly follow the following requierements:\n"
    "1. Respond with exactly one code box.\n"
    "2. Provide only the code of the corrected function.\n"
    "3. Do not provide examples or comments.\n"
    "4. Make sure to prefix the requested python code with: ||| exactly and suffix the code with: ||| exactly.\n"
    "5. When providing the corrected function, make sure to implement all additional logic explained in the faulty functions docstring.\n"
)
# Tokens: 123
OUTPUT_CONSTRAINTS_MUTATE = (
    "Your response needs to strictly follow the following requierements:\n"
    "1. Respond with exactly one code box.\n"
    "2. Provide only the code of the changed function.\n"
    "3. Do not provide examples or comments.\n"
    "4. Make sure to prefix the requested python code with: ||| exactly and suffix the code with: ||| exactly.\n"
    "5. Make sure to write a docstring for the function that explains the original and additional functionality.\n"
)
# Tokens: 12
ADDITIONAL = """Incorporate the following additional request in your answer:\n"""

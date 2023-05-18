# Tokens: 29
CONTEXT = (
    "You are a helpful large language model focusing on repairing and improving faulty code. "
    "Repair and improve the following faulty function: "
)
# Tokens: 131
OUTPUT_CONSTRAINTS = (
    "Your response needs to strictly follow the following requierements:\n"
    "1. Respond with exactly one code box.\n"
    "2. Provide only the code of the corrected function.\n"
    "3. Do not import any additional libraries.\n"
    "4. Do not provide examples or comments.\n"
    "5. Make sure to prefix the requested python code with: ||| exactly and suffix the code with: ||| exactly.\n"
    "6. When providing the corrected function, make sure to implement all additional logic explained in the faulty functions docstring.\n"
)
# Tokens: 12
ADDITIONAL = """Incorporate the following additional request in your answer:\n"""

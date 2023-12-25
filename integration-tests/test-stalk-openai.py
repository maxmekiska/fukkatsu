import fukkatsu
print(f"fukkatsu version running: {fukkatsu.__version__}")

from fukkatsu import stalk

@stalk(likelihood = 1.0,
       additional_req = "",
       allow_installs = False,
       active_twin = False,
       primary_model_api = "openai",
       primary_config = {"model": "gpt-3.5-turbo", "temperature": 0.1}, 
      )
def my_function(x, y, z):
    """
    function to divide x by y and add to the result z. Should return z if y is 0.
    """
    result = x / y + z
    return result

print(my_function(x = 1, y = 0, z= 2))
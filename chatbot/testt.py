import openai
from packaging import version

required_version = version.parse("1.1.1") # replace the version by the version you want
current_version = version.parse(openai.__version__)

if current_version < required_version:
    raise ValueError(f"Error: OpenAI version {openai.__version__}"
                     " is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

# -- Now we can get to it
from openai import OpenAI

print('OPENAI WAS GREAT AGAIN')
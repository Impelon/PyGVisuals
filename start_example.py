import os
import sys

"""
Script to execute example-files from outside the pygvisuals-package
"""


def has_main_loop(f):
    """
    Simple test to see if a py-file has a method called 'main_loop'
    """
    if not f.lower().endswith(".py"):
        return False

    try:
        descriptor = open(f)
    except:
        return False
    try:
        while True:
            try:
                line = descriptor.readline()
            except:
                line = None
            if not line:
                break
            if line.startswith("def main_loop():"):
                descriptor.close()
                return True
        descriptor.close()
        return False
    except:
        descriptor.close()
        return False

### Scan Directory ###

example_directories = [os.path.join(os.path.split(__file__)[0], "examples")]

print("Searching in: " + ", ".join(example_directories))

examples = []

for path in example_directories:
    for root, dirs, files in os.walk(path):
        for f in files:
            if has_main_loop(os.path.join(root, f)):
                examples.append(os.path.join(root, f))

print("List of executable examples:")
for e in range(len(examples)):
    print(str(e) + ":", examples[e])

### Handle User-Input ###

print("")
print("Choose an example to execute with its index! (type 'exit' to exit)")

index = None
while index == None:
    userinput = str(input("index: "))
    if userinput.lower() == "exit":
        sys.exit()
        break
    try:
        index = int(userinput)
        if index >= len(examples) or index < 0:
            print("Could not find example of index", index)
            index = None
    except:
        print("Invalid index!")
        index = None
print("Executing:", examples[index])

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(os.path.split(examples[index])[1], examples[index])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
except Exception as ex:
    __import__(examples[index].replace(os.sep, "."))

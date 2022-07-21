#%%
# Part A
# Find a list of all of the names in the following string using regex.
simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
Ruth and Peter, their parents, have 3 kids."""

import re
re.findall("[A-Z][a-z]*", simple_string)

# %%
# Part B
# students who received a B in the course.
with open('grades.txt','r') as file:
    grades = file.read()

    print(re.findall("[\w ]*:\ B", grades))

# %%
# Part C
'''
Your task is to convert this into a list of dictionaries, where each dictionary looks like the following:
example_dict = {"host":"146.204.224.152", 
                "user_name":"feest6811", 
                "time":"21/Jun/2019:15:45:24 -0700",
                "request":"POST /incentivize HTTP/1.1"}
'''
with open("logdata.txt", "r") as file:
    logdata = file.read()

pattern = """
    (?P<host>[\d]*.[\d]*.[\d]*.[\d]*)    
    (\ -\ )  
    (?P<user_name>[\w-]*) 
    (\ \[) 
    (?P<time>\w*/\w*/.*)
    (\]\ \") 
    (?P<request>.*)
    (")
    """
result = []
for item in re.finditer(pattern, logdata, re.VERBOSE):
    result.append(item.groupdict())

print(result)
# %%

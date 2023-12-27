import subprocess

# List of parameter pairs to run script.py with
parameters = [
    ('1','11'),
    ('2','22'),
    ('3','33'),
]

# Running script.py with different parameters
for param1, param2 in parameters:
    print(param1)
    subprocess.run(['python', 'script.py', param1, param2])

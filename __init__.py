from sys import path
from os import getcwd

# PATH hack.
cwd = getcwd()
if cwd not in path:
    path.append(cwd)

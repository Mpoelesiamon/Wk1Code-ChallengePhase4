import sys, os

if __name__ == "__main__":
    name = ''
    with open('bin/config') as config_file:
        name = config_file.read()

    if name: 
        os.system("cd code-challenge && git add . && git commit --allow-empty -m \"Final commit\"")
        os.system(f"cd code-challenge && git bundle create ../#{name}.bundle HEAD #{name}")

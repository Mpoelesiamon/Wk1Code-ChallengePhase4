import sys, os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("File must be run as `python bin/start your-name` (e.g., `python bin/start ada-lovelace`)")
        sys.exit(1)
    concat_name = "-".join(sys.argv[1:])

    with open('bin/config', 'w') as config_file:
        config_file.write(concat_name)


    os.system("git clone code-challenge.bundle")
    os.system(f"cd code-challenge && git checkout -b #{concat_name}")
    os.system("cd code-challenge && git commit --allow-empty -m \"Initial commit\"")
    print("Removing code-challenge.bundle")

    os.system("rm code-challenge.bundle")

import os
import sys
from multiprocessing import *
import subprocess
import shlex
import new_tools


class Bshl:
    def __init__(self, input_arg=None, output_argv=sys.__stdout__):
        self.stdin_param = input_arg
        self.stdout_param = output_argv
        self.environ = os.environ
        self.path = os.getcwd()
        self.commands = {
            "cd": self.change_dir,
            "environ": self.list_environ,
            "quit": self.quit,
            "var" : self.set
        }

    def change_dir(self, target=None):
        if target is None:
            print(self.path)
        else:
            try:
                os.chdir(target)
                self.path = os.getcwd()
                self.environ["PWD"] = self.path
                print(self.path)
            except FileNotFoundError:
                print("No such directory " + target)

    def list_environ(self):
        for k, v in self.environ.items():
            print(k, v)

    def quit(self):
        sys.exit(0)

    def set(self, pair):
        key_val = pair.split("=")
        self.environ[key_val[0]] = key_val[1]




if len(sys.argv[1:]):
    shellins = Bshl(sys.argv[1])
else:
    shellins = Bshl()

if shellins.stdin_param is None:
    while True:
        new_tools.runner(shellins, input("[" + shellins.path + "]" + " $ "))
else:
    with open(shellins.stdin_param, "r") as reader:
        for line in reader:
            shelltools.runner(shellins, line)

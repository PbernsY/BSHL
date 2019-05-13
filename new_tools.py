import sys
import os
import os.path
import shlex
import subprocess
redirection_flags = []
parseable = []
def set_redirect_flags(shellinstance, string):
	''' This is a function to set a list of flags. These flags are then used to perform tasks
	like background execution etc '''
	global redirection_flags
	global parseable
	# set up global variables so they can be passed to the other relevant parsing functions
	redirection_flags = []
	parseable = shlex.split(string)
	if not len(string):
		return	
	if ">>" in string or ">" in string:
		redirection_flags.append(parseable.pop())
		redirection_flags.append(parseable.pop())
	
	return redirection_flags, parseable

def program_invoc(list):
	''' i said this shell didnt use the force, but theres some unwordly action going on here ;)'''
	pid = os.fork()
	# if pid > 0 -> Parent process control
	# else -> Child process control
	if pid > 0:
		wpid = os.waitpid(pid, 0)

	else:
		try:
			# try to execute in the format below
			os.execvp(list[0], list)
		except:
			#catch an error if one is thrown
			print("Bshl: command not found " + list[0])
			#sys exit closes the fork that otherwise would be left opened by the error
			sys.exit()

	

def check_background_redirect(shellinstance, command):
	global redirection_flags
	if len(redirection_flags) == 2:
		location = redirection_flags[0]
		mode = redirection_flags[1]
		with open(location, checkwrite(mode)) as stdin:
			shellinstance.stdout_param = stdin
			subprocess.run(command, stdout = shellinstance.stdout_param)
	else:
		program_invoc(command)




def checkwrite(output_list):
	''' handy little function to determine the filemode'''
	return "a" if ">>" in output_list else "w"



def runner(shellinstance, string1):
	global redirection_flags
	global parseable
	string = os.path.expandvars(string1)
	set_redirect_flags(shellinstance, string)
	if parseable[0] not in shellinstance.commands:
		check_background_redirect(shellinstance, parseable)
	else:
		if parseable[0] == "cd" or parseable[0] == "var":
			shellinstance.commands[parseable[0]](*parseable[1:])
		else:
			shellinstance.commands[parseable[0]]()
	













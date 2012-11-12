#!/usr/bin/env python3

import os
import shutil
import subprocess

ADDON_SDK_DIR = "/home/phanect/bin/AddonSDK"
CURRENT_DIR = os.getcwd()
BUILD_DIR = "/tmp/ffts_build"
SHFILE = "/tmp/firefox_typescript_cfx.sh"

def main():
	if not os.path.exists(BUILD_DIR):
		os.makedirs(BUILD_DIR)
	
	if os.path.exists(os.path.join(ADDON_SDK_DIR, "bin/activate")) and os.path.exists(os.path.join(ADDON_SDK_DIR, "bin/cfx")): # if activate command exists
		os.listdir(CURRENT_DIR)
		
		scriptfiles = []
		for dirpath, dirnames, filenames in os.walk(CURRENT_DIR):
			for filename in filenames:
				srcpath		= os.path.join(dirpath, filename)				# CURRENT_DIR/prjname/src/file.ts
				srcdirpath_relative	= os.path.relpath(dirpath, CURRENT_DIR) # prjname/src/files.ts
				builddirpath	= os.path.join(BUILD_DIR, srcdirpath_relative)		# BUILD_DIR/prjname/src/files.ts
				
				if not os.path.exists(builddirpath):
					os.makedirs(builddirpath)
				
				if filename.endswith(".ts"):
					(root, ext) = os.path.splitext(filename)
					buildfilepath = os.path.join(builddirpath, root + ".js") # BUILD_DIR/prjname/src/files.js
					
					try:
						print(subprocess.check_call(["tsc", srcpath, "--out", builddirpath]))
					except subprocess.CalledProcessError:
						pass
				else:
					shutil.copy2(srcpath, builddirpath)
		
		cmd = "#!/bin/bash\n" \
			+ "cd " + ADDON_SDK_DIR + "\n" \
			+ "source ./bin/activate\n" \
			+ "cd " + BUILD_DIR + "\n" \
			+ "cfx run\ndeactivate\n"
		
		with open(SHFILE, "w+") as sh:
			sh.write(cmd)

		subprocess.check_call(["chmod", "u+x", SHFILE])
		print(subprocess.check_call([SHFILE]))
		
"""		
	else
		print("Addon SDK directory not found. Setup Addon SDK directory.")
		print("Addon SDK directory: ")
		
		import fileinput
		for line in fileinput.input():
			process(line)
		
		read ADDON_SDK_DIR
		main
"""
main()
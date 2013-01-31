#!/usr/bin/env python3

import os
import shutil
import subprocess

# NODE_PATH = ".:" + os.path.join(ADDON_SDK_DIR, "packages/addon-kit/lib") + ":" + os.path.join(ADDON_SDK_DIR, "packages/api-utils/lib/")
CURRENT_DIR = os.getcwd()
BUILD_DIR = ""

def main():
	parser = ArgumentParser(description="Build and/or install extension and run the browser.")
	parser.add_argument("--builddir", dest="builddir", default="./build", help="Just build and generate crx")
	args = parser.parse_args()
	
	if args.builddir:
		BUILD_DIR = args.builddir
	
	
	os.putenv("NODE_PATH", NODE_PATH)
	
	if not os.path.exists(BUILD_DIR):
		os.makedirs(BUILD_DIR)
	
	os.listdir(CURRENT_DIR)
		
	scriptfiles = []
	for dirpath, dirnames, filenames in os.walk(CURRENT_DIR):
		for filename in filenames:
			srcpath				= os.path.join(dirpath, filename)					# CURRENT_DIR/prjname/src/file.ts
			srcdirpath_relative	= os.path.relpath(dirpath, CURRENT_DIR)			# prjname/src/files.ts
			builddirpath			= os.path.join(BUILD_DIR, srcdirpath_relative)	# BUILD_DIR/prjname/src/files.ts
				
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
	
	os.unsetenv("NODE_PATH")

if __name__ == "__main__":
	main()

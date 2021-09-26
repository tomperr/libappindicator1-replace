# author: tomperr
# 26/09/2021

# ---------------------------------
# 	IMPORTS
# ---------------------------------

import os
import shutil
import sys

# ---------------------------------
# 	GLOBAL VARIABLES
# ---------------------------------

old_lib = "libappindicator1"
new_lib = "libayatana-appindicator1" 

cwd = os.getcwd()

tmp_root_str = "tmp_update_lib"
tmp_old_str = "old_package"
tmp_new_str = "new_package"

tmp_root = os.path.join(cwd, tmp_root_str)
tmp_old = os.path.join(tmp_root, tmp_old_str)
tmp_new = os.path.join(tmp_root, tmp_new_str)

tmp_old_debian_str = "DEBIAN"
tmp_old_debian = os.path.join(tmp_old, tmp_old_debian_str)

control_path_str = "control"
control_path = os.path.join(tmp_old_debian, control_path_str)

# ---------------------------------
# 	FUNCTIONS
# ---------------------------------

def create_structure():
	"""Create directories for depackaging and packaging"""
	os.mkdir(tmp_root)
	os.mkdir(tmp_old)
	os.mkdir(tmp_new)
	os.mkdir(tmp_old_debian)

def delete_structure():
	"""Delete directories and files used to build new package"""
	if os.path.exists(tmp_root):
		shutil.rmtree(tmp_root)

def get_deb_filepath():
	"""Get deb package filename from cmd argument"""
	argc = len(sys.argv)
	if argc == 2:
		deb_filename = sys.argv[1]
		deb_filepath = os.path.join(cwd, deb_filename)
		if os.path.exists(deb_filepath):
			return (deb_filename, deb_filepath)
		else:
			print("ERROR: {} does not exist.".format(deb_filename))
			return -1

	else:
		print("ERROR: Wrong arguments")
		return -1

def unpack_deb(filepath, old, old_debian):
	"""Unpackage deb file"""
	os.system("dpkg-deb -x {} {}".format(filepath, old))
	os.system("dpkg-deb -e {} {}".format(filepath, old_debian))

def replace_lib():
	"""Replace old lib by the new one in control file"""
	control_content = None

	with open(control_path) as f:
		control_content = f.read()
	
	with open(control_path, 'w') as f:
		control_content = control_content.replace(old_lib, new_lib)
		f.write(control_content)

def repack_deb():
	"""Rebuild new package from modified sources"""
	os.system("dpkg-deb -Z xz -b {} {}".format(tmp_old, tmp_new))

def move_new_deb(filename):
	"""Move new package to cwd"""
	package_filepath_str = os.listdir(tmp_new)[0]
	package_filepath = os.path.join(tmp_new, package_filepath_str)
	new_location = os.path.join(cwd, "modified_"+filename)	
	shutil.move(package_filepath, new_location)
	return new_location
	
def add_execution_permissions(path):
	"""Add excecution permission on modified package"""
	os.system("chmod +x {}".format(path))

def main():
	"""Main function"""

	# delete structure if already exists
	delete_structure()
	
	# get path of package
	deb_filename, deb_filepath = get_deb_filepath()

	# create temporary structure
	create_structure()

	# process
	unpack_deb(deb_filepath, tmp_old, tmp_old_debian)
	replace_lib()
	repack_deb()
	new_path = move_new_deb(deb_filename)
	add_execution_permissions(new_path)

	# delete temporary structure 
	delete_structure()

# ---------------------------------
# 	EXECUTION
# ---------------------------------

if __name__ == '__main__':
	main()

"""
<Program>
  package_installers.py

<Date Started>
  March 22, 2015

<Author>
  Xuefeng Huang

<Purpose>

  This is a library used by the other packaging components. It provides
  various functions to package the installation files for different platforms
  we supported. It helps new packaging script that generates Seattle
  installers for different platforms using the new build harness.

"""

import os
import sys
import shutil
import tarfile
import zipfile
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../DEPENDENCIES/common/"))
import build_component



def copyfiles(base_installer_dir):
  """
  <Purpose>
    Take from the current working directory
      * the general non-installer-specific files ("seattle_repy", needed 
        for all installers) and 
      * all of the platform-specific installation/start/stop scripts 
        ("seattle_linux", "seattle_mac" etc.) for each platforms we support,
    and copy the directory trees of those into the base installer directory.
    Further packaging will continure from the base_installer_dir.
    
  <Arguments>
    base_installer_dir: 
      The directory to put the base installers in

  <Exceptions>
    None
    
  <Side Effects>
    None

  <Returns>
    None
  """  

  component_dirs = ['seattle_mac', 'seattle_linux', 'seattle_android', 
      'seattle_win', 'seattle_repy']

  for component_dir in component_dirs:
   build_component.copy_tree_to_target(component_dir, 
       base_installer_dir + os.sep + component_dir)



def unzip_file():
  """
  <Purpose>
     Unzip partial_win.zip 
    
  <Arguments>
    None

  <Exceptions>
    None
    
  <Side Effects>
    None

  <Returns>
    None
  """
  if os.path.isfile('seattle_win' + os.sep + 'seattle_repy'+os.sep +'partial_win.zip'): 
    fh = open('seattle_win' + os.sep + 'seattle_repy'+os.sep +'partial_win.zip', 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
      outpath = 'seattle_win' + os.sep + 'seattle_repy'
      z.extract(name, outpath)
    fh.close()
    build_component.copy_tree_to_target('seattle_win' + os.sep + 'seattle_repy'+os.sep +'seattle'+os.sep+'seattle_repy','seattle_win' + os.sep + 'seattle_repy')
    shutil.rmtree('seattle_win' + os.sep + 'seattle_repy'+os.sep+'seattle') 
    os.remove('seattle_win' + os.sep + 'seattle_repy'+os.sep+'partial_win.zip')
  else:
    pass


def make_tarfile(output_filename, source_dir):
  """
  <Purpose>
    Inserts the files in the source directory into the specified tarball.
    
  <Arguments>
    output_filename: 
      the name of outfile
    source_dir : 
      source file directory

  <Exceptions>
    None
    
  <Side Effects>
    None

  <Returns>
    None
  """

  tar = tarfile.open(output_filename, "w:gz")
  tar.add(source_dir, arcname=os.path.basename(source_dir))
  shutil.rmtree(source_dir)

def make_zipfile(output_filename, source_dir):
  """
  <Purpose>
    Inserts the files in the source directory into the specified zipfile.
    
  <Arguments>
    output_filename: 
      the name of outfile
    source_dir : 
      source file directory

  <Exceptions>
    None
    
  <Side Effects>
    None

  <Returns>
    None
  """

  zipf = zipfile.ZipFile(output_filename, 'w')

  for root, dirs, files in os.walk(os.path.basename(source_dir)):
     for file in files:
         zipf.write(os.path.join(root, file))

  shutil.rmtree(source_dir)

def package_win(base_installer_directory,version):
  """
  <Purpose>
    Packages the installation files for Windows into a zipfile
    and adds the specific installation scripts for this OS.

  <Arguments>
    base_installer_directory: 
      The directory to put the base installers in
    version: 
      your project/clearinghouse/Custom Installer Builder name

  <Exceptions>
    None

  <Side Effects>
    None

  <Returns>
    None.  
   """

  installer_files = ['seattle_win']
  
  for files in installer_files:
     build_component.copy_tree_to_target(base_installer_directory + os.sep + 'seattle_repy',base_installer_directory + os.sep + files + os.sep + 'seattle_repy')
  
  os.chdir(base_installer_directory)
  make_zipfile('seattle_'+ version +'_win.zip',base_installer_directory +os.sep+'seattle_win')

def package_linux_or_mac(base_installer_directory,version):
  """
  <Purpose>
    Packages the installation files for Linux or Mac into a tarball
    and adds the specific installation scripts for this OS.

  <Arguments>
    base_installer_directory: 
      The directory to put the base installers in
    version: 
      your project/clearinghouse/Custom Installer Builder name

  <Exceptions>
    None

  <Side Effects>
    None

  <Returns>
    None.  
   """

  installer_files = ['seattle_linux','seattle_mac']

  for files in installer_files:
    build_component.copy_tree_to_target(base_installer_directory + os.sep + 'seattle_repy',base_installer_directory + os.sep + files + os.sep + 'seattle_repy')
    if 'pyreadline' in os.listdir(base_installer_directory + os.sep + files + os.sep + 'seattle_repy'):
      shutil.rmtree(base_installer_directory + os.sep + files + os.sep + 'seattle_repy'+ os.sep + 'pyreadline')
  
  os.chdir(base_installer_directory)
  make_tarfile('seattle_'+ version +'_mac.tgz',base_installer_directory +os.sep+'seattle_mac')
  make_tarfile('seattle_'+ version +'_linux.tgz',base_installer_directory +os.sep+'seattle_linux')

def package_android(base_installer_directory,version):
  """
  <Purpose>
    Packages the installation files for Android into a zipfile
    and adds the specific installation scripts for this OS.

  <Arguments>
    base_installer_directory: 
      The directory to put the base installers in
    version: 
      your project/clearinghouse/Custom Installer Builder name

  <Exceptions>
    None

  <Side Effects>
    None

  <Returns>
    None.  
  """

  build_component.copy_tree_to_target(base_installer_directory + os.sep + 'seattle_repy',base_installer_directory + os.sep + 'seattle_android' + os.sep + 'seattle_repy')

  if 'pyreadline' in os.listdir(base_installer_directory + os.sep + 'seattle_android' + os.sep + 'seattle_repy'):
    shutil.rmtree(base_installer_directory + os.sep + 'seattle_android' + os.sep + 'seattle_repy'+ os.sep + 'pyreadline')
  
  os.chdir(base_installer_directory)
  make_zipfile('seattle_'+ version +'_android.zip',base_installer_directory +os.sep+'seattle_android')

def write_metainfo(base_installer_directory,privkey,pubkey):
  """
  <Purpose>
    Writes the metainfo files used by the software updater.

  <Arguments>
    base_installer_directory: 
      The directory to put the base installers in
    privkey: 
      The path to a private key that will be used to generate the metainfo file.
    pubkey:
      The path to a public key that will be used to generate the metainfo file.
    
  <Exceptions>
    IOError on bad file paths.

  <Side Effects>
    None

  <Returns>
    None.  
  """

  os.chdir(base_installer_directory)
  # Generate the metainfo file.
  try:
    p = subprocess.Popen([sys.executable, "writemetainfo.py", privkey, pubkey, "-n"])
  except:
    print "Failed to generate the metainfo file."
    sys.exit(1)

  p.wait()

def prepare_gen_files(updatesite_dir,privkey,pubkey):
  """
  <Purpose>
    Prepare the general non-installer-specific files (needed for all installers)
    and deposit them into the temporary folder designated to hold the files
    that will be present in the base installer(s), including the metainfo file.

  <Arguments>
    updatesite_dir: 
      The directory to put the generated update files in
    privkey: 
      The path to a private key that will be used to generate the metainfo file.
    pubkey:
      The path to a public key that will be used to generate the metainfo file.

  <Exceptions>
    None

  <Side Effects>
    None

  <Returns>
    None
  """

  build_component.copy_tree_to_target('seattle_repy',updatesite_dir)
  write_metainfo(updatesite_dir,privkey,pubkey)
  

def package_installers(base_installer_directory,version,privkey,pubkey):
  """
  <Purpose>
    Build the installers for one or more of the supported operating systems

  <Arguments>
    base_installer_directory: 
      The directory to put the base installers in
    version:
      your project/clearinghouse/Custom Installer Builder name
    pubkey:
      The path to a public key that will be used to generate the metainfo file.
    privkey: 
      The path to a private key that will be used to generate the metainfo file.

  <Exceptions>
    None    

  <Side Effects>
    None

  <Returns>
    None  
  """
  unzip_file()
  copyfiles(base_installer_directory)
  write_metainfo(base_installer_directory + os.sep + 'seattle_repy',privkey,pubkey)

  package_win(base_installer_directory,version)
  package_linux_or_mac(base_installer_directory,version)
  package_android(base_installer_directory,version)

  shutil.rmtree(base_installer_directory + os.sep + 'seattle_repy')

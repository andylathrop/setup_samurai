#!/usr/bin/env python3

# A Linux/OSX environment setup script

import os
import time
import sys
import shutil 
import logging
import argparse

global installer_command # This is the package manager (e.g. brew, dnf, yum, apt, etc...)
global installer_command_install # Package manager's 'install' command
global installer_command_update # Package manager's self-update command

global args # command line arguments

def common_install(prog_name): # Install software using your regular package manager

    command = installer_command + ' ' + installer_command_install + ' ' + prog_name
    
    # If you're running this on a fresh installation, the odds are you just want everything; especially if you're using brew on OS X to get up-to-date software. 

    if args.check_before_install:
        logging.info('Checking for %s' % prog_name)
        if shutil.which(prog_name) is not None:
            logging.info('%s is already installed, skipping' % prog_name)
            return()
        else:
            logging.info('%s not found, installing [%s]' % (prog_name, command))

    # the main event
    ret = os.system(command)
        
    if ret==0:
        logging.info('%s successfully installed!' % prog_name)
    else:
        logging.warning('%s installation failed!' % prog_name)

def install_homebrew(): # Install the latest homebrew from the web
   
    # we need to set these
    global installer_command
    global installer_command_install
    global installer_command_update
    
    # Set our globals... so crass
    logging.debug('setting installer command globals')
    installer_command = "brew"
    installer_command_install = "install"
    installer_command_update = "update"
 
    logging.info('Checking for homebrew installation')
    installer_command_path = shutil.which("brew")

    if installer_command_path is not None:
        logging.info('Homebrew is already installed! [%s]' % installer_command_path)
        return()
    else:
        logging.info('Could not locate homebrew installation, installing now...')

    ret = os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')

    # check if everything went okay
    if ret==0:
        logging.info('Homebrew installed successfully!')
    else:
        logging.error('Homebrew installation failed, exiting...!')
        sys.exit()
    
# Set up logging facilities
logfile_name = "_setup_samurai.log"

# Init logging mechanism and create new logfile using 'logfilename'

logging.basicConfig(filename=logfile_name, 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

# Parse command line args

prog_name = (sys.argv[0]).split("/")[-1]

arg_parser = argparse.ArgumentParser(prog=prog_name, description='A script to set up your Linux/OSX environment.')

arg_parser.add_argument('-q', '--quiet', action='store_true', help='don\'t print info messages to stdout')

arg_parser.add_argument('-c', '--check-before-install', action='store_true',help='check if programs are already installed')
args = arg_parser.parse_args()

if not args.quiet:
    console_lh = logging.StreamHandler()
    console_lh.setLevel(logging.INFO)
    formatter = logging.Formatter('[*] %(message)s')
    console_lh.setFormatter(formatter)
    logging.getLogger('').addHandler(console_lh)
    print('')

# Check OS and version 
logging.info('Getting OS version')
if sys.platform == "darwin":
    logging.info('Mac OS X (darwin) detected!')
    install_homebrew()
    
else:
    logging.error('Unknown OS detected (%s)... exiting' % sys.platform)
    sys.exit()

# Locate other linux installer (e.g. apt, dnf, etc...) 

# Give us a chance to back out
timer=10
logging.warning('*** Warning: About to alter system, abort by pressing ctrl-c in the next %s seconds!' % timer)
try:
    print('    ')
    for i in range(timer):
        time.sleep(1)
        print('%s... ' % str(timer-i), end='')
        sys.stdout.flush()
    print('\n')

except:
    logging.warning('User aborted, exiting...\n')
    sys.exit()

# Update installer 
update_command = installer_command + ' ' + installer_command_update
logging.info('Updating package manager with \'%s\'' % update_command)
# os.system(update_command)
logging.info('Updating package manager... DONE!')

# Install wget
common_install('wget')

# Install git
common_install('git')

# Install ZSH
common_install('zsh')

# Install pip 
common_install('pip')

# Install Python pipenv 
common_install('pipenv')

# Install Screen
common_install('screen')

# Install TMUX
common_install('tmux')

# Install ohmyzsh 

# Install the LAMP stack...

# Install php 

# Install Apache 

# Install gnu coreutils on mac 
if sys.platform == 'darwin':
    common_install('coreutils')

# Set up my favorite aliases 
# copy over a .aliases file, and source it

# Prompt each step options 

# Set home dir permissions 

# Add custom home directory folders

# Install network tools 
	# Hping 
common_install('hping')
	# NMap 
common_install('nmap')

# Install vim, emacs, nano
common_install('vim')

# Install mutt 

# Install ssh and gen keys 

logging.info("DONE!")
if not args.quiet:
    print('')


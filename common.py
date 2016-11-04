#!/usr/bin/python3
###############################################################################
#
# Copyright (c) 2015-2016, Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

import logging
import os
import shutil
import subprocess

# $YARPGEN_HOME environment variable should be set to YARP Generator directory
yarpgen_home = ""

def print_and_exit (msg):
    logging.error(msg)
    exit (-1)


def check_and_open_file(file_name, mode):
    if (not os.path.isfile(file_name)):
        print_and_exit("File " + file_name + " doesn't exist and can't be opened")
    return open(file_name, mode)


def check_and_copy (src, dst):
    if not isinstance(src, str) or not isinstance(dst, str):
        print_and_exit("Src and dst should be strings")
    if os.path.exists(src):
        logging.debug("Copying " + src + " to " + dst)
        shutil.copy(src, dst)
    else:
        print_and_exit("File " + src + " wasn't found")


def check_dir_and_create (directory):
    if (not os.path.exists(directory)):
        logging.debug("Creating '" + str(directory) + "' directory")
        os.makedirs(directory)
    elif (not os.path.isdir(directory)):
        print_and_exit("Can't use '" + directory + "' directory")


def run_cmd (cmd, time_out = None, num = -1):
    time_expired = False
    ret_code = 0
    try:
        log_msg = "Running " + str(cmd)
        if (num != -1):
            log_msg += " in process " + str(num)
        logging.debug(log_msg)
        compl_proc = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, timeout = time_out, check = True)
        compl_proc.check_returncode()
        ret_code = compl_proc.returncode
        output = compl_proc.stdout
        err_output = compl_proc.stderr
    except subprocess.CalledProcessError as cpe:
        logging.debug(str(cmd) + " failed")
        ret_code = cpe.returncode
        output = cpe.stdout
        err_output = cpe.stderr
    except subprocess.TimeoutExpired as te:
        logging.debug("Timeout expired while executing " + str(cmd))
        time_expired = True
        ret_code = None
        output = te.stdout
        err_output = te.stderr
    return ret_code, output, err_output, time_expired


def if_exec_exist (program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    logging.debug("Checking if " + str(program) + " exists")
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            logging.debug("Exec " + program + " was found at " + program)
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                logging.debug("Exec " + program + " was found at " + exe_file)
                return True
    logging.debug("Exec wasn't found")
    return False

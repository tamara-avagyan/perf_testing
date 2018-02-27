#!/usr/bin/python

import argparse
import datetime
import subprocess
import csv
import ast
import json
import shutil
import os
from string import Template
from distutils.spawn import find_executable
import re
import sys
import time

def run_command(command):
    subprocess.call(command, shell=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Execute BODI system tests.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-r", "--results",
        default = "results/" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        help = "Directory wher all the result files and logs should be written")
    parser.add_argument("--threads",
        default = "1",
        help = "Max amount of simulation threads to be executed")
    parser.add_argument("--Xms",
        default = "1G",
        help = "Xms (The initial memory allocation pool)")
    parser.add_argument("--Xmx",
        default = "3G",
        help = "Xmx (The maximum memory allocation pool)")
    parser.add_argument("--delay",
        default = "0",
        help = "Duration (in minutes) of delay before launching simulation threads")
    parser.add_argument("--startup",
        default = "1",
        help = "Duration (in minutes) of increasing simulation threads from 0 to MAX")
    parser.add_argument("--hold",
        default = "1",
        help = "Duration (in minutes) of holding simulation threads at MAX")
    parser.add_argument("--shutdown",
        default = "1",
        help = "Duration (in minutes) of decreasing simulation threads from MAX to 0")
    parser.add_argument("--pause",
        default = "1",
        help = "Delay duration (in seconds) between the requests.")
    parser.add_argument("--loop_count",
        default = "1",
        help = "Loop count to hit each API.")
    parser.add_argument("--is_blog_testing",
        default = False,
        help = "Is Blog testing: Need to generate correct grafana grafs")
    parser.add_argument("--page_path",
        default = "/",
        help = "Page path to test node js performance.")
    parser.add_argument("test",
        help = "JMX file that should be executed")
    parser.add_argument("environment",
        help = "Environment properties file")
    parser.add_argument('-c', '--calculate_users', 
            dest='calculate', 
            nargs='?',
            const=True, 
            default=False,
            help='Calculate Active Users count during the testing. Note it is the correct value for real user scenario only.')
    args = parser.parse_args()
    return args

def run_jmeter(arguments):
#     jmeter_dir = find_executable('jmeter')
    jmeter_dir_bin = ~/Downloads/apache-jmeter-3.3/bin

    if (os.environ.has_key('BUILD_NUMBER')):
        build_number = os.environ['BUILD_NUMBER']
    else:
        build_number= ''
    template = '''java -Xms$Xms -Xmx$Xmx -jar ''' + jmeter_dir_bin + '''/ApacheJMeter.jar -n \\
        -t $test \\
        -q $environment \\
        -l $results/results.jtl \\
        -j $results/jmeter.log \\
        -Dlog4j.configurationFile=../log4j2.xml \\
        -JRESULTS_DIR=$results \\
        -JTHREADS=$threads \\
        -JSTARTUP=$startup \\
        -JHOLD=$hold \\
        -JSHUTDOWN=$shutdown \\
        -JPAUSE=$pause \\
        -JLOOP_COUNT=$loop_count \\
        -JPAGE_PATH=$page_path \\
        -JBUILD_NUMBER=''' + build_number
        #-JDELAY=$delay \\
    command = Template(template).substitute(arguments)
    print ('Build number - ', build_number)
    run_command(command)


def main():
    args = parse_args()
    if not os.path.exists(args.results):
        os.makedirs(args.results)
    start_time = datetime.datetime.now()
    print ("waiting " + args.delay + " min...")
    time.sleep(60 * float(args.delay))  # Delay by minute before testing
    print ("end waiting ... ")
    run_jmeter(args.__dict__)


main()

#Watch Dogs Artificial Assistant
#Write by Pyrra in Python 3.8.0-

#This script is for fun, test and educationnal purpose only

import os
import time
import getpass
import platform
import webbrowser
import socket
import pyttsx3
import requests
import speech_recognition as sr 
from datetime import datetime
from colorama import init 
from termcolor import colored 
import subprocess
import sys
import keyboard 
try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
import argparse


date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
username = getpass.getuser()
#system = platform.system()

engine = pyttsx3.init()
speech = sr.Recognizer()
#for voice in voices:     UNCOMMENT IT ONLY IF YOU WANT TO CHANGE THE VOICES
#    print(voice.id)
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-15)

def speak_text_cmd(cmd):
    engine.say(cmd)
    engine.runAndWait()

def get_server_ip():
     print(colored(": What is the target ?", 'blue'))
     speak_text_cmd("What is the target ?")
     host = input()
     print(colored(": target set to " + host, 'blue'))
     speak_text_cmd('target set to ' + host)
     time.sleep(1)
     print(': starting...')
     speak_text_cmd('starting')
     ip = socket.gethostbyname(host)
     print(colored(": the ip adress of " + host + " is " + ip, 'green'))
     speak_text_cmd('The ip adress of the target is: ' + ip)

def get_website_response_code():
     import requests
     print(colored(": What is the target ?", 'blue'))
     speak_text_cmd("What is the target ?")
     target = input()
     print(colored(": target set to " + target, 'blue'))
     speak_text_cmd('target set to ' + target)
     time.sleep(1)
     print(': starting...')
     speak_text_cmd('starting')
     req = requests.get(target)
     print('Response Code:' + str(req.status_code))
     print("\nResponse:\n" + req.text)

def get_server_info():
     import socket
     s = socket.socket()
     s.settimeout(2)
     print(colored(": What is the target ?", 'blue'))
     speak_text_cmd("What is the target ?")
     target = input()
     print(colored(": target set to " + target, 'blue'))
     speak_text_cmd('target set to ' + target)
     time.sleep(1)
     print(': starting...')
     speak_text_cmd('starting')
     s.connect((target, 80))
     s.send('HEAD / HTTP?1.1\nHost:', target, '\n\n')
     print (s.recv(1024))
     s.close

def parse_args():
     """Parse arguments."""
     parser = argparse.ArgumentParser(
     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
     description='Diagnose script for checking the current system.')
     choices = ['python', 'pip', 'mxnet', 'os', 'hardware', 'network']
     for choice in choices:
          parser.add_argument('--' + choice, default=1, type=int,
                            help='Diagnose {}.'.format(choice))
     parser.add_argument('--region', default='', type=str,
                        help="Additional sites in which region(s) to test. \
                        Specify 'cn' for example to test mirror sites in China.")
     parser.add_argument('--timeout', default=10, type=int,
                        help="Connection test timeout threshold, 0 to disable.")
     args = parser.parse_args()
     return args

URLS = {
     'MXNet': 'https://github.com/apache/incubator-mxnet',
    'Gluon Tutorial(en)': 'http://gluon.mxnet.io',
    'Gluon Tutorial(cn)': 'https://zh.gluon.ai',
    'FashionMNIST': 'https://apache-mxnet.s3-accelerate.dualstack.amazonaws.com/gluon/dataset/fashion-mnist/train-labels-idx1-ubyte.gz',
    'PYPI': 'https://pypi.python.org/pypi/pip',
    'Conda': 'https://repo.continuum.io/pkgs/free/',
}
REGIONAL_URLS = {
    'cn': {
        'PYPI(douban)': 'https://pypi.douban.com/',
        'Conda(tsinghua)': 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/',
    }
}

def test_connection(name, url, timeout=10):
    """Simple connection test"""
    urlinfo = urlparse(url)
    start = time.time()
    try:
        ip = socket.gethostbyname(urlinfo.netloc)
    except Exception as e:
        print('Error resolving DNS for {}: {}, {}'.format(name, url, e))
        return
    dns_elapsed = time.time() - start
    start = time.time()
    try:
        _ = urlopen(url, timeout=timeout)
    except Exception as e:
        print("Error open {}: {}, {}, DNS finished in {} sec.".format(name, url, e, dns_elapsed))
        return
    load_elapsed = time.time() - start
    print("Timing for {}: {}, DNS: {:.4f} sec, LOAD: {:.4f} sec.".format(name, url, dns_elapsed, load_elapsed))

def check_python():
    print('----------Python Info----------')
    print('Version      :', platform.python_version())
    print('Compiler     :', platform.python_compiler())
    print('Build        :', platform.python_build())
    print('Arch         :', platform.architecture())

def check_pip():
    print('------------Pip Info-----------')
    try:
        import pip
        print('Version      :', pip.__version__)
        print('Directory    :', os.path.dirname(pip.__file__))
    except ImportError:
        print('No corresponding pip install for current python.')

def check_mxnet():
    print('----------MXNet Info-----------')
    try:
        import mxnet
        print('Version      :', mxnet.__version__)
        mx_dir = os.path.dirname(mxnet.__file__)
        print('Directory    :', mx_dir)
        commit_hash = os.path.join(mx_dir, 'COMMIT_HASH')
        with open(commit_hash, 'r') as f:
            ch = f.read().strip()
            print('Commit Hash   :', ch)
    except ImportError:
        print('No MXNet installed.')
    except Exception as e:
        import traceback
        if not isinstance(e, IOError):
            print("An error occured trying to import mxnet.")
            print("This is very likely due to missing missing or incompatible library files.")
        print(traceback.format_exc())

def check_os():
    print('----------System Info----------')
    print('Platform     :', platform.platform())
    print('system       :', platform.system())
    print('node         :', platform.node())
    print('release      :', platform.release())
    print('version      :', platform.version())

def check_hardware():
    print('----------Hardware Info----------')
    print('machine      :', platform.machine())
    print('processor    :', platform.processor())
    if sys.platform.startswith('darwin'):
        pipe = subprocess.Popen(('sysctl', '-a'), stdout=subprocess.PIPE)
        output = pipe.communicate()[0]
        for line in output.split(b'\n'):
            if b'brand_string' in line or b'features' in line:
                print(line.strip())
    elif sys.platform.startswith('linux'):
        subprocess.call(['lscpu'])
    elif sys.platform.startswith('win32'):
        subprocess.call(['wmic', 'cpu', 'get', 'name'])

def check_network(args):
    print('----------Network Test----------')
    if args.timeout > 0:
        print('Setting timeout: {}'.format(args.timeout))
        socket.setdefaulttimeout(10)
    for region in args.region.strip().split(','):
        r = region.strip().lower()
        if not r:
            continue
        if r in REGIONAL_URLS:
            URLS.update(REGIONAL_URLS[r])
        else:
            import warnings
            warnings.warn('Region {} do not need specific test, please refer to global sites.'.format(r))
    for name, url in URLS.items():
        test_connection(name, url, args.timeout)
#def exit():
     
def get_full_info():
     print(colored(": Getting system info and network speed", 'blue'))
     speak_text_cmd("Getting system info and network speed")
     import platform, subprocess, sys, os
     import socket, time
     try:
          from urllib.request import urlopen
          from urllib.parse import urlparse
     except ImportError:
          from urlparse import urlparse
          from urllib2 import urlopen
     import argparse
     args = parse_args()
     if args.python:
        check_python()

     if args.pip:
        check_pip()

     if args.mxnet:
        check_mxnet()

     if args.os:
        check_os()

     if args.hardware:
        check_hardware()

     if args.network:
        check_network(args)


def subdomain_scanner():
     import requests
     os.system('cls')
     print("Subdomain scanner lauch at", date, "on", platform.system(), "by", username)
     speak_text_cmd("Subdomain scanner lauch at" + date + "on" + platform.system() + "by" + username)
     print(colored("What is the target(eg: google.com): ", 'blue'))
     speak_text_cmd("What is the target ?")
     domain = input()
     print(colored("Domain set to " + domain, 'blue'))
     speak_text_cmd("Domain set to " + domain)
     print(colored("starting...", 'blue'))
     speak_text_cmd("starting")
     file = open("subdomains.txt")
     content = file.read()
     subdomains = content.splitlines()
     for subdomain in subdomains:
          url = f"http://{subdomain}.{domain}"
          try:
               requests.get(url)
          except requests.ConnectionError:
               pass
          else:
               print("[+] Discovered subdomain:", url)


def ddos_attack():
     os.system('python ddos.py')

def instagram_attack():
     print(colored(": Lauching instagram bruteforce programm...", 'blue'))
     speak_text_cmd("Lauching instagram bruteforce programm")
     print(colored("""
     ################# Instagram Bruteforce Program #################
     #                                                              #
     # modes: 0 => 32 bots; 1 => 16 bots; 2 => 8 bots; 3 => 4 bots  #
     #                                                              #
     ################################################################
     """, 'blue'))
     print(colored(": Please enter the username: ", 'blue'))
     speak_text_cmd("Please enter the username")
     instaUsername = input()
     print(colored(": Please enter the mode: ", 'blue'))
     speak_text_cmd("Please enter the mode")
     instaMode = input()
     print(colored("The target username is:" + instaUsername + "and the crack mode is: " + instaMode, 'blue'))
     speak_text_cmd("The target username is: " + instaUsername + " and the crack mode is: " + instaMode)
     print(colored(": Starting attack", 'blue'))
     speak_text_cmd("Starting attack")
     os.system('python instagram.py ' + instaUsername + ' passwords.txt ' + '-m '+ instaMode)

def credit():
     print(colored("""
     ###################################################################
     #                      Script code by Pyrra                       #
     #                                                                 #
     #                DDos script 1: Memcrashed ddos                   #                             
     #                        Use python 3.8                           #
     #   Speech recognition, pyttsx3, socket and more python module    #
     #              Contact at pyrra@mail.com for advice               #
     #              and be part of the developpers team                #
     #       See my github page for more info(just search Pyrra)       #
     # #################################################################""", 'blue'))
     

def manual_mode():
     os.system('cls')
     print(colored("""

      ██▓███ ▓██   ██▓ ██▀███   ██▀███   ▄▄▄      
     ▓██░  ██▒▒██  ██▒▓██ ▒ ██▒▓██ ▒ ██▒▒████▄    
     ▓██░ ██▓▒ ▒██ ██░▓██ ░▄█ ▒▓██ ░▄█ ▒▒██  ▀█▄  
     ▒██▄█▓▒ ▒ ░ ▐██▓░▒██▀▀█▄  ▒██▀▀█▄  ░██▄▄▄▄██ 
     ▒██▒ ░  ░ ░ ██▒▓░░██▓ ▒██▒░██▓ ▒██▒ ▓█   ▓██▒
     ▒▓▒░ ░  ░  ██▒▒▒ ░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░
     ░▒ ░     ▓██ ░▒░   ░▒ ░ ▒░  ░▒ ░ ▒░  ▒   ▒▒ ░
     ░░       ▒ ▒ ░░    ░░   ░   ░░   ░   ░   ▒   
             ░ ░        ░        ░           ░  ░
             ░ ░                                 

     """, 'green'))
     print(": Pyrra manual control mode launch at:", date, "on", platform.system(), "by", username,)
#speak_text_cmd('Pyrra launch at:' + date +  'on'+ SystemPlatform + 'by'+ username)
     print(colored(": Hello " + username, 'blue'))
     speak_text_cmd('Hello' + username)
     print(colored(': What can I do for you ?', 'blue'))
     speak_text_cmd('What can I do for you ?')
     while True:
          menu_opt = input(':')
          if 'get server ip' in menu_opt:
               get_server_ip()
               continue
          elif 'website response code' in menu_opt:
               get_website_response_code()
               continue
          elif 'voice control mode' in menu_opt:
               print(colored(": Do you want to enter voice control mode ? y/n", 'blue'))
               speak_text_cmd("Do you want to enter voice control mode ? yes or no")
               voice_control_opt = input(": ")
               if voice_control_opt == 'y':
                    voice_control_mode()
               elif voice_control_opt == 'n':
                    continue
               else:
                    print(": Invalid option")
                    speak_text_cmd('Invalid option')
                    continue
          elif 'get server info' in menu_opt:
               get_server_info()
               continue
          elif 'get system info' in menu_opt:
               get_full_info()
               continue
          elif 'ddos attack' in menu_opt:
               ddos_attack()
               continue
          elif 'exit' in menu_opt:
               print(colored(": Bye " + username, 'blue'))
               speak_text_cmd("Bye " + username)
               print(": Pyrra stop at:", date, "on", platform.system(), "by", username)
               quit()
          elif 'credit' in menu_opt:
               credit()
               continue
          elif 'facebook bruteforce' in menu_opt:
               print(colored(": Launching facebook bruteforce program...", 'blue'))
               speak_text_cmd("Launching facebook bruteforce program")  
               os.system('python fb.py')
               continue
          elif 'instagram bruteforce' in menu_opt:
               instagram_attack()
               continue
          elif 'subdomain scanner' in menu_opt:
               subdomain_scanner()
               continue


def read_voice_cmd():
   voice_text = ''
   print(colored('Listening...', 'red'))
   with sr.Microphone() as source:
       audio = speech.listen(source)
   try:
        #voice_text = speech.recognize_bing(audio)
        voice_text = speech.recognize_google(audio)
   except sr.UnknownValueError:
        pass
   except sr.RequestError as e:
        print('Network error.')
   return  voice_text

# MAIN PART
def voice_control_mode():
     os.system('cls')
     print(colored("""

      ██▓███ ▓██   ██▓ ██▀███   ██▀███   ▄▄▄      
     ▓██░  ██▒▒██  ██▒▓██ ▒ ██▒▓██ ▒ ██▒▒████▄    
     ▓██░ ██▓▒ ▒██ ██░▓██ ░▄█ ▒▓██ ░▄█ ▒▒██  ▀█▄  
     ▒██▄█▓▒ ▒ ░ ▐██▓░▒██▀▀█▄  ▒██▀▀█▄  ░██▄▄▄▄██ 
     ▒██▒ ░  ░ ░ ██▒▓░░██▓ ▒██▒░██▓ ▒██▒ ▓█   ▓██▒
     ▒▓▒░ ░  ░  ██▒▒▒ ░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░
     ░▒ ░     ▓██ ░▒░   ░▒ ░ ▒░  ░▒ ░ ▒░  ▒   ▒▒ ░
     ░░       ▒ ▒ ░░    ░░   ░   ░░   ░   ░   ▒   
             ░ ░        ░        ░           ░  ░
             ░ ░                                 

     """, 'green'))
     print(": Pyrra launch at:", date, "on", platform.system(), "by", username,)
#speak_text_cmd('Pyrra launch at:' + date +  'on'+ SystemPlatform + 'by'+ username)
     print(colored(": Hello " + username, 'blue'))
     speak_text_cmd('Hello' + username)
     print(colored(': What can I do for you ?', 'blue'))
     speak_text_cmd('What can I do for you ?')
     while True:
          voice_note = read_voice_cmd()
          print(colored(': {}'.format(voice_note), 'green'))
          if 'get server IP' in voice_note:
               get_server_ip()
               continue
          elif 'website source code' in voice_note:
               get_website_response_code()
               continue
          elif 'manual mode' in voice_note:
               print(colored(": Entering manual input and control mode", 'blue'))
               speak_text_cmd('Entering manual control mode')
               manual_mode()
               continue
          elif 'get server info' in voice_note:
               get_server_info()
               continue
          elif 'get system info' in voice_note:
               get_full_info()
               continue
          elif 'DDOS attack' in voice_note:
               ddos_attack()
               continue
          elif 'exit' in voice_note:
               print(colored(": Bye " + username, 'blue'))
               speak_text_cmd("Bye " + username)
               print(": Pyrra stop at:", date, "on", platform.system(), "by", username)
               quit()
          elif 'credit' in voice_note:
               credit()
               continue
          elif 'facebook bruteforce' in voice_note:
               print(colored(": Launching facebook bruteforce program...", 'blue'))
               speak_text_cmd("Launching facebook bruteforce program")  
               os.system('python fb.py')
               continue
          elif 'instagram bruteforce' in voice_note:
               instagram_attack()
               continue
          elif 'subdomain scanner' in voice_note:
               subdomain_scanner()
               continue
          else:
               print(colored(": No command detected, do you want to enter manual control mode ? y/n", 'blue'))
               speak_text_cmd("No command detect detected, do you want to enter manual control mode ? yes or no")
               manual_control_opt = input()
               if manual_control_opt == 'y':
                    manual_mode()
               elif manual_control_opt == 'n':
                    pass
               else:
                    print(": Invalid option")
                    speak_text_cmd('Invalid option')
                    continue
          

voice_control_mode()
import os
import platform
import sys
import time
import json

try:
    from ConfigParser import RawConfigParser ,NoSectionError,  NoOptionError
except:
    from configparser import RawConfigParser ,NoSectionError, NoOptionError
from collections import OrderedDict
import argparse

if sys.version_info.major == 2:
    # Python2
    from urllib import urlencode
    from urllib import quote
    from urlparse import urlparse
    import urllib2 as request
else:
    # Python3
    from urllib.parse import urlencode  
    from urllib.parse import quote
    from urllib.parse import urlparse
    import urllib.request as request

config = RawConfigParser()


PIP_CONF_PATH = LINUX_PIP_CONF_PATH = "%s/.pip/pip.conf" % (os.path.expanduser('~'))
PYRM_DIR   = LINUX_PYRM_DIR  =  "%s/.pip" % (os.path.expanduser('~'))
WIN_PIP_CONF_PATH = "%s\pip\pip.ini" % ( os.environ.get("HOMEPATH"))
WIN_PYRM_DIR = "%s\pip" % ( os.environ.get("HOMEPATH"))
PYRM_PATH =  os.path.join(os.path.split(os.path.realpath(__file__))[0],"pip.json")
 
sysstr = platform.system()
if(sysstr =="Windows"):
    PIP_CONF_PATH = WIN_PIP_CONF_PATH
    PYRM_DIR = WIN_PYRM_DIR
elif(sysstr == "Linux"):
    PIP_CONF_PATH = LINUX_PIP_CONF_PATH
else:
    PIP_CONF_PATH = LINUX_PIP_CONF_PATH
    print("Unsupported System - ",sysstr)


GLOBAL_SECTION = 'global'
CONF_TEMPLATE ='''[global]
timeout = 60
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com
'''

def init_pip_conf():
    try:
        os.makedirs(PYRM_DIR)
    except :
        pass

    with open(PIP_CONF_PATH,"w") as pip_conf_f:
        pip_conf_f.write(CONF_TEMPLATE)



if not os.path.exists(PIP_CONF_PATH):
    init_pip_conf()

try:
    config.get(GLOBAL_SECTION,"index-url")
    config.get(GLOBAL_SECTION,"trusted-host")
    config.getint(GLOBAL_SECTION,"timeout")
except :
    init_pip_conf()

config.read(PIP_CONF_PATH)

PIP_LIST = OrderedDict()
SYS_PIP_LIST =  OrderedDict()
SYS_PIP_LIST_REVERSE =  OrderedDict()
 

def load_pip_local_list():

    global SYS_PIP_LIST, SYS_PIP_LIST_REVERSE
    with open(PYRM_PATH) as pip_local_list_f:
        SYS_PIP_LIST = json.loads(pip_local_list_f.read())
        SYS_PIP_LIST_REVERSE = {value:key for key,value in SYS_PIP_LIST.items()}
        return SYS_PIP_LIST

def get_current_pip_conf():

    index_url = None
    trusted_host = None
    timeout = -1

    try :
        index_url =  config.get(GLOBAL_SECTION,"index-url")
    except NoSectionError as e:
        print(e)

    try :
        trusted_host = config.get(GLOBAL_SECTION,"trusted-host")
    except  (NoSectionError,NoOptionError):
        try:
            trusted_host = config.get("install","trusted-host")
        except Exception as e:
            print(e)

    try :
        timeout =  config.getint(GLOBAL_SECTION,"timeout")
    except  NoSectionError as e:
        print(e)

    return index_url,trusted_host,timeout

def set_current_pip_conf(index_url=None,trusted_host=None,timeout=None):
    '''
    set current pip config file
    '''
    if index_url:
        config.set(GLOBAL_SECTION, 'index-url', index_url)

    if trusted_host:
        config.set(GLOBAL_SECTION, 'trusted-host', trusted_host)

    if timeout:
        config.set(GLOBAL_SECTION, 'timeout', timeout)

    with open(PIP_CONF_PATH,"w") as pip_conf_f:
        config.write(pip_conf_f)

def test_pip_source_speed(url,default_timeout=5):

    start = time.time() 
    try: 
        f = request.urlopen(url,timeout=default_timeout) 
    except Exception as e: 
        return url,99999,e
    else: 
        try:
            f.readline() 
        except :
            return url,time.time() -start,None
        f.close() 
        return url,time.time() -start,None

def test_pip_list_speed():
    print("[+] May cost your few minutes according your network situation.\n")

    with open(PYRM_PATH) as pip_list_f:

        pip_list = json.loads(pip_list_f.read())
        for pip_url in pip_list.items():
            url,speed,err = test_pip_source_speed(pip_url[1])
            if err:
                print("[+] %s\t%s\t%s" % (pip_url[0],url.strip(),err))
            else:
                print ("[+] %s\t%s\t%s" % (pip_url[0],url.strip(),speed))
            PIP_LIST[url.strip()] = round(speed,3) 

def sort_pip_list():

    return sorted(PIP_LIST.items(), lambda x, y: cmp(x[1], y[1])) 

def get_fastest_pip():

    test_pip_list_speed()

    pip_list = sort_pip_list()

    if pip_list:
        print ("\n\n[+] BEST PIP : %s  -  %s ,SPEED: %s" % (SYS_PIP_LIST_REVERSE.get(pip_list[0][0],"UNKNOWN"), pip_list[0][0],pip_list[0][1]))

    use([SYS_PIP_LIST_REVERSE.get(pip_list[0][0],"UNKNOWN")])

def save_pip_conf():

    with open(PYRM_PATH,"w") as pip_list_f:
        pip_list_f.write(json.dumps(SYS_PIP_LIST))

###########################################


def list(*args):

    with open(PYRM_PATH) as pip_list_f:
        pip_list = json.loads(pip_list_f.read())
        for pip_url in pip_list.items():
            print("%s      \t\t(%s)" % (pip_url[0],pip_url[1]))

def current(*args):

    print ("[*] %s" %( SYS_PIP_LIST_REVERSE.get(get_current_pip_conf()[0].strip("/"))))

def update_pip_list():
    pass

def recover(*args):

    set_current_pip_conf(index_url="https://pypi.python.org/simple",trusted_host="pypi.python.org",timeout=60)

def test(*args):

    if len(args[0]) > 1:
        exit("0 or 1 arg is needed")
    elif len(args[0])==0:
        test_pip_list_speed()
    else:

        url,speed,err = test_pip_source_speed(SYS_PIP_LIST.get(args[0][0],'not found source'))

        if not err:
            print ('%s - %s - %s(s)' % (args[0][0], url, round(speed,2)))
        else:
            print ('%s - %s - %s(s)' % (args[0][0], url, err))

def add(*args):

    if len(args[0]) is not 2:
        exit("2 args are needed")
    registry = args[0][0]
    url = args[0][1]
    print ('ADD %s - %s' % (registry, url))
    global SYS_PIP_LIST
    SYS_PIP_LIST[registry.strip()] = url.strip()
    save_pip_conf()

def rm(*args):

    if len(args[0]) is not 1:
        exit("2 args are needed")
    
    registry = args[0][0]
    url = SYS_PIP_LIST.get(registry,None)
    print ('DEL %s - %s' % (registry, url))
    del SYS_PIP_LIST[registry]
    save_pip_conf()

def use(*args):

    if len(args[0]) is not 1:
        exit("1 arg is needed")
    registry = args[0][0]
    url = SYS_PIP_LIST.get(registry,None)
    if url:
        print ('USE %s - %s' % (registry, url))
        pr = urlparse(url)
        set_current_pip_conf(index_url=url,trusted_host = "%s" % (pr.netloc))

def auto(*args):
    get_fastest_pip()

def help(*args):

    print ('''
Usage: faster [options] [command]

Options:
  -V, --version                output the version number
  -h, --help                   output usage information

Commands:
  auto                          Auto get the fastest registry
  list                           List all the registries
  current                       Show current registry name
  use <registry>               Change registry to registry
  add <registry> <url>         Add one custom registry
  rm  <registry>                Delete one custom registry
  test [registry]              Show response time for specific or all registries
  recover                      Recover  to official registry
  help                         Print this help
''')


def start():
    
    load_pip_local_list()

    parser = argparse.ArgumentParser(description='python pip resource manager')

    parser.add_argument('cmd', type=str, nargs='*',
                        help='help')

    args = parser.parse_args()
    if args.cmd:
        globals().get(args.cmd[0],globals().get('help'))(args.cmd[1:])
    else:
        help()

if __name__ == "__main__":
    start()
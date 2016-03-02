#!/usr/bin/env python
from __future__ import print_function

import getpass,os,re,signal,subprocess,sys
import pexpect

ssh = None

def handler(signum, frame):
    if ssh:
        ssh.kill(signum)
    sys.exit(signum)

signal.signal(signal.SIGQUIT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

def winch_handler(signum, frame):
    if ssh:
        rows, cols = os.popen('stty size', 'r').read().split()
        ssh.setwinsize(int(rows), int(cols))

signal.signal(signal.SIGWINCH, winch_handler)

ssh = pexpect.spawn("ssh", sys.argv[1:])
winch_handler(None, None)

index = -1
pattern_list = ssh.compile_pattern_list([
    "Enter additional factors:.*",
    "----- BEGIN U2F CHALLENGE -----\r?\n([^\r\n]*)\r?\n(.*)\r?\n----- END U2F CHALLENGE -----",
    "Welcome.*",
    pexpect.EOF
])
while True:
    index = ssh.expect_list(pattern_list)
    if index == 0:
        try:
            pin = getpass.getpass(ssh.match.group())
        except EOFError:
            pin = ""
        ssh.sendline(pin)
    elif index == 1:
        p = subprocess.Popen(["/usr/local/bin/u2f-host", "-aauthenticate",
                              "-o", ssh.match.group(1)],
                             env={"LD_LIBRARY_PATH": "/usr/local/lib"},
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate(ssh.match.group(2))
        p.stdin.close()
        p.wait()
        ssh.sendline(out.strip())
    else:
        break
if index == 3:
    sys.exit(0)
sys.stdout.write(ssh.match.group())
ssh.interact()

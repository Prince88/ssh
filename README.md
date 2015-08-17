# ssh
This is a simple script for day to day use for executing commands/Copy files on remote linux/unix flavour machines
sample usage:

import ssh

>>> sshclient = ssh("10.213.157.25","root","Recnex#1")
>>> sshclient.execute("mkdir -p /prince")
('Output returned is None', 0)
>>> sshclient.execute("touch /prince/test.txt")
('Output returned is None', 0)
>>> sshclient.execute("ls /prince")
(b'test.txt\n', 0)
>>> 

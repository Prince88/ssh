#-------------------------------------------------------------------------------
# Name:        ssh.py
# Purpose:     Module to make ssh connections and execute command, transfer files
#
# Author:      Prince Sharma
#
# Created:     04/08/2015
# Licence:     GNU GENERAL PUBLIC LICENSE Version 2, June 1991
#-------------------------------------------------------------------------------

import paramiko
import os

class ssh(object):
    """
    @purpose: Generic class which returns ssh object which can further be used with functions in the class
    @args: username and password
    """

    def __init__(self,IP,username,password):

        """
        @purpose: Intialization of class variables
        @args: IPaddress, username, password
        """
        
        self.IP = IP
        self.username = username
        self.password = password
        self._ssh = None
        self._sftp = None


    def _getConnection(self):

        """
        @purpose: Creates a new SSH connection
        @args: None
        """
        try:
            
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(self.IP,username=self.username,password=self.password)
        except Exception as e:
            raise str(e)        
    def _checkConnection(self):

        """
        @purpose: Verifies if the connection is still active to avoid situations for closed connections
        @args: None
        """

        if self._ssh is not None:
            if self._ssh.get_transport().is_active():
                return True
            else:
                return False
        else:
            self._getConnection()
            

    def execute(self,command):

        """
        @purpose: Executes commands and returns the stdout/error
        @args: command to be executed
        """
        try:
            ret = self._checkConnection()
            if not ret:
                self._getConnection()
            stdin,stdout,stderr = self._ssh.exec_command(command)
            output = stdout.read()
            error = stderr.read()
            stdin.flush()
            stdin.channel.shutdown_write()
            if output:
                return output, 0
            elif error:
                return error, 1
            else:
                #for commands like mkdir, rm where output returned is none.
                return "Output returned is None", 0 
        except:
            raise

        
    def copy(self,localpath,remotepath):

        """
        @purpose: Copies local folder to remote path, returns True in case of success else False
        @args: localpath, remotepath
        """

        try:
            if not self._checkConnection():
                self._getConnection()

            #create the remotepath
            ret, status = self.execute("mkdir -p %s " % remotepath)
            #get all the files to be transferred
            files = os.listdir(localpath)
            self._sftp = self._ssh.open_sftp()
            for f in files:
                fpath = localpath + os.sep + f
                if os.path.isfile(fpath):
                    self._sftp.put(fpath,remotepath + "//" + f)
        except:
            raise


    def close(self):

        """
        @purpose: Teardown
        @args: None
        """

        if self._ssh is not None:
            self._ssh.close()
            

if __name__ == '__main__':
    sshclient = ssh("10.213.157.25","root","Recnex#1")

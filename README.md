[![Build Status](https://travis-ci.org/privacyidea/pam_python.svg?branch=master)](https://travis-ci.org/privacyidea/pam_python)

This module is to be used with http://pam-python.sourceforge.net/.
It can be used to authenticate with OTP against privacyIDEA. It will also 
cache future OTP values to enable offline authentication.

To be used like this::

   auth   requisite    pam_python.so /path/to/modules/privacyidea-pam.py

It can take the following parameters:

**url=https://your-server** 

   default is https://localhost
  
**debug**

   write debug information to the system log
   
**realm=yourRealm**

   pass additional realm to privacyidea
   
**nosslverify**

   Do not verify the SSL certificate
   
**prompt=<Prompt>**

   The password prompt. Default is "Your OTP".
   
**sqlfile=<file>**

   This is the SQLite file that is used to store the offline authentication 
   information.
   The default file is /etc/privacyidea/pam.sqlite

**no_authtok**

  Do not set pam authtok to user input from OTP prompt.
  Useful if you want pam_unix to ask for user password after OTP authentication.

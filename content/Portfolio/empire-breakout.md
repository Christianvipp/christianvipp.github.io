
+++
title = "Empire-breakout"
date = 2024-11-07T04:26:45
draft = false
+++
Recon : 

rust scan

![2024-11-07_01-47.png](/images/2024-11-07_01-47.png)

5 open ports.. 

Scan : 
Nmap scan 

![2024-11-07_01-50.png](/images/2024-11-07_01-50.png)

Http server running on apache, Samba server with V. smbd 4.6.2 and another http server hosted by miniserv on V. 1.981 also with 20000 on 1.830 

OS runs on debian. 


Enumeration :

Website running on port 80 shows default apache page.

![2024-11-07_01-53.png](/images/2024-11-07_01-53.png)

viewing it source code beneath shows a message.

![2024-11-07_01-55.png](/images/2024-11-07_01-55.png)

Using https:///dcode.fr 

Decrypted it to this string..

![2024-11-07_01-56.png](/images/2024-11-07_01-56.png)

keep it note, might be useful along the line..


 `.2uqPEfj3D<P'a-3

Port 139&445


Using enum4linux, found 2 users, cyber & nobody.. 


tried the creds for webmin server on port 10000 but wasnt valid. 


Tried on webmin on port 20000 and it was valid.. 


![2024-11-07_02-54.png](/images/2024-11-07_02-54.png)

Now, get an interactive shell. 

click on the command shell in the application side bar

![2024-11-07_03-11.png](/images/2024-11-07_03-11.png)

set up a listener. 

since the application framework language runs on Perl, use a Perl payload
![2024-11-07_03-13.png](/images/2024-11-07_03-13.png)

to attempt a reverse connection..  

![2024-11-07_03-19.png](/images/2024-11-07_03-19.png)

got a shell and also the local.txt flag text. 

There is a `tar` binary in the user's directory.. ![2024-11-07_03-54.png](/images/2024-11-07_03-54.png)


checking gtfobins.. 

ability to read files..

![2024-11-07_03-55.png](/images/2024-11-07_03-55.png)

Try to read the passwd file..

![2024-11-07_04-00.png](/images/2024-11-07_04-00.png)

works well, read root's history file.. 

there is entries to the file .old_pass.bak in the /var/backups directory

reading the file reveals a potential password for root. 
![2024-11-07_04-09.png](/images/2024-11-07_04-09.png)

attempt to log in as root with that password.

Valid root login 
![2024-11-07_04-12.png](/images/2024-11-07_04-12.png)


also with the last flag..


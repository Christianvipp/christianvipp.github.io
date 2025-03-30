+++
title = "Creative"
date = "2025-03-30T00:55:44"
draft = false
+++

Recon & Scanning :

Utilizing rustscan and nmap to find open ports.. 
![2025-03-29_22-12.png](/images/2025-03-29_22-12.png)

2 open ports.. 

command executed - nmap -sCV -p 22,80 IP -T4 -oG creative
```# Nmap 7.95 scan initiated Sat Mar 29 22:15:16 2025 as: /usr/lib/nmap/nmap --privileged -sCV -p 22,80 -T4 -oG creative 10.10.37.0
Host: 10.10.37.0 ()     Status: Up
Host: 10.10.37.0 ()     Ports: 22/open/tcp//ssh//OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)/, 80/open/tcp//http//nginx 1.18.0 (Ubuntu)/
# Nmap done at Sat Mar 29 22:15:29 2025 -- 1 IP address (1 host up) scanned in 13.10 seconds
```

With nmap, figured out the additional info for the open ports, 22 hosts ssh server and 80 hosts a nginx server with the version information, we could deduce it runs on  LINUX host specifically UBuntu.. 

Enumeration :

PORT 80 :

Visiting the IP does not resolve, add the hostname to the hosts file.. 
how ? `nano /etc/hosts`  paste the ip and add the hostname, use sudo.. i.e 
`IP  hostname` 

Visiting again, this should pop.. 
![2025-03-29_22-23.png](/images/2025-03-29_22-23.png)

Source code - nothing 
Directory fuzzing -nothing
contact form seemed interesting but nothing likewise.


Subdomain fuzz - there is a hit..
![2025-03-29_22-54.png](/images/2025-03-29_22-54.png)

add to the hosts file like we did above..

Visit the subdomain -- 

![2025-03-29_22-58.png](/images/2025-03-29_22-58.png)

it is offline so it goes nowhere with a valid address but visiting the parent domain works fine.. 

![2025-03-29_23-00.png](/images/2025-03-29_23-00.png)

since it returns the contents of the site, we could try checking localhost which basically displays same contents.
Now we could try to fuzz for internal open, running ports.. 


Exploitation : 

curate the list you want to use. 

![2025-03-29_23-32.png](/images/2025-03-29_23-32.png)

a sneak-peek of mines.. 

paste it in position in burp suite's intruder tab , do not ignore capturing the request in BURP and the setting the variables to fuzz.. 

Results came back and we got a potential hit, 1337 has a directory listing.. 
![2025-03-29_23-36.png](/images/2025-03-29_23-36.png)

checking the home/user directory to find info, we got a user  `saad` . 

view `saad` directory to find more info.. 

![2025-03-29_23-41.png](/images/2025-03-29_23-41.png)

Couple of files  and directories including the user.txt.. 

![2025-03-29_23-43.png](/images/2025-03-29_23-43.png)

Navigating to the ssh directory, there is the id_RSA file, copy it and login as saad to get a stable shell.. 

Unfortunately, it is protected..
![2025-03-29_23-47.png](/images/2025-03-29_23-47.png)

 Using john the ripper which is a hash cracking tool, i was able to get the passphrase used.. 

![2025-03-29_23-52.png](/images/2025-03-29_23-52.png)

ACCESS GRANTED...

Maintaining access : 


![2025-03-29_23-54.png](/images/2025-03-29_23-54.png)


Privilege Escalation :

While enumerating to gain root.. 

concatenating the .bash_history file revealed some information the user's recent log activity on the host..![2025-03-29_23-58.png](/images/2025-03-29_23-58.png)
executing sudo -l to and using the password revealed we see binary `PING` which we are allowed to execute with root permissions. 

Although, we can not directly escalate privileges by executing “sudo” on the binary absolute path but you can use **_“env_keep += LD_PRELOAD”_** configuration to escalate. 

Using this article guide below
https://www.hackingarticles.in/linux-privilege-escalation-using-ld_preload/

![2025-03-30_00-07.png](/images/2025-03-30_00-07.png)

now let's compile it to generate a shared object.

![2025-03-30_00-33.png](/images/2025-03-30_00-33.png)

make sure you specify the full path of the binary


Dropped to a #shell  verifying that, executing id shows root and we got the user and the root flag.. 
![2025-03-30_00-30.png](/images/2025-03-30_00-30.png)

Till next time, ADios... 
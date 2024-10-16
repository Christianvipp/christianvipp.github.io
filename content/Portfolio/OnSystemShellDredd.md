+++
title = "Onsystemshelldredd"
date = 2024-10-14T16:25:52-04:00
draft = false
+++

## Platform: Proving Grounds  
**Level**: Easy  
**Name**: Onsystemshelldredd  

### Reconnaissance:

A quick rustscan shows 2 open ports, 2 and 61000.  
![Rustscan result](/images/ksnip_20231106-031514.png)

### Scanning:

I performed an nmap scan on the target to identify the services running, but nmap only identified one port (FTP), and not the other.  
I ran a separate nmap scan against the port, but nmap didn’t identify the service running on port 61000.  
![Nmap scan 1](/images/ksnip_20231106-032314.png)  
![Nmap scan 2](/images/ksnip_20231106-032614.png)

### Enumeration:

The FTP service on the target had a misconfiguration, allowing anonymous login with a random password.  
After logging into the FTP server, I found a directory named `.hannah` that contained an `id_rsa` file. I downloaded it to my attacker machine.  
![FTP enumeration](/images/ksnip_20231106-032534.png)

I now had an `id_rsa` file and a potential user (`hannah`), but no way to access the target, which led me to further enumerate port 61000.  
Using telnet for a banner grab on port 61000, I discovered that it was running SSH.  
![SSH banner grab](/images/ksnip_20231106-032656.png)

### Exploitation:

With the SSH key and the user `hannah`, I was able to log into the target machine.  
I listed the home directory of the user `hannah` and retrieved the first flag.  
![First flag](/images/ksnip_20231106-032803.png)

### Privilege Escalation:

To escalate privileges, I used the `linpeas` script to automate the search for potential privilege escalation vectors.  
In the `/usr/bin/` directory, I found two binaries owned by root, but the `cpulimit` binary caught my attention.  
![Privilege escalation binary](/images/ksnip_20231106-032846.png)

I inspected the binary, which showed the help usage of how it works.  
I needed to set both the `_UID_` and `_GID_` bits on the binary using the command `chmod +s`.  
![Setting UID/GID bits](/images/ksnip_20231106-033356.png)

After setting the necessary bits, I ran `/bin/bash -p`, which gave me a new shell as root.  
I successfully rooted the box.

Thank you, haxors!

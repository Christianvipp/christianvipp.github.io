
+++
title = "Gaara"
date = 2024-10-15T20:40:51
draft = false
tags = ["Weak SSH Credentials", "SUID Privilege Escalation", "Information Disclosure", "Misconfigured Services"]
+++

Platform : Proving Grounds

![2024-02-07_20-27.png](/images/2024-02-07_20-27.png)

The target is active and responding to the ICMP ping request. 

### Recon

A quick rust scan to find the open ports on the targets.
![2024-02-07_20-34.png](/images/2024-02-07_20-34.png)

There are 2 open ports: 22 (SSH) and 80 (HTTP). 

### Scanning

Run an nmap scan to confirm and identify the versions of those services.
![2024-02-07_20-32.png](/images/2024-02-07_20-32.png)

Yes, SSH and HTTP. Based on the banners (Debian), this is a Linux server.

### Enumeration

Starting with the web server running on port 80.

Visiting the website:
![2024-02-07_20-39.png](/images/2024-02-07_20-39.png)

An image of a cartoon/anime character and an email below. The source code didn't reveal anything interesting.

Proceeding to fuzz for hidden endpoints.

![2024-02-07_20-53.png](/images/2024-02-07_20-53.png)

Found nothing, just the image file. Feeling stuck.

### Exploitation

Since the name "Gaara" appeared, I tried using it to brute force the SSH server with the rockyou wordlist.

![2024-02-07_20-52.png](/images/2024-02-07_20-52.png)

Fortunately, I got a hit.

Logged in to the server and found the first flag in Gaara's home directory:
![2024-02-07_21-14.png](/images/2024-02-07_21-14.png)

### Privilege Escalation

After uploading LinPEAS and executing it, I found a binary, `/usr/bin/gdb`.

![2024-02-07_21-42.png](/images/2024-02-07_21-42.png)

Checked GTFObins and found a technique to exploit the SUID bit for privilege escalation.

![2024-02-07_21-45.png](/images/2024-02-07_21-45.png)

The binary's full path needed to be specified.

![2024-02-07_21-47.png](/images/2024-02-07_21-47.png)

Gained root privileges! The EUID is set to 0 (root). Retrieved the last flag in the root directory:
![2024-02-07_21-49.png](/images/2024-02-07_21-49.png)

Last flag captured.

---

This box was quite easy and straightforward.

**End!**

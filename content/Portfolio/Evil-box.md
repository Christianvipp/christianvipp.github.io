+++
title = "Evil-box"
date = 2024-10-14T16:25:52-04:00
draft = false
+++


## Platform : Proving Grounds  
**Level**: Easy

### Reconnaissance:

A rustscan as usual to find open ports, 22 and 80 opened.  
![Scan result](/images/2023-10-31_21-45.png)

### Scanning:

Performed an nmap scan to find version information on the open ports and operating system identification using the aggressive nmap flag.  
![Nmap scan](/images/2023-10-31_21-46.png)

An Apache webserver is hosted on port 80, and SSH is running on port 22 as usual.

A quick visit to the website shows a default Apache webserver page.  
![Default Apache page](/images/2023-10-31_23-43.png)

I fuzzed for hidden directories and found a secret directory, which contained a file called `evil.php`.  
![Fuzzing result](/images/2023-10-31_22-18.png)

Visiting the secret directory had no content, and `evil.php` was also empty, but it seemed like a good candidate for fuzzing. I initially thought of using `wfuzz`, but had issues installing it due to time constraints. So I used BurpSuite's intruder tool, which allowed me to fuzz two parameters using the "clustering bomb" payload.  
![BurpSuite intruder](/images/2023-10-31_22-43.png)

After starting the attack and analyzing the results, I noticed a difference in response length. It was a hit! The first parameter was vulnerable to Local File Inclusion (LFI).  
![LFI exploit](/images/2023-10-31_22-44.png)

I was able to view the `/etc/passwd` file.  
![passwd file](/images/2023-10-31_23-08.png)

### Exploitation:

I initially thought of trying SSH log poisoning or brute-forcing SSH, but neither worked. However, I was able to read the `id_rsa` file of the user `mowree` and copied it to my attacker machine.  
![id_rsa found](/images/2023-10-31_23-11.png)

Unfortunately, the `id_rsa` file was passphrase-protected. To crack the passphrase, I used `ssh2john` to convert the RSA file into a hash that John the Ripper could process.  
![ssh2john](/images/2023-10-31_23-13.png)

After running John the Ripper, I successfully cracked the passphrase.  
![John the Ripper cracked the passphrase](/images/2023-10-31_23-13_1.png)

I was then able to connect to the target via SSH.  
![SSH connection](/images/2023-10-31_23-14.png)

Once inside, I found the first flag in the user's directory.

### Privilege Escalation:

As time was limited, I transferred the `linpeas` script to the target for automated enumeration. Upon reviewing the results, I noticed that the `passwd` file was writable—indicating a serious misconfiguration.  
I followed a guide on how to exploit a writable `passwd` file, generated a new password using `openssl`, and added it to the file to create a fake root user.  
![Privilege escalation](/images/2023-10-31_23-24.png)

Switching to the new root user worked, and I successfully got the root flag.

### Conclusion:

Got the root flag, and that's it. Thank you, hackers! Until next time, stay burped!

**Vulnerabilities used**: LFI, writable `passwd` file.

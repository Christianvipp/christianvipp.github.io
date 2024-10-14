+++
title = "Blogger"
date = 2024-10-14T16:25:52-04:00
draft = false
tags = ["CMS enumeration", "file upload bypass", "vertical privilege escalation"]
+++


Platform: Proving Grounds  
Level: Easy 

### Recon:
A rustscan as usual!  
![Rustscan result](/images/2023-10-14_18-04_1.png)

Two open ports 22 and 80, by default, we know that is SSH and HTTP.

### Scanning:  
Let's go ahead and scan those ports to know which services run on them and their versions.  
![Nmap result](/images/2023-10-14_18-04_2.png)

SSH and HTTP with their respective versions, and we can deduce the OS is Linux.

### Enumeration:
I ran a curl command to the webserver, hoping to get some information from the headers. Visiting the webpage shows a portfolio:  
![Portfolio webpage](/images/2023-10-14_18-06.png)

I fuzzed for hidden directories and found a few: `/assets`, `/images`, `/css`, `/js`. Visiting `/assets`, there were more directories. Going to `/fonts/blog`, there was a strange redirection and a change in the hostname:  
![Hostname change](/images/2023-10-14_18-19.png)

It looks like a WordPress site, so I added the hostname to my hosts file:  
![Hosts file change](/images/2023-10-14_18-20.png)

A quick look at Wappalyzer showed that it's running an old version of WordPress:  
![Wappalyzer result](/images/2023-10-14_18-21.png)

### Scanning with WPScan:
I used WPScan to scan the site. WPScan is a powerful CMS scanner specifically for WordPress, with features like user enumeration, plugin detection, and theme detection.

Running an aggressive plugin detection scan revealed a vulnerable plugin:  
![WPScan plugin detection](/images/2023-10-14_18-59.png)

### Gaining Access/Foothold:
After a quick Google search, I discovered the plugin is vulnerable to arbitrary file upload. It has a public exploit and a Metasploit module, but the Metasploit exploit didn't work for me:  
![Metasploit failure](/images/2023-10-14_19-14.png)

I decided to exploit it manually.

On a blog post, there's an option to make a comment with an image upload functionality:  
![Comment with image upload](/images/2023-10-14_19-16.png)

Trying to upload any file other than an image throws an error:  
![File upload error](/images/2023-10-14_19-18.png)

After several attempts, I was able to bypass the filter using file headers. The server checks files via mechanisms like file extensions and MIME types, but I was able to trick it by injecting a GIF file type header into a reverse shell script from PentestMonkey:  
![Reverse shell uploaded](/images/2023-10-14_19-19.png)

I filled out the other form fields and submitted the comment:  
![Form submission](/images/2023-10-14_19-23.png)

Meanwhile, I set up a netcat listener, and once the comment was posted, I received a reverse shell:  
![Reverse shell received](/images/2023-10-14_19-23_1.png)

We now have a shell as `www-data`. Let's find some flags. I navigated to the user `james` and found the first flag:  
![First flag found](/images/2023-10-14_19-38.png)

### Privilege Escalation:
Attempting to access other users gave a "Permission denied" error, so it's time for privilege escalation.

After some enumeration, I found that the user `vagrant` is also present.  
![Vagrant user found](/images/2023-10-14_19-31.png)

I continued manual enumeration and discovered that I could escalate privileges to `vagrant` since this user has permissions to run all commands without a password:  
![Privilege escalation to vagrant](/images/2023-10-14_19-35.png)

Finally, I gained root access and captured the flag!  
Great box.

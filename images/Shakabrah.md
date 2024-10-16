Platform : PG
Level : Easy

Reconnaissance :

A simple rustscan to find open ports on target.![[2023-10-22_08-43.png]]

Scanning :

Then proceeds to scan those ports for running services and version identification using nmap. ![[2023-10-22_08-44.png]]

Enumeration : 

Visit the website, it has a functionality to ping ips. ![[2023-10-22_08-44_1.png]]

i will proceed to ping the localhost what happens is that it tries to make a  ping request to the specified ip if correct and the output are the ping responses with 4 counts![[2023-10-22_08-44_2.png]]

Foothold :

Nice, we can test for different potentials vulnerability, but it seems it more potentially vulnerable to command injection. let's test. shall we?

we will ping the localhost and execute another system command (whoami) alongside the ip. ![[2023-10-22_08-45.png]]

command : 127.0.0.1;whoami

![[2023-10-22_08-46.png]]

With the ping responses was also the output of the whoami command, command injection spotted. we should be able to execute a reverse shell then. 

let's find one from https://rev.shells.com  ![[2023-10-22_08-47.png]]

please note, it seems like there was a firewall on the target that drops all incoming or outgoing connections from any port apart from port 80, so after few trials, i figured it was port 80. Setup your netcat listener on port 80 and execute the command. ![[2023-10-22_08-47_1.png]]

I got a reverse shell, found the first flag at user dylan home's directory. 
![[2023-10-22_08-50.png]]

time to find the other.  

Privlege escalation :

After few mins of manual enumeration, searched for suid bit set to them with the user root, found quite number of them and one was distinctive. ![[2023-10-22_10-23.png]]

Let's check gtfobins which is a great resource to find how to exploit binaries in certain ways and techniques, our goal is to escalate privilege vertical to root. so let's find what suits us best. ![[2023-10-22_10-48.png]]

Got one but few issues with it. i will advise you follow the following steps as i did so you can get root. 

steps
1. Run /usr/bin/vim.basic
2. run :py3 and the highlighted command above in blue.

you might get stucked while the program is running, you have to quit out of vim.
worked for me tho ;)

![[2023-10-22_10-48_1.png]]

i got root, navigated to the root's directory, got the last flag!

Adios hackers. 
command Injection. 

+++
title = "Pyrat"
date = 2024-11-11T06:01:49
draft = false
+++

recon :

rustscan to find open ports. ![2024-11-11_01-01.png](/images/2024-11-11_01-01.png)

2 opened ports.. 

scanning :

nmap scan to identify services and versions.. 
![2024-11-11_01-06.png](/images/2024-11-11_01-06.png)

ssh and HTTP server running simple http python server.. 

Enumeration : 

Visit the web server running on port 8000

![2024-11-11_01-11.png](/images/2024-11-11_01-11.png)

Try fuzzing, nothing

checking with burp, the simple http server version, made some research on it and realized there was a github convo based on it.. 
![2024-11-11_01-57.png](/images/2024-11-11_01-57.png)


saw a poc and tried to recreate it on my own end to understand the attack, seemed like i was confident with that route but did not work. 

![2024-11-11_02-00.png](/images/2024-11-11_02-00.png)

couldnt write to that directory cause it is a directory, i tried to retrieve a file from the ssh directory from my end.. (in this case known_host) which worked well and i was able to read the content, also tried to move out of the ssh directory and download file![2024-11-11_02-01.png](/images/2024-11-11_02-01.png)
which worked well as well 

since a ssh server is also up, maybe i could try to pull id_rsa or some stuff, it works but the file content only is 'try a basic connection' 

![2024-11-11_02-08.png](/images/2024-11-11_02-08.png)

quite frustrating, peeped a writeup and had another method, ditched that since it did nt work, if anyone knew if i made a mistake could try to reach out to me on X and tell me, it would mean alot.. 

From the writeup have to connect to the port via netcat and inject a python reverse shell excluding the python suffix. 

![2024-11-11_03-08.png](/images/2024-11-11_03-08.png)

setup a listener
![2024-11-11_03-09.png](/images/2024-11-11_03-09.png)

a shell is called back. 

uploaded linpeas to the target and got a /dev in /opt dir.

![2024-11-11_03-19.png](/images/2024-11-11_03-19.png)

Digging through reveals a hidden folder, the config file stood out, which actually contained the user credentials. 

![2024-11-11_03-22.png](/images/2024-11-11_03-22.png)

Persistence : 

login with ssh to get a more stable shell.. ![2024-11-11_03-33.png](/images/2024-11-11_03-33.png)

go for the first user text file.

![2024-11-11_03-36.png](/images/2024-11-11_03-36.png)

Privilege escalation : 

checking the current status of the .git folder, a file has been deleted.. 

![2024-11-11_03-54.png](/images/2024-11-11_03-54.png)

running `git log`  there is a commit added, ![2024-11-11_04-02.png](/images/2024-11-11_04-02.png)

using `git show commitname` there is a snippet of the switch_case which basically the switchcase function process some data based on conditions  i.e `if data` is some_endpoint then it calls get_this_endpoint if not then `if data` is shell then it calls exec_python function and drops a shell.

Testing that thoery.. 

![2024-11-11_04-15.png](/images/2024-11-11_04-15.png)

typing `some_endpoints` its not defined.. ![2024-11-11_04-15_1.png](/images/2024-11-11_04-15_1.png)

Fuzz with a custom script as mentioned in the room description.. 
![2024-11-11_04-23.png](/images/2024-11-11_04-23.png)

got a hit on `admin` . 

![2024-11-11_05-29.png](/images/2024-11-11_05-29.png)


Using admin as input.. 
![2024-11-11_05-32.png](/images/2024-11-11_05-32.png)

bruteforcing for password too.. 

modifying same script..

![2024-11-11_05-47.png](/images/2024-11-11_05-47.png)

after getting the right password, got logged as admin and typed shell automatically got drop to a root shell..

thanks. 

![[2024-02-07_20-27.png]]

The target is active and responding to the icmp ping request. 

Recon : 

A quick rust scan to find the open ports on the targets .
![[2024-02-07_20-34.png]]

There are 2 open ports 22,80 which by default are ssh and http. 

Scanning : 
Would run an nmap scan to confirm and also identify the versions of those opened services. ![[2024-02-07_20-32.png]]

Yes, ssh and http, from the banners(Debian), could tell it is a linux server. 

Enumeration : 

Starting enumeration with the web server running on port 80. 

Visiting the website, ![[2024-02-07_20-39.png]]

An image of a cartoon or anime character perhaps and an email below. 
Viewed the source code too and nothing really.

None of these interests me, would proceed to fuzz for hidden endpoints.

![[2024-02-07_20-53.png]]

also nothing, just the image file. 

quite stuck! 

Exploitation : 

since there is a name Gaara, i  thought of using it to bruteforce the ssh server using the rockyou wordlists.  

![[2024-02-07_20-52.png]]

Fortunately, got a hit. 

Logged in to the server and in the user gaara home directory, 
![[2024-02-07_21-14.png]]

there is the 1st flag.  

![[2024-02-07_21-28.png]]

Further enumeration to escalate privilege to the root user.

After uploading linpeas to the target and executed, there was a binary lurking around, /usr/bin/gdb. 

![[2024-02-07_21-42.png]]

Checked gtfobins and got a potential technique to exxploit the suid bit to escalate privileges. 

![[2024-02-07_21-45.png]]
the binary's full path needs to be specified. 


![[2024-02-07_21-47.png]]

and right there is the root privilege, the current user has the euid set to 0 which is root. Now, could get the last flag in the root user directory. ![[2024-02-07_21-49.png]]

Last flag captured. 


This box was quite easy and straightforward...

End! 
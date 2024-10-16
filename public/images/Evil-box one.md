Platform : Proving Grounds
Level: 

Reconnaissance : A rustscan as usual to find open ports, 22 and 80 opened.![[2023-10-31_21-45.png]]

Scanning : Performed an nmap scan to find version information on the open ports and operating systrm identification using the aggressive nmap flag.
![[2023-10-31_21-46.png]]

Well, an apache webserver is been hosted on 80 and 22 running ssh and usual.

A quick visit to the website shows a default apache web-server page. ![[2023-10-31_23-43.png]]

well, i will fuzz for hidden directory and got a secret directory and in the secret directory is a file called evil.php. hmmm.![[2023-10-31_22-18.png]]

Visiting the secret directory had no content in it same as evil.php, but sounds like we could fuzz it. wfuzz came to mind but had issues installing it and time wasn't on my side as i have just 2 hours. Burpsuite told me not to panick that he got everything under control, so intercepted the request, send to intruder and used the clustering bomb payload since there were 2 parameters i was fuzzing for. ![[2023-10-31_22-43.png]]

Started the attack and enumerating, i noticed a difference in the length response, seem like a hit, was it? it was, i had command for the first parameter. 
![[2023-10-31_22-44.png]]
and it was vulnerable to Local file Inclusion, i could view the /etc/passwd file. 
![[2023-10-31_23-08.png]]

which is a normal file in linux systems where users  sensitive information are on the system. 

Exploitation :

Well, 2 things came to mind first, apache and ssh log poisoning  i even tried bruteforcing ssh, but didn't work me.  i was able to read the id_rsa file of the user `mowree` and copy it to a file, gave it the necessary permissions and here came the issue.![[2023-10-31_23-11.png]]

it was a passphrase protected id_rsa file. guess who we could send an invitation, one of john's kids. ssh2john. 

i used ssh2john to change the id_rsa file content to a hash that john can understand and saved it in an output file called hash.txt![[2023-10-31_23-13.png]]
Ok, john can understand this and with instruction can help bruteforce the passphrase. After letting john do it's thing. it has the passphrase used

![[2023-10-31_23-13_1.png]]

Hopefully, i can now safely connect to the target via ssh. ![[2023-10-31_23-14.png]]

We are in and we got the first flag in the user's directory. There were no other user on the target, so it's time to escalate to root.

Privilege Ecalation :
As stated earlier, didn't have enough time, i transffered linpeas to the target, an automated enumeration script on linux systems. 

While checking the result, i saw that the passwd file was writable, well great news. a misconfiguration. we can now safely test that route to escalate privilege. i followed a blog that explained how it is vulnerable and dangerous to make the passwd file writable on a linux system. I used openssl to generate a new password and added the hash to the passwd placholder and created an identical root user with similar necessary information. i proceeded to switch to the fake root and it worked successfully.![[2023-10-31_23-24.png]]

Got the root flag and that's it. thank you hackers! 
till next timr. stay burped :/

LFI, writable passwd file

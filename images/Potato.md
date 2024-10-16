
platform : Proving Grounds
level : easy 

Recon : i will perform a quick rust-scan to see the available open ports.
![[2023-08-19_19-19.png]]
There are three (3) open ports in running on the target, let's enumerate further to understand what services are running on the target ports and their and versions

Scanning & Enumeration :
i will also run an nmap scan for further enumeration.![[2023-08-19_19-21.png]]
The scan result came back and we have ssh , http , ftp running on port 2112, and we can see the ftp server contains some files. might help us. let's take a dive, shall we?

FTP :
i will login to the ftp server, since the server allows anonymous login and i will also specify the port number since ftp doesnt run on it default port, the creds are anonymous/anonymous. ![[2023-08-19_19-24.png]]
let's list the contents in the server since we saw there was some files in the server from our nmap scan result.![[2023-08-19_19-27.png]]
i will download everything in my local machine using the `mget *` command, then i will view the file content.![[2023-08-19_19-29.png]]
The welcome.msg file doesn't really gives us any valuable information, let's move on to the next, the index.php.bak file is a html document, concatenating the content shows a php login script that once we enter the correct creds, we login in and it takes us to the dashboard else it prints a error message, looking at the script we see we have a username  `admin`  which shows admin is a valid user and we have a password potato which is in the $pass variable, and then the actually login form. let's continue with our enumeration, that information might help us somewhere.

HTTP: Navigating to the website, we have a static page with the Title `Potato Company. ` ![[2023-08-19_19-30.png]]

i will perform a directory bruteforce incase there are any hidden directories

![[2023-08-19_19-40.png]]

ooooh, result came back and it looks like we have 1 hidden directory 
`admin`  Navigating to the directory shows this simple login form.


![[2023-08-19_19-41.png]]

let's try default creds which is `admin/admin` which gave an error bad user, we see some familiarity with the form action and the index.php.bak we came across earlier.![[spaces_-MFlgUPYI8q83vG2IJpI_uploads_git-blob-606ec3161be6b892cfe9a8dccf020d926b6dff7f_image.png]]

![[2023-08-20_09-56.png]]

We know that from the code the admin name exists and that the password is changed regularly base on the comment from the php script . Going with this we can try the _strcmp_ bypass on the password value.

Authentication bypass
i will  use burpsuite for this so i can intercept traffic.
![[2023-08-19_19-48.png]]

And then, i will set the password value to `[]==""`


![[2023-08-19_19-51.png]]

Nice, we are in, let's go back to enumeration, ![[2023-08-19_19-54.png]]

While checking around, in the logs section, ![[2023-08-19_19-57.png]]

i will test if the server validates user's input, i will try to move out of webroot's directory, i will try to read the passwd file
![[2023-08-19_19-58.png]]

Great, it vulnerable to path transversal, there is a user on the machine, `webadmin` and we have the user's hash.

![[2023-08-19_20-21.png]]

Cracking time, let's save in a file, then we will john to crack, i will use the rockyou file as wordlist.

john -w=/usr/share/wordlists/rockyou.txt hashfile

![[2023-08-19_21-37.png]]
Exploitation :
booom, we have plaintext creds, let's use this to login to ssh.

![[2023-08-19_21-36.png]]

Now in the box, In search of our flags. let's list the content of the user's directory![[2023-08-19_21-38.png]]

There are few files in the directory, including our flag. On to the last flag.

Privilege Escalation :

since we have creds for the user, let's see if we have any sort of admin/root privilege to execute any commands with sudo. 
![[2023-08-19_21-46.png]]
Cool, i tried the gtfobins exploit but doesn't work. After few searches, i found another and created a file called ` comrade.sh`     echo'ed /bin/bash to the file and gave full permissions, then executed it. which gave a root bash shell. Navigated to the root directory and get the flag. 

Thanks for reading, happy hacking folks, till another time. Adios

strump, auth bypass , path traversal.
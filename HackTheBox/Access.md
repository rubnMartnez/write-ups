# Access

This is my write-up for the machine **Access** on Hack The Box located at: https://app.hackthebox.com/machines/156

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/Access/nmapScan.png)

Since ftp is open and anonymous login is allowed, I tried it first, but it was not possible to get any information out of it

![ftpEnum](./res/Access/ftpEnum.png)

So I run some nmap scripts, but they didn't get any information either

![nmapFTPscripts](./res/Access/nmapFTPscripts.png)

With that in mind I moved to telnet, but it was more of the same

![telnet](./res/Access/telnet.png)

So I went to the last port open to enumerate, which was port 80, and the default page shows the following image of some servers

![defaultPage](./res/Access/defaultPage.png)

Since there wasn't any other links to click or subdirectories I run gobuster, but it didn't show anything either

![gobusterReport](./res/Access/gobusterReport.png)

So I run some nmap scripts against it ot check if there was any vulnerabilities, but it doesn't seem to be the case

![nmapHTTPscripts](./res/Access/nmapHTTPscripts.png)

The nikto scan didn't found anything either

![nikto](./res/Access/nikto.png)

I also tried to do a POST, but it isn't allowed

![POST](./res/Access/POST.png)

After trying to enumerate port 80 without succes, I went back to FTP, to see if I was able to enumerate it furter, but since I was gettingt the passive error all the time I run wireshark, to check what was going on more in depth, and the conclusion was the same

![wiresharkWithFTP](./res/Access/wiresharkWithFTP.png)

So I googled which firewall was used on kali, and I added a rule to accept the incoming traffic from the box

![addIptablesRule](./res/Access/addIptablesRule.png)
![checkIptablesRule](./res/Access/checkIptablesRule.png)

But it didn't work either, so I decided to check the write-up to check what I was missing, and they used ufw, but it didn't work for me, so I search for other write-ups online, and one guy used wget with no passive mode, which actually worked for me

![wgetFTP](./res/Access/wgetFTP.png)

So after that I changed the approach slightly and I started searching for how to disable the passive mode, and after running those commands it finally worked

![passiveFTP](./res/Access/passiveFTP.png)

With that said, I went ahead to enumerate the files that we pulled from ftp

![ftpFiles](./res/Access/ftpFiles.png)

It seems the the only file the we are able to access is the access DB, so I checked all the tables available and some of them seems to be pretty interesting

![mdbTables](./res/Access/mdbTables.png)

After navigating through the tables, I found that there's sensitive info inside auth_user

![userCreds](./res/Access/userCreds.png)

With that I tried to login on telnet, but it seems that the credentials aren't from there

![telnetLoginAttempts](./res/Access/telnetLoginAttempts.png)

So since the zip is encrypted, I tried with the credentials there, and it worked

![unzip](./res/Access/unzip.png)

After checking the contents of it, we could the that there's a message a password change to security:4Cc3ssC0ntr0ller

![readpst](./res/Access/readpst.png)

## Exploitation

And if we try those credentials on telnet, we get a shell

![gettingTelnet](./res/Access/gettingTelnet.png)

## Post Exploitation

So I proceed to do some basic enumeration, first with systeminfo

![systeminfo](./res/Access/systeminfo.png)

Then with netstat to check which ports are open

![netstat](./res/Access/netstat.png)

And I continued by enumerating the users, groups and privileges

![netuser](./res/Access/netuser.png)
![whoamiPriv](./res/Access/whoamiPriv.png)
![whoamiGroups](./res/Access/whoamiGroups.png)
![netLocalGroup](./res/Access/netLocalGroup.png)

And I also got the user flag

![userFlag](./res/Access/userFlag.png)

After that I tried running the cmdkey command, which was recommended from the course that I'm doing on privilege escalation, and I got that the administrator credentials were stored

![cmdkey](./res/Access/cmdkey.png)

With that in mind, I fetched netcat from my machine and tried to run it with runas as suggested on the following [guide](https://swisskyrepo.github.io/InternalAllTheThings/redteam/escalation/windows-privilege-escalation/#eop-runas) but it didn't work

![fetchNetcat](./res/Access/fetchNetcat.png)

So after googling a little bit I found a command for runas that actually worked, so I went ahead and generated a meterpreter shell

![generateMeterpreterShell](./res/Access/generateMeterpreterShell.png)

I fetched it

![fetchShell](./res/Access/fetchShell.png)

And I ran it with the command that I was talking before

![runas](./res/Access/runas.png)

With that I got the shell back

![getMeterpreterShell](./res/Access/getMeterpreterShell.png)

And now the only thing left to do is get the root flag

![rootFlag](./res/Access/rootFlag.png)

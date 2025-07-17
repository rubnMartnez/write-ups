# Timelapse

This is my write-up for the machine **Timelapse** on Hack The Box located at: https://app.hackthebox.com/machines/452

## Enumeration

First I started with an [nmap scan](./res/Timelapse/10_10_11_152_nmapReport.txt), which shows the following

![nmapScan](./res/Timelapse/nmapScan.png)

After that I ran smbmap to check if I could pull some information about the shares, but it wasn't the case

![smbmap](./res/Timelapse/smbmap.png)

Then I ran enum4linux, which retrieved the domain name and some information about the target SO

![enum4linux](./res/Timelapse/enum4linux.png)

After that I did a dig, which didn't tell much apart from the hostname

![dig](./res/Timelapse/dig.png)

I also did an ldap search, but nothing came through either

![ldapsearch](./res/Timelapse/ldapsearch.png)

So I tried with GetNPUsers script, but it didn't work either

![GetNPUsers](./res/Timelapse/GetNPUsers.png)

After that I decided to change the approach and start enumerating each port deeper, I started with smb, and I got the shares with smbclient

![shares](./res/Timelapse/shares.png)

I tried to connect to "Shares" share and since they seemed interesting, I got all the files that were there

![shareFiles](./res/Timelapse/shareFiles.png)

Before start reading the documents I wanted to unzip the zip to see what's inside and prioritize the enumeration, but it seems that it is encrypted

![zipProtected](./res/Timelapse/zipProtected.png)

## Exploitation

So I did a quick google search and I found [this blog](https://medium.com/@rundcodehero/cracking-a-password-protected-zip-file-with-john-the-ripper-a-hands-on-guide-1aea0f6b3627) that explained how to get the zip hash and crack it with john the ripper and the password was **supremelegacy**

![zipCrack](./res/Timelapse/zipCrack.png)

After that, I tried to open the pfx file, but it was encrypted as well

![pfxEncrypted](./res/Timelapse/pfxEncrypted.png)

But it was possible to follow the same methodology as before in order to obtain the password, which was **thuglegacy**

![pfxCracked](./res/Timelapse/pfxCracked.png)

With that I was able to open the file, which seems to be a certificate

![pfxFile](./res/Timelapse/pfxFile.png)

Since I didn't know what to do with it, I went to the HTB guided mode for a hint, which was to use winrm, so I googled how to do that, and after extracting the key and the cert from the pfx file, I was able to pass them to winRM and get a shell

![shell](./res/Timelapse/shell.png)

## Post Exploitation

Now that I had a shell, I started the enumeration, first by checking the users and groups that were available

![usersAndGroups](./res/Timelapse/usersAndGroups.png)

Then I navigated through the directories a little bit to see if there was something interesting, and I retrieved the user flag along the way

![userFlag](./res/Timelapse/userFlag.png)

After that I tried to run winPEAS, but apparently the AV was blocking it

![winPEAS](./res/Timelapse/winPEAS.png)

So I continued the enumeration manually, by pulling the local open ports with netstat

![netstat](./res/Timelapse/netstat.png)

Along with the ipconfig

![ipconfig](./res/Timelapse/ipconfig.png)

Since I wasn't getting anything interesting from there, I decided to run sharphound to retrieve domain information

![sharphound](./res/Timelapse/sharphound.png)

Then I uploaded it on bloodhound, and I pulled all domain users

![domainUsers](./res/Timelapse/domainUsers.png)

After that I made a query to get to domain admin, which was to use DCSync

![pathToDomainAdmin](./res/Timelapse/pathToDomainAdmin.png)

Since I needed mimikatz for this, I tried to get a meterpreter shell in order to do it more comfortably, but it didn't work

![msfFail](./res/Timelapse/msfFail.png)

After that I tried invoking mimikatz, but it was also blocked

![invokeMimikatz](./res/Timelapse/invokeMimikatz.png)

So I tried downloading the exe and uploading it, but it was also blocked

![mimikatzBlocked](./res/Timelapse/mimikatzBlocked.png)

That made me search for alternatives, and there's where I found certipy, so I went ahead and install it

![installCertipy](./res/Timelapse/installCertipy.png)

But after reading their wiki and make it run, it didn't seem to work either

![certipy](./res/Timelapse/certipy.png)

So I went to HTB guided mode for a hint, which was to check the powershell history and a link to [this page](https://0xdf.gitlab.io/2018/11/08/powershell-history-file.html), with that I was able to find the history location

![historyPath](./res/Timelapse/historyPath.png)

And once there I saw that there was the credentials for the service account, which were **svc_deploy:E3R$Q62^12p7PLlC%KWaxuaV**

![history](./res/Timelapse/history.png)

But then I tried to login into that new account and I got an error

![svcFailedLogin](./res/Timelapse/svcFailedLogin.png)

So I got back for another hint, which was to check the groups of that user, there we could see that this user was member of the LAPS_READERS group

![groupsOfSvcDeploy](./res/Timelapse/groupsOfSvcDeploy.png)

After a google search I found [this post](https://swisskyrepo.github.io/InternalAllTheThings/active-directory/pwd-read-laps/#reading-laps-password) where it explains how to pull the laps password for administrator, which was **administrator:Y(40DbZs6689%VNaxL27/5Cs**

![bloodyAD](./res/Timelapse/bloodyAD.png)

With that I was able to get an elevated shell

![elevatedShell](./res/Timelapse/elevatedShell.png)

And the only thing left to do was to retrieve the root flag

![rootFlag](./res/Timelapse/rootFlag.png)

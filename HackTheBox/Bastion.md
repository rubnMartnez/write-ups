# Bastion

This is my write-up for the machine **Bastion** on Hack The Box located at: https://app.hackthebox.com/machines/186

## Enumeration

First I started with an [nmap scan](./res/Bastion/10_10_10_134_nmapReport.txt), which shows the following

![nmapScan](./res/Bastion/nmapScan.png)

Considering the ports that are open, I decided to start the enumeration on smb, using smbmap, but as usual it didn't get us anything

![smbmap](./res/Bastion/smbmap.png)

So I used smbclient to verify that we were able to list the shares, and then cme to get more info out of them

![shares](./res/Bastion/shares.png)

After that I ran enum4linux, which didn't tell much a part from the DNS, the rpc login and that the smb signing is not required, which we already knew from the nmap scan

![enum4linux](./res/Bastion/enum4linux.png)

Then I proceed to get into the backups share the one that we have access, and there was some interesting files, like note and WindowsImageBackup, so I downloaded everything to explore it more comfortably on my VM

![backupFile](./res/Bastion/backupFile.png)

Since it was taking a lot of time to download, I went to read the note.txt meanwhile, where I saw that there was recommended to not download the backup file

![note](./res/Bastion/note.png)

So, after navigating around the share, I saw that everything but the backup and the note were empty. But checking the backup files we could assume that **L4mpje** is a valid username, despite that, we are not able to recover the backup files yet, cause we miss the identifier, so we probably need to get a shell before that

![smbclient](./res/Bastion/smbclient.png)

With that said, I proceed to download manually all the files that I found interesting and not too heavy

![manualDownload](./res/Bastion/manualDownload.png)

After exploring the files a little bit, I saw that grep wasn't working as expected, so after some googling, I saw that I had to convert them in order to be able to use grep properly

![convertedFile](./res/Bastion/convertedFile.png)

So I asked chatGPT for a script to convert all of them, so I could grep them properly, but I didn't find anything intersting

![convertedFile](./res/Bastion/convertFiles.png)

Then I fired up responder and put a malicious file in the share to see if it triggers a challenge, but it didn't

![iniScf](./res/Bastion/iniScf.png)

Since we had writing permissions on the backup share, I tried running psexec, but I got an error

![psexecFail](./res/Bastion/psexecFail.png)

So before enumerating smb further I explored the other ports first, starting for rpc, where I got nothing

![rpcclient](./res/Bastion/rpcclient.png)

Then I used nmap scripts to enumerate smb further, first by checking the protocols

![smbProtocols](./res/Bastion/smbProtocols.png)

After that checking the shares info and the os discovery

![smbOsDiscovery](./res/Bastion/smbOsDiscovery.png)

And lastly checking for eternal blue, just in case

![eternalBlue](./res/Bastion/eternalBlue.png)

Since I wasn't getting anything interesting from smb, I tried to dump information with rpc, but nothing interesting came through either

![rpcDump](./res/Bastion/rpcDump.png)

## Exploitation

I was stuck, so I decided to check the write-up, which suggested to use a windows VM to get into the share and open the vhd files with 7zip, since I didn't want to get a windows VM I tried to mount the share on my kali machine

![mountShare](./res/Bastion/mountShare.png)

And since I wasn't able to open the files with 7zip as they did, I googled an alternative, which was extract the whole vhd to another directory with 7z

![extractVhd](./res/Bastion/extractVhd.png)

Then all I had to do was navigate there and use secretsdump with sam and system to get the hashes

![hashes](./res/Bastion/hashes.png)

But when I tried to get a shell with winRM I got an error

![evilWinRM](./res/Bastion/evilWinRM.png)

So I had to crack the hashes in order to use them in ssh, and unfortunately the administrator was empty, so the only valid credentials we have are **L4mpje:bureaulampje**

![hashesCracked](./res/Bastion/hashesCracked.png)

With that I was finally able to get a shell via ssh

![shell](./res/Bastion/shell.png)

## Post Exploitation

First I navigated around a little bit to see if there was something that stood out, and I grabbed the user flag along the way

![userFlag](./res/Bastion/userFlag.png)

Then I tried to pull the system info, but the access was denied, so I pulled the user info

![whoami](./res/Bastion/whoami.png)

And I also checked the PS history, but apparently there were only my commands

![PShistory](./res/Bastion/PShistory.png)

After that I tried to upload winPEAS and PowerUp, but they were blocked by the AV

![winPEASfail](./res/Bastion/winPEASfail.png)

Then I tried getting winPEAS with curl, and it actually worked, it was kind of sketchy, cause it got a lot of permission denieds, but at least it worked, unfortunately there wasn't any useful information, a part from one script that contained the user and password of L4mpje, which we already knew

![winPEAS](./res/Bastion/winPEAS.png)

So I ran powerup, which displayed a potential dll hijack

![powerUp](./res/Bastion/powerUp.png)

After that, I asked chatgpt for a script to detect the process that could be using this dll

![script](./res/Bastion/script.png)

But after running it, nothing was found, so I tried with another dll which was more common, and that one was found, which means our dll is not used, or it is only used by a process that requires admin rights, so we are not able to read it

![dllSearch](./res/Bastion/dllSearch.png)

So I googled a little bit, and I found a tool from Microsoft called [ListDLLs](https://learn.microsoft.com/en-us/sysinternals/downloads/listdlls) that should work better than our script, but after running it I didn't get any output either

![listDlls](./res/Bastion/listDlls.png)

Since I was stuck, I checked the HTB guided mode for a hint, which was to check what was installed at Program Files, where I found a program called mRemoteNG

![programFiles](./res/Bastion/programFiles.png)

Then I checked the readme, where there was an explanation of what mRemote was about

![readme](./res/Bastion/readme.png)

With that information, I went to google to check where does mRemote store the password, which apparently was in a file called confCons.xml found inside AppData, so I checked the file, where I found the encrypted password for administrator and our current user

![confCons](./res/Bastion/confCons.png)

Since I saw on the xml that the encryption was AES, I tried to decrypt the password with cyberChef, but I got errors all the time

![cyberChef](./res/Bastion/cyberChef.png)

So I googled how to decrypt the confCons.xml, and I found [this tool](https://github.com/gquere/mRemoteNG_password_decrypt), so I cloned it and after running I got nothing, I guess it was a problem with the way I've formatted the xml

![passDecryptFail](./res/Bastion/passDecryptFail.png)

Then I downloaded another tool, but I still got an error

![passDecryptFail2](./res/Bastion/passDecryptFail2.png)

So I thought that probably it was a problem of the format, so I changed it, and rerun the first tool, then I finally got the admin credentials, which were **Administrator:thXLHM96BeKL0ER2**

![passDecrypt](./res/Bastion/passDecrypt.png)

Then all I had to do was get an ssh session with those credentials

![elevatedShell](./res/Bastion/elevatedShell.png)

And fetch the root flag

![rootFlag](./res/Bastion/rootFlag.png)

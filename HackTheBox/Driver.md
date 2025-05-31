# Driver

This is my write-up for the machine **Driver** on Hack The Box located at: https://app.hackthebox.com/machines/387

## Enumeration

First I started with an nmap scan, which shows the following

![nmapScan](./res/Driver/nmapScan.png)

Since port 80 is open, I navigated there first to see what are we up against, and it asks for authentication right away

![defaultPage](./res/Driver/defaultPage.png)

I tried admin:admin and it let me through

![pageLoggedIn](./res/Driver/pageLoggedIn.png)

So I ran gobuster with those creds but it didn't seem to find anything

![gobusterReport](./res/Driver/gobusterReport.png)

I also checked the headers

![headers](./res/Driver/headers.png)

Along with wappalyzer

![wap](./res/Driver/wap.png)

While I was navigating around I found this page, that could be really interesting, because it allow us to upload files, the problem is that we don't know where they end up

![upload](./res/Driver/upload.png)

I ran nikto as well and it only found the password that we already knew and the allowed methods

![nikto](./res/Driver/nikto.png)

I also checked the other http port, but nothing was found there

![port5985](./res/Driver/port5985.png)

So, before digging deeper into port 80, I decided to check smb, to see if I could enumerate some files or endpoints, I started running enum4linux, but it didn't find anything

![enum4linux](./res/Driver/enum4linux.png)

I also tried some manual enum, but nothing either

![smbManualEnum](./res/Driver/smbManualEnum.png)

So I tried running some nmap scripts to discover smb information and vulnerabilities, and it found some interesting things about smb singing and NTLM, but I'm not sure that would be useful on this environment

![smbNmapScripts](./res/Driver/smbNmapScripts.png)

## Exploitation

Since I was a little stuck I checked the guided mode from HTB for a hint, which was to look at smb share file attack, with that I found this [post](https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/) that talked about that, so I copied the payload and put it into a scf file, and I procced to upload it to the website

![smbNmapScripts](./res/Driver/uploadScf.png)

And with that I got the hash on responder, it is a curious exploit path, cause I'm not used to user interaction on CTFs, but there's that

![responder](./res/Driver/responder.png)

Then I tried to relay the hash, but it was not working, so I google it, and I found this command from crackmapexec where it seems that if singing is false the hash cannot be relayed

![smbrelayFail](./res/Driver/smbrelayFail.png)

So I went straight to hashcat to crack it, and the credentials where **tony:liltony**

![hashcat](./res/Driver/hashcat.png)

After that I tried to get a shell with psexec, but when I triggered the command I got a list of shares saying that they were not writable

![psexecFail](./res/Driver/psexecFail.png)

So I tried another commands to enumerate all the shares to see if there was any with writing permissions, but it doesn't seem to be the case

![shareEnum](./res/Driver/shareEnum.png)

Then I when to metasploit to try and connect with psexec, thinking that maybe it follows another process where it doesn't need to write any file, but it wasn't the case

![msfPsExecFail](./res/Driver/msfPsExecFail.png)

So I spent some time googling about another ways to get in, and eventually I came out with winrm, and with that I finally got a shell back

![winrm](./res/Driver/winrm.png)

## Post Exploitation

Once on the target shell, I procced to the basic enumeration, first I pulled the system and user information

![systeminfo](./res/Driver/systeminfo.png)

Then I pulled the network info

![netstat](./res/Driver/netstat.png)

I also grabbed the user flag

![userFlag](./res/Driver/userFlag.png)

And then I got a meterpreter shell in order to run the local exploit suggester, which showed the following

![localExploitSuggester](./res/Driver/localExploitSuggester.png)

I tried all of them and they didn't work, so I checked the write-up to see what was going on, and they said that considering that the website is about printers, it would be good to focus on those exploits, also that if we check the powershell history, it is possible to see that the driver RICOH PCL6 is being used, then it make sense to use the exploit with the same name, the problem is that when I used it, it didn't work

![ricohExploitFail](./res/Driver/ricohExploitFail.png)

The problem was that it is required to migrate the meterpreter process first in order to obtain one with the 1 set, which means that is interactive

![processMigration](./res/Driver/processMigration.png)

With that we can run the exploit and get the elevated shell

![elevatedShell](./res/Driver/elevatedShell.png)

And now we only have to retrieve the root flag

![rootFlag](./res/Driver/rootFlag.png)

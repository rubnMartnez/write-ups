# Heist

This is my write-up for the machine **Heist** on Hack The Box located at: https://app.hackthebox.com/machines/201

## Enumeration

First I started with an [nmap scan](./res/Heist/10_10_10_149_nmapReport.txt), which shows the following

![nmapScan](./res/Heist/nmapScan.png)

Since port 80 was open, I navigated there first to see what were we up against, which apparently is an IIS server, which presents a login page right away

![nmapScan](./res/Heist/defPage.png)

So I checked the tech stack real quick with wappalyzer

![wap](./res/Heist/wap.png)

Then I logged in as a guest, where I saw that there's an [attachment](./res/Heist/config.txt) with some configuration

![guest](./res/Heist/guest.png)

Which apparently contained some credentials

![configTxt](./res/Heist/configTxt.png)

So I googled how to decrypt those passwords, and I found and online tool that does it for us

![ciscoPassDecrypt](./res/Heist/ciscoPassDecrypt.png)

I also cracked the md5 hash that was there which leaves us with **stealth1agent**

![ciscoHash](./res/Heist/ciscoHash.png)

Now with that I ran gobuster to see if there was any other page that can give us information, but it didn't seem to be the case

![ciscoHash](./res/Heist/gob.png)

And I also ran nikto, which didn't provide much more information as well

![nikto](./res/Heist/nikto.png)

Then I went to check smb, starting with enum4linux, which didn't gave us any useful information, apart from the OS version

![enum4lin](./res/Heist/enum4lin.png)

And some smb information that we already knew from the first nmap scan

![smbInfo](./res/Heist/smbInfo.png)

So I tried to list the shares manually as a guest, but it didn't work

![guestShareListing](./res/Heist/guestShareListing.png)

Then I tried with the user hazard and all 3 password convinations, and the md5 one worked, so we have the following credentials **hazard:stealth1agent**

![hazardShareListing](./res/Heist/hazardShareListing.png)

After that I used crackmapexec to enumerate the shares further, which apparently we only have access to the IPC share and I also tried to enumerate the users, which wasn't possible

![cme](./res/Heist/cme.png)

So I tried to read the IPC share, which was available, but as expected no listing was possible, so I tried to get some more information with rpc, but apart from server information we couldn't take anything else

![rpc](./res/Heist/rpc.png)

I also tried to login with winrm just in case, but it didn't work either

![winrmHazardFail](./res/Heist/winrmHazardFail.png)

Since I was running out of options, I checked the write-up which explains that we can enumerate users with cme by bruteforcing the RIDs which stands for Relative Identifier and it's part of the SID and those are used to identify a user or service on a Windows host. So I ran the command suggested, and I got a list of users back

![ridBrute](./res/Heist/ridBrute.png)

## Exploitation

Now we are able to bruteforce those with cme, and we get a successful login with chase user `Chase:Q4)sJu\Y8qz*A3?d`

![chase](./res/Heist/chase.png)

And with those credentials we can finally get a shell via winrm

![winrm](./res/Heist/winrm.png)

## Post Exploitation

Then I went to the desktop to grab the user flag as usual

![userFlag](./res/Heist/userFlag.png)

And there I saw a todo list, which contained 2 tasks that could be interesting as a hint, cause it maybe a missconfiguration on the router config that let us escalate

![todo](./res/Heist/todo.png)

But before digging deeper into that, I wanted to do some basic enumeration as usual, starting with the groups, privileges and system information, which unfortunately the last one wasn't accessible

![privs](./res/Heist/privs.png)

Then I checked which users exists, which are the ones that we already knew, and which groups there were in

![netUsers](./res/Heist/netUsers.png)

I also checked the localgroups, and which users were in some of the interesting ones, but apparently it was only Administrator, despite that I'll probably run winpeas later just in case I've missed something

![localGroups](./res/Heist/localGroups.png)

After that I tried to check the powershell history, and the location was found

![psHistory](./res/Heist/psHistory.png)

But when I navigated to the directory nothing was there

![noHistory](./res/Heist/noHistory.png)

So I moved on to check the network information, starting with a netstat, which didn't show any port listening that we didn't already know about

![netstat](./res/Heist/netstat.png)

Then I checked the ipconfig, to see if there was something else there, since we knew that there could be some missconfigurations with the router and so on, but everything looked good

![ipconfig](./res/Heist/ipconfig.png)

I also decided to check the routing table to get as much information as possible as how the network is built

![route](./res/Heist/route.png)

And finally I pulled the firewall status

![fwStat](./res/Heist/fwStat.png)

As well as the firewall configuration

![fwConf](./res/Heist/fwConf.png)

I also ran winpeas to double check the information and see if I missed something, and it found an unattend file, but unfortunately the password was deleted

![unattend](./res/Heist/unattend.png)

After that I saw that it found a firefox DB on AppData\Roaming so I explore it, but the password was really cryptic, so I moved on

![firefoxDB](./res/Heist/firefoxDB.png)

It also found that lateral movement is possible with uac, but we already have "the best" low level user, so I'm not sure it is worth exploring

![uac](./res/Heist/uac.png)

With all that information, I started looking for files manually, either for router configs or where the issues page was, then I saw that there was a script called runphp.cmd that was copying some config files from iis folder

![runphp](./res/Heist/runphp.png)

But when I navigated there, there was no iis folder

![progFiles](./res/Heist/progFiles.png)

So I did a search for the issues.php file, but it wasn't anywhere either

![noIssues](./res/Heist/noIssues.png)

Then I googled where IIS gets installed, and they mentioned an xml called applicationHost.config which should be located under system32, but we had no access there

![inetsrvNotAccessible](./res/Heist/inetsrvNotAccessible.png)

So I searched for the file to see if it was somewhere else, which seemed to be the case, but when I opened it, it seemed corrupted

![findAppConf](./res/Heist/findAppConf.png)

And every folder I check that could contain useful information I get an access denied, so from my point of view right now, if chase has to check the issues and the router config, he has to have access to the IIS where those are, though on CLI he hasn't so either we find his email and access it through web (hopefully there's some useful info there) or we move to hazard user (since he should have acces there to get the files, that's why they've created the account on the first place) or someone else and access IIS from there. Since I wasn't being able to find the email, or access the IIS files, I decided to try and switch user to hazard, but it didn't work either.

![findAppConf](./res/Heist/suFail.png)

So I checked the write-up to see what I was missing, and according to it, the correct way to escalate here is to check the processes, to identify what was being used to read the issues.php, which in this case is firefox

![ps](./res/Heist/ps.png)

Then use a tool called [procdump](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump), to dump the process memory, in this case, we grab the firefox PID

![dumpFirefox](./res/Heist/dumpFirefox.png)

After that we can inspect the dump, since it contains a bunch of weird characters we could use strings to obtain the useful ones, despite that the file is still huge, so I used less and grep to check for credentials, and as expected, the admin credentials were found there

![loginPass](./res/Heist/loginPass.png)

With that we can try and login as administrator via winrm, and we get an elevated shell, then all we have to do is retrieve the root flag

![rootFlag](./res/Heist/rootFlag.png)

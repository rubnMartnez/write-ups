# Sauna

This is my write-up for the machine **Sauna** on Hack The Box located at: https://app.hackthebox.com/machines/229

## Enumeration

First I started with an [nmap scan](./res/Sauna/10_10_10_175_nmapReport.txt), which shows the following

![nmapScan](./res/Sauna/nmapScan.png)

It seems that the target has an Active Directory, but since port 80 was open I navigated there first to see what we are up againts, and the default page displayed is the following

![defaultPage](./res/Sauna/defaultPage.png)

Then, before digging deeper on port 80 I tried to explore smb shares, but it seems that wasn't possible

![sharesFail](./res/Sauna/sharesFail.png)

I also triggered enum4linux, which actually retrieved some interesting information about the domain

![enum4linux](./res/Sauna/enum4linux.png)

Then I got back to port 80, first I checked wappalyzer, which didn't tell us much

![wap](./res/Sauna/wap.png)

After that I ran gobuster, but it didn't find anything either, just the pages that are navigable from the website

![gobuster](./res/Sauna/gobuster.png)

And also nikto, which only found some methods that could be interesting

![nikto](./res/Sauna/nikto.png)

After navigating the website manually, I didn't find anything interesting either, just two requests that seemed to be not allowed, which was weird

![postNotAllowed](./res/Sauna/postNotAllowed.png)

So I moved to the other ports, first I started with a DNS dig, which didn't show much

![DNSdig](./res/Sauna/DNSdig.png)

After that I used ldapsearch to get the naming contexts

![ldapNamingContexts](./res/Sauna/ldapNamingContexts.png)

Which then I used to get a complete [ldap dump](./res/Sauna/ldapDump.txt)

![ldapDump](./res/Sauna/ldapDump.png)

After that I tried to get some more information with the impacket scripts, but nothing came through

![impacketScriptsFail](./res/Sauna/impacketScriptsFail.png)

## Exploitation

So I tried with kerbrute, and it retrieved a hash from the user fsmith

![kerbrute](./res/Sauna/kerbrute.png)

But when I got to hashcat, it didn't seem to work

![hashCrackingFail](./res/Sauna/hashCrackingFail.png)

After trying to crack the hash with some other modules and with john the ripper and it still didn't work, I went to the hack the box guided mode for a hint, which was to use the script GetNPUsers.py to retrieve the hash, and when I did, I noticed that the hash was different from the one retrieved previously

![hashFromImpacket](./res/Sauna/hashFromImpacket.png)

Then I was finally able to crack the hash and retrieve the credentials which where **fsmith:Thestrokes23**

![crackedHash](./res/Sauna/crackedHash.png)

And with that I was able to get a shell via winRM

![shell](./res/Sauna/shell.png)

## Post Exploitation

Then I retrieved the user flag

![userFlag](./res/Sauna/userFlag.png)

Along with some basic information about the target like groups, privileges and system information even though the last one was not available

![Groups](./res/Sauna/Groups.png)

Since it is an Active Directory I used bloodhound first to try to get a path to domain admin, so first I dumped all the information needed with bloodhound-python

![BloodhoundPy](./res/Sauna/BloodhoundPy.png)

Then I uploaded that information into bloodhound and search for a path to domain admin, but there wasn't any paths available, so I started by enumerating fsmith users to see which groups it was in

![fsmithSchema](./res/Sauna/fsmithSchema.png)

After that I enumerated the domain admins, which only had Administrator

![domainAdmins](./res/Sauna/domainAdmins.png)

So I checked the administrator groups, which were a lot

![administratorGroups](./res/Sauna/administratorGroups.png)

Since I wasn't getting any other option, I pulled the domain users to see if I could do a lateral movement

![domainUsers](./res/Sauna/domainUsers.png)

So I pulled the roastable users which was hsmith, the problem is that when I tried to pull the hash I got the clock skew too great error

![clockSkew](./res/Sauna/clockSkew.png)

After some research I found Rubeus, which should bypass the clock skew error, but it didn't work either

![rubeus](./res/Sauna/rubeus.png)

So, I changed the approach and I ran winPEAS instead, which found some interesting things, like the svc_loanmanager credentials, which are **svc_loanmanager:Moneymakestheworldgoround!**

![svc_loanmanagerCreds](./res/Sauna/svc_loanmanagerCreds.png)

But then when I tried those credentials they didn't work

![svcFailedLogin](./res/Sauna/svcFailedLogin.png)

So I did a password spray within the known users, but nothing came through either

![passSpray](./res/Sauna/passSpray.png)

I didn't understand what was going on, so I checked the write-up, and I found that the username was svc_loanmgr and not the whole name as I was using, so with that I was able to get the info via bloodhound python

![BHpyDump2](./res/Sauna/BHpyDump2.png)

And after uploading it to bloodhound GUI, I saw that the use svc_loanmanager have the permission GetChangesAll over the domain, which after checking the abuse section we could see that it is possible to use secretsdump.py to get hashes

![GetChangesAll](./res/Sauna/GetChangesAll.png)

So I used impacket secretsdump and I got the hashes

![hashes](./res/Sauna/hashes.png)

Then the only thing left to do is relay the hash in order to get an elevated shell

![elevatedShell](./res/Sauna/elevatedShell.png)

And retrieve the root flag

![rootFlag](./res/Sauna/rootFlag.png)

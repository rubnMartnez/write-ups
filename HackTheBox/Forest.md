# Forest

This is my write-up for the machine **Forest** on Hack The Box located at: https://app.hackthebox.com/machines/212

## Enumeration

First I started with an [nmap scan](./res/Forest/10_10_10_161_nmapReport.txt), which shows the following

![nmapScan](./res/Forest/nmapScan.png)

Since SMB is open, I tried to enumerate the shares, but it wasn't possible

![shareEnumFail](./res/Forest/shareEnumFail.png)

Since I didn't know where to start exactly, and it always happens to me with Active Directory, I ask chatgpt for a checklist to pentest it, and the first step was to use dig to query all DNS records

![dig](./res/Forest/dig.png)

Then I continued with enum4linux, which printed a lot of information, like users, groups and password policies

![enum4linuxUsers](./res/Forest/enum4linuxUsers.png)
![enum4linux](./res/Forest/enum4linux.png)

After that I used ldapsearch to pull some information from it

![ldapsearch](./res/Forest/ldapsearch.png)

Where I saw that there was some account names, so I did a grep of all of them

![accountNames](./res/Forest/accountNames.png)

Then I used awk to get just the usernames, and I ran GetNPUsers.py to identify users with pre-auth disabled, but I wasn't getting anything, so I tried again with the users that I got from enum4linux, and then I got svc-alfresco hash

![alfrescoHash](./res/Forest/alfrescoHash.png)

## Exploitation

After that, I went straight to hashcat to crack the hash, which gave me the following credentials **svc-alfresco:s3rvice**

![hashCracked](./res/Forest/hashCracked.png)

That allowed me to enumerate the shares

![shares](./res/Forest/shares.png)

But when I tried to enter the shares I got an error on all of them but the SYSVOL, which after downloading all it's content and checking it, there was only some policies, which isn't that useful

![shareFiles](./res/Forest/shareFiles.png)

So I tried a different approach, which was getting a shell with winRM, and it actually worked

![shell](./res/Forest/shell.png)

## Post Exploitation

Then I retrieved the user flag

![userFlag](./res/Forest/userFlag.png)

After that I started gathering information for the escalation, by checking the privileges and the groups

![groupsAndPrivs](./res/Forest/groupsAndPrivs.png)

Then I took a little detour to dump the domain info from ldap to check users, groups and policies, but there wasn't anything that stood out

![domainDump](./res/Forest/domainDump.png)

So I came back to the target machine to check the netstat to see if there was any internal port open

![netstat](./res/Forest/netstat.png)

And also the ipconfig to check if there was another subnet, which wasn't the case

![ipconfig](./res/Forest/ipconfig.png)

After that I checked if there was windefend running, which also doesn't seem to be the case

![windefend](./res/Forest/windefend.png)

Then I moved to bloodhound to see if there was a path to the domain controller, first I had to modify the /etc/hosts and the /etc/resolv.conf in order to make bloohound-python work

![resolv.conf](./res/Forest/resolv.conf.png)

With that I was able to retrieve the data with bloodhound python

![bloodhoundPython](./res/Forest/bloodhoundPython.png)

And after installing bloodhound GUI and uploading the data retrieved before I checked the domain admins, which only had the user administrator

![DomainAdmins](./res/Forest/DomainAdmins.png)

So I queried the path to get to that user, there I saw that the user we already own is in all those groups, that are inside one another

![pathToAdmin](./res/Forest/pathToAdmin.png)

Then I clicked at WriteDacl and tried the commands of the abuse section, but one of them got stuck

![failedWriteDacl](./res/Forest/failedWriteDacl.png)

After a little research I saw that the cause could be insufficient permissions and that there was some commands to be executed on the genericAll section in order to put that last group into the exchange windows permissions group

![genericAllFail](./res/Forest/genericAll.png)

Then I got back to the writeDACL commands, and this time they worked

![writeDACL](./res/Forest/writeDACL.png)

But when I tried to do the secretsdump it failed

![secretsDumpFail](./res/Forest/secretsDumpFail.png)

I was a little confused, so I went to the write-up to check which will be the correct process, and after following it, I finally got the hashes. After that, I did a little research about how this works, cause I was curious of what were the differences between the write-up and what I was doing, and apparently in this case it seems that creating a new use could make the difference because group membership may not have taken effect immediately

![writeupProcess](./res/Forest/writeupProcess.png)

After that I used psexec to pass the hash and get an elevated shell as administrator

![elevatedShell](./res/Forest/elevatedShell.png)

Then the only thing left to do was to retrieve the root flag

![rootFlag](./res/Forest/rootFlag.png)

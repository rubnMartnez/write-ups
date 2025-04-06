# SecNotes

This is my write-up for the machine **SecNotes** on Hack The Box located at: https://app.hackthebox.com/machines/151

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/SecNotes/nmapScan.png)

Since port 80 is open I went ahead to check what was on the webpage, which showed the following

![defaultPage](./res/SecNotes/defaultPage.png)

I run gobuster, but it didn't report anything interesting apart from what we were able to see from the default page

![gobusterReport](./res/SecNotes/gobusterReport.png)

I also explored the port 8808 default page, which seems to be an IIS

![iisDefaultPage](./res/SecNotes/iisDefaultPage.png)

And also run gobuster against it, which gave ablsolutely nothing

![IISgobusterReport](./res/SecNotes/IISgobusterReport.png)

So before I dive into enumerating the web further by checking how the requests are handled and so on, I wanted to enumerate a little bit the port 445, so first I checked for eternal blue, which isn't the case

![checkingForEternalBlue](./res/SecNotes/checkingForEternalBlue.png)

Then I run enum4linux, which didn't gave any useful info either

![enum4linuxReport](./res/SecNotes/enum4linuxReport.png)

It was not possible to enumerate it manually either

![smbManualEnum](./res/SecNotes/smbManualEnum.png)

I also tried with some nmap scripts to enumerate the shares, which wasn't possible, and another one to enumerate protocols, which reported that NTLM is active, which will be interesting if it wasn't a CTF without any traffic

![smbNmapScripts](./res/SecNotes/smbNmapScripts.png)

So I changed the approach to start enumerating port 80, first I tried registering, which didn't show anything weird on the request, neither does the login

![registerRequest](./res/SecNotes/registerRequest.png)
![loginRequest](./res/SecNotes/loginRequest.png)

But with that we are able to see the home defaultPage

![homePage](./res/SecNotes/homePage.png)

Here wappalyzer gave us a little bit more info

![homePageWappalyzer](./res/SecNotes/homePageWappalyzer.png)

Navigating around we could see that the contact.php and submit_note.php are sending information to the server, so maybe there's a way to upload a shell with it

![creatingNotes](./res/SecNotes/creatingNotes.png)

So I checked if there was XSS, which seems to be the case

## Exploitation

![checkingForXSS](./res/SecNotes/checkingForXSS.png)

Since XSS worked, I tried creating a php shell and fetching it with a script

![creatingPhpShell](./res/SecNotes/creatingPhpShell.png)

And it seems that the shell is fetched, but the execution is blocked by CORS

![shellFetched](./res/SecNotes/shellFetched.png)

So I tried a different approach which was to upload a reverse JS shell, and it connected, but doesn't seem to be working

![jsReverseShell](./res/SecNotes/jsReverseShell.png)

After playing a little bit with it I discovered how to use it, but it still doesn't seem to be useful

![exploringTheJSshell](./res/SecNotes/exploringTheJSshell.png)

I also checked the methods that were allowed and the headers, and I tried uploading a test image there, but it didn't work either

![checkingAllowedMethods](./res/SecNotes/checkingAllowedMethods.png)
![checkHeaders](./res/SecNotes/checkHeaders.png)

So, since I was stuck I checked the official write-up to see what I was missing, and it seems that since there's no password validation on the password change request, we can use CSRF (Cross Site Request Forgery), which I didn't know what it is, but it's pretty interesting, cause it seems that we are able to create a link from the password change request, manipulate it, and send it on the post of the contact form in order to exploit this vulnerability. So I went ahead and send the tweaked URL on the contact us form

![sendPayloadOnContactUs](./res/SecNotes/sendPayloadOnContactUs.png)

And with that I was finally able to login as tyler user

![loginAsTyler](./res/SecNotes/loginAsTyler.png)

Now if we check all of tyler notes, we could see that there's one particularly interesting which could be a login tyler / 92g!mA8BGjOirkL%OG*&

![tylerNotes](./res/SecNotes/tylerNotes.png)

So I tried to enumerate the shares and connect to SMB with tyler's password, and it worked

![connectToSMBwithTylerPass](./res/SecNotes/connectToSMBwithTylerPass.png)

So I tried to run psexec to see if I could get a shell right away, but it didn't work

![psexecFail](./res/SecNotes/psexecFail.png)

With that in mind, I uploaded a png as a test and php shell to the server to check if it works

![pngTest](./res/SecNotes/pngTest.png)
![phpShell](./res/SecNotes/phpShell.png)

Then I tried uploading some reverse shells, but they didn't work

![reverseShellTries](./res/SecNotes/reverseShellTries.png)
![listener](./res/SecNotes/listener.png)

So I referred to the write-up again, which suggested to upload a netcat exe that's stored on our kali machine and use it to trigger the reverse shell, so I located the nc.exe

![locateNetcat](./res/SecNotes/locateNetcat.png)

I created the reverse php shell

![createReversePhpShell](./res/SecNotes/createReversePhpShell.png)

Ans I uploaded everything to the server

![uploadNetcat](./res/SecNotes/uploadNetcat.png)

And finally got that reverse shell

![gettingReverseShell](./res/SecNotes/gettingReverseShell.png)

## Post Exploitation

I tried doing some basic enumeration as usual, but it seems that systeminfo is being blocked

![sysinfoBlocked](./res/SecNotes/sysinfoBlocked.png)

I was able to pull the privs of the user though

![privs](./res/SecNotes/privs.png)

As well as the local groups and the antivirus status

![groupsAndAV](./res/SecNotes/groupsAndAV.png)

Also it was possible to check the netstat

![netstat](./res/SecNotes/netstat.png)

Navigating around I found tyler's password for SecNotes inside this script which is forested85sunk

![tylerSecNoterPass](./res/SecNotes/tylerSecNoterPass.png)

I also got the user flag

![userFlag](./res/SecNotes/userFlag.png)

Now I'd normally go with winPEAS or some other automated tool to help me identify possible escalation paths, but since I'm doing this box because it was part of the windows privilege escalation course that I'm doing, and there's they gave a hint of using WSL I'm going to try that even though I've never use it, and if I get stuck I'll get back to the course. So I got a [guide](https://swisskyrepo.github.io/InternalAllTheThings/redteam/escalation/windows-privilege-escalation/#example-with-windows-xp-sp1-upnphost) that suggested to find bash.exe and so I did

![findingBashExe](./res/SecNotes/findingBashExe.png)

Since I had root privileges on the WSL shell I tried launching a reverse shell against my kali machine as the guide suggested

![pythonRevShell](./res/SecNotes/pythonRevShell.png)

And it worked, but it only gave me access to the WSL subsystem

![pythonRevShellListener](./res/SecNotes/pythonRevShellListener.png)

So I went back to the course to see what would be the correct way to do it. Which it seems that all we had to do is check the history of WSL, which contains the admin password which is u6!4ZwgwOM#^OBf#Nwnh

![history](./res/SecNotes/history.png)

So now all we have to do is connect to it and retrieve the root flag

![connectToAdminSMB](./res/SecNotes/connectToAdminSMB.png)

![rootFlag](./res/SecNotes/rootFlag.png)

# Jerry

This is my write-up for the machine **Jerry** on Hack The Box located at: https://app.hackthebox.com/machines/144

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/Jerry/nmapScan.png)

Since only the port 8080 I procced to go to webpage, which a default apache tomcat page is presented

![defaultPage](./res/Jerry/defaultPage.png)

I run gobuster to see if there's any interesting directory, which it seems to be the case 

![gobusterReport](./res/Jerry/gobusterReport.png)

Before enumerating this new directories, I activate burp suite scope, to see if it catches something else

![burpScope](./res/Jerry/burpScope.png)

it seems that the /docs is only documentation about tomcat, but on /manager we get a login page, so first I'll try with default credentials for tomcat

![loginPage](./res/Jerry/loginPage.png)

I found the following list of default credentials online

![defaultCredsList](./res/Jerry/defaultCredsList.png)

And after some trys, I was able to log in with **tomcat:s3cret**

![managerPage](./res/Jerry/managerPage.png)

If we scroll down we could se the server information, a part from that, it seems that it is running some kind of deployment process with WAR files and XML, but I'll have to google it, since I don't know how it works

![serverInfo](./res/Jerry/serverInfo.png)

After googling it, it seems that WAR files are packaged Java web applications, which seems to be executable, I've navigate it to the examples dir, and there's some executable scripts, so probably we will be able to upload a reverse shell here

![Examples](./res/Jerry/Examples.png)

Just to see how it works, I opened the source code of Hello World servlet and then execute it

![helloWorldCode](./res/Jerry/helloWorldCode.png)
![helloWorldExecution](./res/Jerry/helloWorldExecution.png)

## Exploitation

So I created a war reverse shell with msfvenom

![creatingWarShell](./res/Jerry/creatingWarShell.png)

Then I've uploaded it on the war file deployment section

![warShellDeployment](./res/Jerry/warShellDeployment.png)

And now we could see that it appears on the applications of the maneger panel

![shellOnManagerPanel](./res/Jerry/shellOnManagerPanel.png)

Then we open it and we could see that a shell pops up

![reverseShell](./res/Jerry/reverseShell.png)

## Post Exploitation

Since the uid was Jerry instead of system, I though that we'll have to escalate privileges

![generalEnum](./res/Jerry/generalEnum.png)

But after some basic enumeration and moving throught the directories, I saw that we were able to get inside the Administrator folder and retrieve the flags

![Flags](./res/Jerry/Flags.png)
# Blue

This is my write-up for the machine **Blue** on Hack The Box located at: https://app.hackthebox.com/machines/51

first we start with an nmap scan, it shows the following:

![nmapScan](./Imgs/Blue/nmapScan.png)

Since the port for SMB is open, and we know that hack the box usually give us hint on the machine name, we could try to exploit eternal blue. A quick google search which the specific windows version lead us to this minitutorial on how to exploit it with metasploit

![SMBmetasploitExploit](./Imgs/Blue/SMBmetasploitExploit.png)

After setting up the options for the exploit we get a shell

![exploitConfig](./Imgs/Blue/exploitRun.png)

we can find the user flag here:

![userFlag](./Imgs/Blue/userFlag.png)

and the root flag here:

![rootFlag](./Imgs/Blue/rootFlag.png)
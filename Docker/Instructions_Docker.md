Instructions for starting a Docker service at local computer. 
The Docker service allows to run all the code on a local machine. The Docer service will run an ```image```
containing all the necessary software packages.

Full list of the packages available in provided image can be found [here](https://hub.docker.com/repository/docker/akalinow/root-fedora31)


1. Instruction hot to install the Docker application on 
[Linux](https://docs.docker.com/install/linux/docker-ce/fedora/), 
[Windows](https://docs.docker.com/docker-for-windows/),
[MacOS](https://docs.docker.com/docker-for-mac/install/)

**Note**: after the installation one has to restart the computer.

2. Dowload and run the ```runDocker``` script for [Windows](runDocker.bat), and [Linux, MacOS](runDocker.sh) 
   to start the container.

3. After starting the container one gets acces to a terminal window:

---
[jupyter@07fe5696fbe3 ~]$ 
---

4. Starting the jupyter server:

---
[jupyter@07fe5696fbe3 /]$ cd
[jupyter@07fe5696fbe3 ~]$ ./start-notebook.sh 
---

In the terminal window you will see an information that server has started, and is available under URL similar to:

---
http://127.0.0.1:8000/?token=0e4f4e2560cd4a409ec01c2317ca26cc5cbd09ea7ad2413
---

Please copy this URL to web browser to start the jupyter client.

5. All files created within the container in ```scratch``` directory are visible in the host system:
on Windows on the desktop in directory ```Docker```, on Linux in the root directory, ```\```.








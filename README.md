# RUMBA


## Introduction

 The objective of this software project is to deliver  a webapp that allows recording live concerts, combining good quality sound as provided by the sound technician with video as recorded  by the audience using their mobile phones.
 
 Using the same webapp authorized video editors can easily combine the different videos  recorded by the audience and publish an edit that combines these videos and the audio track, thus obtaining an edited multi-camera recording with good sound quality.


## Credits


The original idea for this software arose in a meeting of the parents association of the public school La Concepció, in Barcelona. Editing videos of the concerts of the students was a daunting task. We conceived a better, simpler way to do this with mobile phones, and named such a software with the school's transversal topic of that year: the musical style known as **Rumba** . Thanks to a program on citizen innovation run by Victor Jiménez and the support of the Institut de Cultura de Barcelona (ICUB), we managed to develop the prototype found in this code repository. 

The software was designed by Dr Joan Llobera. The graphical layout was designed by Ms Gemma Solana. The software was implemented mainly by Mr Adrián Rosselló (backend) and Mr Enric Alminyana (Front-end).



## Roadmap
**todo:** There are still several technical issues to be solved (see known issues section)

Once the previous issues are solved, the following step will be to implement a service that suggests video edits, in order that by default the cuts between the different sources are already suggested. Thus the editor will only have to check the suggestion, and change it if needed. This will further accelerate the edition process.


## Project set up with a virtual machine (with vagrant)

For development purposes it is more convenient to use vagrant and deploy this software in a virtual machine. Vagrant is a virtual machine manager, similar to Docker. To do so, you should:

### Installation

 1. Install  Hypervisor and Vagrant

```console 
sudo apt install virtualbox
sudo apt install vagrant

```

 2. Create a folder `/vagrant`, and a subfolder called  `rumba`
 3. Download this repository in this rumba folder


Running `vagrant up` in the same folder where there is the *Vagrantfile* will create a virtual machine and then, within the virtual machine, call ansible, which is the tool that actually installs all the dependencies.

### Configuration
Once the dependencies are installed, to run the project you  will also need to configure some small things:

 1. Copy the certificates for janus. For this, you should enter inside the virtual machine, and copy them. Specifically:

```console

$sudo vagrant ssh

vagrant@vagrant-ubuntu-trusty-64:~$ sudo cp -R /vagrant/rumba/janus/certs/   /opt/janus/share/janus/.` 

```
  
 2. if necessary, copy  `/vagrant/rumba/backend/backend.cfg.example` to `/vagrant/rumba/backend/backend.cfg (and change {{janus_dir}})

 3. Find out if the services are running, otherwise, enter into the virtual machine and restart supervisor. Specifically, this means:

```
  sudo vagrant ssh
  sudo service nginx restart
  sudo supervisorctl restart rumba-backend
``` 
### Running the vagrant virtual machine

There are different ways to start and stop the virtual machine created. Specifically: 
 - `sudo vagrant up` and `sudo vagrant halt`  allows you to  power on and off the virtual machine
 -  `sudo vagrant suspend` and `sudo vagrant resume` allows you to  pause and resume the Virtual Machine. It is quite quite faster than the previous

### Known issues

- Since vagrant sets up the folder  `/vagrant/rumba` at the end of the initialization, starting the services is problematic because it does not have the right folder available. In this case, the simplest is to enter into the virtual machine and restart all the services. This can be done by doing:  
  ```console

  $vagrant ssh
  sudo supervisorctl reload

  ```
- The angular service, used by angular in the frontend, uses an excessive amount of resources.

PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND                                                                                        
 2505 vagrant   20   0 1603788 451032  13432 S 133.4  5.5  58:28.60 ng  
possible solutions, depending on the OS used, can be found here:
https://github.com/angular/angular-cli/issues/2748

- The app has only been tested with android devices as clients. It is likely that the editing mode will not work with ios due to the fact that mpeg-dash is not supported on ios.  

- Once connecting to the service in this setup, the videos downloaded have no audio. This may be due to the fact that the virtual machine has no access to the sound input
- The edition view has not been tested yet



## Getting Started installing directly in an ubuntu machine

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

 **TODO: complete the instructions or update the repo to use ansible without entering into trouble**

### Prerequisites

This software has been developed and tested in Ubuntu 14.04.

In order to install and deploy it, the following software should be already installed in your system.

<ul>
    <li> Python3.4 or later</li>
    <li> Ansible </li> 
    <li> Git </li>
</ul>

### Installing

1) Edit <b>variables.yml</b> file in ansible/vars folder to match your needs:

<ul>
    <li>rumba_src_folder: Absolute path of the folder where the cloned code will reside.</li>
    <li>frontend_port: Port that the frontend will be listening</li>
    <li>backend_port: Port that the backend will be listening</li>
    <li>ffmpeg_version: Version of FFMPEG to download and install</li>
    <li>janus_dir: Absolute path to the folder where Janus will be installed.</li>
    <li>ubuntu_user: Username for ubuntu system</li>


</ul>

2) set up the hosts file in the file /etc/ansible/hosts

```console
$ echo "localhost" > /etc/ansible/hosts
```
you can also replace the localhost, with the ip where you want to install all this, always in double quotes


3) Execute Ansible playbook for installing the software and its dependencies

``` 
$ ansible-playbook ansible/installation.yml --ask-become-pass
``` 

Please be patient, this command takes a while, since it needs to download, compile and/or install the software and all its dependencies.

### Deployment

In order to deploy the software, we provide two different methods: either deploy the software in a byobu session or deploy it as services managed by the  <a href="http://supervisord.org/" target="_blank">Supervisor</a> package.
<br>
#### Deploying on Byobu

Execute the <b>byobu_deployment.yml</b> playbook for installing <a href="http://byobu.co/" target="_blank">Byobu</a> and deploy the software in it:

```
$ ansible-playbook ansible/byobu_deployment.yml --ask-become-pass
```

In order to join to the byobu session, just execute the byobu command:

```
$ byobu
```

#### Deployment as services of Supervisor

Execute the <b>supervisor_deployment.yml</b> playbook for installing the Supervisor service and deploy the software in it.

```
$ ansible-playbook ansible/supervisor_deployment.yml --ask-become-pass
```

Once it finishes, the state of the different Rumba components can be checked by executing the supervisorctl command.

```
$ sudo supervisorctl
```


### LOGS

By default, backend logs are written in <b>/var/rumba/logs folder</b>, separated in different files 
depending on the component. Regarding Janus, logs are located in <b>/var/log/janus/</b> folder.







Vagrant.configure("2") do |config|
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "8192", "--cpus", "8"]
    end
    config.vm.box = "ubuntu/trusty64"
    config.vm.synced_folder ".", "/vagrant/rumba"
    config.vm.network "private_network", ip: "192.168.100.100"
    config.vm.network "forwarded_port", guest: 443, host: 443
    config.vm.network "forwarded_port", guest: 8081, host: 8081
    config.vm.network "forwarded_port", guest: 4200, host: 4200
    config.vm.provision "ansible_local" do |all|
        all.playbook = "rumba/ansible/installation_local.yml"
    end
    config.vm.provision "ansible_local" do |run|
        run.playbook = "rumba/ansible/supervisor_deployment.yml"
    end


require 'yaml'

config = YAML.load(<<-EOF)
box:
    url: "ubuntu/trusty64"
    check_update: false

provider:
    name: "ubuntu14.04-docker"
    memory: 1024
    window: false

mount:
    from: #{Dir.home}
    to: "/mnt/host" 

network:
    ip: "10.0.0.10"

    forwarded_port:
      - guest: 80
        host: 8080
EOF

Vagrant.configure(2) do |vagrant|
  vagrant.vm.box              = config["box"]["url"]
  vagrant.vm.box_check_update = config["box"]["check_update"]
  
  forwarded_port = config["network"]["forwarded_port"]
  forwarded_port.each do |mapping|
    vagrant.vm.network "forwarded_port", guest: mapping["guest"], host: mapping["host"]
  end
  vagrant.vm.network "private_network", ip: config["network"]["ip"], id: "default-network"

  vagrant.vm.synced_folder config["mount"]["from"], config["mount"]["to"]
  vagrant.vm.provider "virtualbox" do |vbox|
    vbox.name   = config["provider"]["name"]
    vbox.memory = config["provider"]["memory"]
    vbox.gui    = config["provider"]["window"]
    #vbox.customize ["modifyvm", :id, '--audio', 'coreaudio', '--audiocontroller', 'hda'] 
    vbox.customize ["modifyvm", :id, '--audiocontroller', 'hda'] 
  end

  vagrant.ssh.forward_x11 = true  
  vagrant.vm.provision "shell", inline: <<-EOF
    apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' | tee /etc/apt/sources.list.d/docker.list
    apt-get update && apt-cache policy docker-engine
    apt-get update && apt-get install -y docker-engine

    ## Audio Support
    add-apt-repository ppa:ubuntu-audio-dev/alsa-daily
    apt-get update && \
    apt-get install -y linux-headers-$(uname -r) \
       oem-audio-hda-daily-dkms alsa alsa-utils pulseaudio pulseaudio-utils gconf2 paprefs

    groupadd docker
    gpasswd --add vagrant docker
    gpasswd --add vagrant audio

    ## Audio Settings
    echo 'options snd-hda-intel model=generic index=0' >> /etc/modprobe.d/alsa-base.conf
    echo 'snd'                                         >> /etc/modules
    echo 'snd-hda-intel'                               >> /etc/modules
    modprobe snd
    modprobe snd-hda-intel
    alsa force-reload
    service pulseaudio restart

    #docker run hello-world
  EOF
end




end

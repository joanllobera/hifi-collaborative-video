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
end

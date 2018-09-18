Vagrant.configure("2") do |config|
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
    config.vm.box = "ubuntu/trusty64"
    config.vm.synced_folder ".", "/vagrant/rumba"
    Vagrant.configure("2") do |config|
      config.vm.network "forwarded_port", guest: 8081, host: 8081
      config.vm.network "forwarded_port", guest: 4200, host: 4200
    end
    config.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "rumba/ansible/installation.yml"
    end
    config.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "rumba/ansible/supervisor_deployment.yml"
    end
end

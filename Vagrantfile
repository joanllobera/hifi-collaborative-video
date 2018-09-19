Vagrant.configure("2") do |config|
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
    config.vm.box = "ubuntu/trusty64"
    config.vm.synced_folder ".", "/vagrant/rumba"
    config.vm.network "forwarded_port", guest: 8081, host: 8081, id: 'backend'
    config.vm.network "forwarded_port", guest: 4200, host: 4200, id: 'frontend'
    config.vm.provision "ansible_local" do |all|
        all.playbook = "rumba/ansible/installation_local.yml"
    end
    config.vm.provision "ansible_local" do |run|
        run.playbook = "rumba/ansible/supervisor_deployment_local.yml"
    end
end

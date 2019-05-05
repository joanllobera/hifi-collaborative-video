echo "this script needs to be run in the main  folder where we want to install everything else, without doing git checkout nor anything else"
echo "we update apt and install git"
# dpkg --configure -a
apt update 
apt install -y git

echo "we install python, specifically version 3.4"
apt install -y python3.4

echo "we install ansible"
apt  install -y software-properties-common
apt-add-repository -y  ppa:ansible/ansible
apt install -y ansible

echo "we clone the rumba repo and find out how to move ahead"
git clone https://github.com/joanllobera/hifi-collaborative-video.git


echo "PROBLEM: you need to change the ubuntu_user from vagrant to ubuntu"
cp hifi-collaborative-video/ansible/vars/variables.yml.fiware hifi-collaborative-video/ansible/vars/variables.yml



 
echo "we add targeted IP to hosts########################################" 
#192.168.111.147
#echo "192.168.111.147" > /etc/ansible/hosts

#echo "185.52.32.31" > /etc/ansible/hosts


#echo "localhost" > /etc/ansible/hosts

ansible-playbook  hifi-collaborative-video/ansible/installation.yml  -u ubuntu -b   --private-key=pangpongkey.pem



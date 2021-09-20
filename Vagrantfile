# -*- mode: ruby -*-
# vi: set ft=ruby  :

# #########################################################################################
# Based on Kubernetes blog post 
# https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/
# #########################################################################################

# Numero de nodes a ser criado
NODES = 2

# Image padrão 
IMAGE_NAME = "ubuntu/focal64"

# Memoria total para o master
MASTER_MEMORY=2048

# Memoria para cada node
NODE_MEMORY=1024

Vagrant.configure("2") do |config|

#   config.ssh.insert_key = false
      
    config.vm.define "k8s-master" do |master|
        master.vm.box = IMAGE_NAME
        master.vm.network "private_network", ip: "192.168.50.10"
        master.vm.hostname = "k8s-master"
        master.vm.provider :virtualbox do |vb|
            vb.name = "k8s-master"
            vb.memory = MASTER_MEMORY
            vb.cpus = 2
            vb.customize ["modifyvm", :id, "--groups", "/bonde-cka"]
        end        
        master.vm.provision "ansible" do |ansible|
            ansible.playbook = "kubernetes-setup/master-playbook.yml"
            ansible.extra_vars = {
                node_ip: "192.168.50.10",
            }
        end
    end

    (1..NODES).each do |i|
        config.vm.define "k8s-node-#{i}" do |node|
            node.vm.box = IMAGE_NAME
            node.vm.network "private_network", ip: "192.168.50.#{i + 10}"
            node.vm.hostname = "node-#{i}"
            node.vm.provider :virtualbox do |vb|
                vb.name = "k8s-node-#{i}"
                vb.memory = NODE_MEMORY
                vb.cpus = 2
                vb.customize ["modifyvm", :id, "--groups", "/bonde-cka"]
            end                  
            node.vm.provision "ansible" do |ansible|
                ansible.playbook = "kubernetes-setup/node-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10}",
                }
            end
        end
    end
end
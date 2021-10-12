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

# Memoria total para o controlplane
CONTROLPLANE_MEMORY=2048

# Memoria para cada worker
WORKER_MEMORY=1024

# Network prefix
NETWORK_PREFIX="192.168.165"

# Virtualbox Group name
VM_GROUP_NAME="bonde-cka"

Vagrant.configure("2") do |config|

    #config.ssh.insert_key = false
    config.vm.define "k8s-controlplane" do |controlplane|
        controlplane.vm.box = IMAGE_NAME
        controlplane.vm.network "private_network", ip: "#{NETWORK_PREFIX}.10"
        controlplane.vm.hostname = "k8s-controlplane"
        controlplane.vm.provider :virtualbox do |vb|
            vb.name = "k8s-controlplane"
            vb.memory = CONTROLPLANE_MEMORY
            vb.cpus = 2
            vb.customize ["modifyvm", :id, "--groups", "/#{VM_GROUP_NAME}"]
        end        
        controlplane.vm.provision "ansible" do |ansible|
            ansible.playbook = "kubernetes-setup/k8s-controlplane-playbook.yml"
            ansible.groups = {
                "controlplane" => ["k8s-controlplane"]
            }
            ansible.extra_vars = {
                node_ip: "#{NETWORK_PREFIX}.10",
                k8s_hostname: "k8s-controlplane"
            }
        end
    end

    (1..NODES).each do |i|
        config.vm.define "k8s-worker-#{i}" do |node|
            node.vm.box = IMAGE_NAME
            node.vm.network "private_network", ip: "#{NETWORK_PREFIX}.#{i + 10}"
            node.vm.hostname = "k8s-worker-#{i}"
            node.vm.provider :virtualbox do |vb|
                vb.name = "k8s-worker-#{i}"
                vb.memory = WORKER_MEMORY
                vb.cpus = 2
                vb.customize ["modifyvm", :id, "--groups", "/#{VM_GROUP_NAME}"]
            end                  
            node.vm.provision "ansible" do |ansible|
                ansible.playbook = "kubernetes-setup/k8s-worker-playbook.yml"
                ansible.groups = {
                    "workers" => ["k8s-worker-#{i}"]
                }                
                ansible.extra_vars = {
                    node_ip: "#{NETWORK_PREFIX}.#{i + 10}",
                    k8s_hostname: "k8s-worker-#{i}"
                }
            end
        end
    end
end
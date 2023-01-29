# -*- mode: ruby -*-
# vi: set ft=ruby  :

# #########################################################################################
# Based on Kubernetes blog post 
# https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/
# #########################################################################################

# https://ostechnix.com/how-to-use-vagrant-with-libvirt-kvm-provider/
# vagrant plugin install vagrant-libvirt

# Numero de nodes a ser criado
NODES = 2

# Image padrão 
IMAGE_NAME = "generic/ubuntu2004"

# Memoria total para o controlplane
CONTROLPLANE_MEMORY=2048

# Memoria para cada worker
WORKER_MEMORY=1024

ENABLE_STORAGE=false

Vagrant.configure("2") do |config|

    config.vagrant.plugins = "vagrant-libvirt"
    config.vm.box = IMAGE_NAME

    (1..NODES).each do |i|
        config.vm.define "k8s-worker-#{i}" do |node|
            node.vm.hostname = "k8s-worker-#{i}"
            node.vm.provider :libvirt do |vb|
                vb.memory = WORKER_MEMORY
                vb.cpus = 2
            end
        end
    end

    if ENABLE_STORAGE then
        config.vm.define "k8s-storage" do |storage|
            storage.vm.hostname = "k8s-storage"
            storage.vm.provider :libvirt do |vb|
                vb.memory = WORKER_MEMORY
                vb.cpus = 2
            end
        end
    end

    #config.ssh.insert_key = false
    config.vm.define "k8s-controlplane" do |controlplane|
        controlplane.vm.hostname = "k8s-controlplane"
        controlplane.vm.provider :libvirt do |vb|
            vb.memory = CONTROLPLANE_MEMORY
            vb.cpus = 2
        end        

        controlplane.vm.provision :ansible do |ansible|
            ansible.playbook           = "kubernetes-setup/k8s-cluster.yml"
            ansible.verbose            = false
            ansible.compatibility_mode = '2.0'
            ansible.limit              = 'all'
            ansible.inventory_path     = "inventory.py"
        end
    end
end
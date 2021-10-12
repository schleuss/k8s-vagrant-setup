# K8S Study Environment

## Requirements


1) [Vagrant](https://www.vagrantup.com/docs/installation)
2) [Kubectl](https://kubernetes.io/docs/tasks/tools/)


## Execute

Execute on the current folder:

```
vagrant up
```

After the process finish, a new file will be created on the local folder (kubernetes_config.conf). This file is the k8s config file.

Use the KUBECONFIG environment variable to use this k8s instance.

```
export KUBECONFIG="$(pwd)/kubernetes_config.conf"
```

To test:

```
$ kubectl get nodes
NAME         STATUS   ROLES                  AGE     VERSION
k8s-master   Ready    control-plane,master   8m9s    v1.22.2
node-1       Ready    <none>                 5m20s   v1.22.2
node-2       Ready    <none>                 2m2s    v1.22.2
```

Delete the env

```
vagrant destroy
```

Use suspend/resume to pause de execution

```
vagrant suspend
vagrant resume
```

# Enable MetalLB

Based on MetalLB [doc](https://metallb.universe.tf/installation/)

Enable strictARP

```
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system
```

Install MetalLB

``` 
 kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/namespace.yaml
 kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/metallb.yaml
 ```

 Configure MetalLB


 1) Create a YAML file (metallb-conf.yaml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.165.100-192.168.165.250
```

2) Apply the config file 

```bash
kubectl apply -f  metallb-conf.yaml
```


# Remove all vagrant instances

This command stops the running machine Vagrant is managing and destroys all resources that were created during the machine creation process. 

```bash
vagrant destroy
```

# Run Ansible on remote servers

To run the ansible playbook on remote servers, first create a inventory file inside kubernetes-setup directory

```
[all:vars]
ansible_user=root

[controlplane]
192.168.60.214 k8s_hostname=k8s-controlplane

[workers]
192.168.60.215 k8s_hostname=k8s-worker-01
192.168.60.216 k8s_hostname=k8s-worker-02
```

Run ansible main playbook

```bash
ansible-playbook -i inventory k8s-cluster-playbook.yml
```

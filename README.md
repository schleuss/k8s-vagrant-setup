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
NAME               STATUS   ROLES           AGE     VERSION
k8s-controlplane   Ready    control-plane   80m     v1.26.1
k8s-worker-1       Ready    <none>          9m31s   v1.26.1
k8s-worker-2       Ready    <none>          3m56s   v1.26.1
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
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/config/manifests/metallb-native.yaml
 ```

 Configure MetalLB


 1) Create a YAML file (metallb-conf.yaml)

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: metallb-addr-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.121.100-192.168.121.199

---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: metallb-l2advertisement
  namespace: metallb-system
```

2) Apply the config file 

```bash
kubectl apply -f metallb-conf.yaml
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
192.168.165.10

[workers]
192.168.165.11
192.168.165.12

[storage]
192.168.165.15
```

Run ansible main playbook

```bash
ansible-playbook -i inventory k8s-cluster.yml
```

# Enable K8S Metrics Server

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

If the metrics server doesn't work correctly, perform the following configuration changes

> Fonte: https://www.devopszones.com/2022/06/kubernetes-error-from-server.html

```bash
kubectl patch deployments -n kube-system metrics-server \
   --type=json -p '{"spec": {"template": {"spec": {"hostNetwork": true, "dnsPolicy": "ClusterFirst"}}}}'

# Only when using invalid certificates.. (x509: cannot validate certificate)
kubectl patch deployments.apps -n kube-system metrics-server \
   --type=json -p '[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls" }]'
```



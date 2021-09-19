# Ambiente de estudos K8S

## Instalação

Instalar vagrant
Iniciar ambiente

```
vagrant up
```

Apos iniciar, o arquivo kubernetes_config.conf será gerado na pasta local do projeto.

```
export KUBECONFIG="$(pwd)/kubernetes_config.conf"
```


```
vagrant destroy
```
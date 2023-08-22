이것은 제목이고
=========================================================

# 요것도 제목이고
## 이건 서브1
### 이건 서브2
#### 이건 서브3
##### 이건 서브4
###### 이건 서브5

```
동해물과 백두산이 마르고 닳도록
하느님이 보우하사 우리 나라 만세
```

Start installing monitoring<br>
Start installing multicluster<br>
Start installing openpitrix<br>
Start installing network<br>

**************************************************
Waiting for all tasks to be completed ...<br>
task multicluster status is successful  (1/4)<br>
task openpitrix status is successful  (2/4)<br>
task network status is successful  (3/4)<br>
task monitoring status is successful  (4/4)<br>
**************************************************


링크는 이렇게 거는건가 https://github.com/kubesphere/kubekey/releases/download/v3.0.8/ubuntu-20.04-debs-amd64.iso
 - [InstallRegistryModule] Sync docker binaries.
 - [InstallRegistryModule] Generate docker service.
 - [InstallRegistryModule] Generate docker config.
 - [InstallRegistryModule] start harbor

```
./create_project_harbor.sh 
creating library
{"errors":[{"code":"CONFLICT","message":"The project named library already exists"}]}
creating kubesphereio
creating kubesphere
creating calico
creating coredns
creating openebs
creating csiplugin
creating minio
creating mirrorgooglecontainers
creating osixia
creating prom
creating thanosio
creating jimmidyson
creating grafana
creating elastic
creating istio
creating jaegertracing
creating jenkins
creating weaveworks
creating openpitrix
creating joosthofman
creating nginxdemos
creating fluent
creating kubeedge
```

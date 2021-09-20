# PeerConnection
python ip 端口转发， 支持多用户访问

#### 使用场景
虚拟机A可以访问B，但无法访问C, 虚拟机B可以访问C.    
通过在虚拟机B上执行脚本，实现虚拟机A访问C的目的。    

#### 使用方式
```
python3 peer_connection.py -s {current_vm_ip}:{current_vm_port} -c {target_vm_ip}:{target_vm_port}
current_vm_ip: 当前虚拟机ip(在该虚拟机上执行脚本)
target_vm_ip: 目的虚拟机ip(要访问的虚拟机ip)

```

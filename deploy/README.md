# Docker Swarm

## Create the infrastructure

```
terraform apply -var-file=<env>/<env>.tfvars
```

## Set up
You should specify on the inventories folder, a new folder with a hosts file. your should define two groups
- ds-master
- ds-workers

```ini
[ds-master]
192.168.33.100 ansible_user=vagrant

[ds-workers]
ds-slave01 ansible_user=vagrant
ds-slave02 ansible_user=vagrant
```

## Update the group_vars

_inventories/<inventory_name>/ds-master.yml_
```
ip: <master_ip>
client_ips:
  - <worker1_ip>
  - ...
  - <workern_ip>

```

_inventories/<inventory_name>/ds-workers.yml_
```
master_ip: <master_ip>
token: <token>
```

## Run the playbook
```
ansible-playbook -i <inventory-path> -e domain_name=<domain-name> playbook-master.yml
```

The last line of this playbook prints the token

```
ansible-playbook -i <inventory-path> -e token=<token> playbook-workers.yml
```

## Deploy into the cluster

1. Log in into the master node
2. On portainer create the network and the volumes (media_<domain_name>, static_<domain_name>, etc. ...)
3. 
```
docker stack deploy --compose-file=<docker-compose-file>.yml <service>
```

## Add a site to the load balancer
```
ansible-playbook -i inventories/do -e domain_name=<domain_name> -e project_port=<port> playbook_add_site_to_loadbalancer.yaml
```

## Clean up the docker system
```
ansible-playbook -i <inventory> playbook-cleanup.yml

```

## Set up the secret vaults
```
ansible-playbook -i <inventory> playbook-setup-secret-vaults.yml

```

## Change the email server
```
ansible-playbook -i <inventory> -e email_server_id=[1-3] playbook-change-email-account.yml

```



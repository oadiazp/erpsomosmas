output "lb-ip" {
  value = "${digitalocean_loadbalancer.lb.ip}}"
}

output "cluster-ips" {
  value = "${digitalocean_droplet.cluster.*.ipv4_address_private}"
}
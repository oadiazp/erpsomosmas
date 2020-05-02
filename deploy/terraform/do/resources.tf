resource "digitalocean_droplet" "cluster" {
  image  = "ubuntu-18-04-x64"
  name   = "web"
  region = "nyc3"
  ssh_keys = ["${data.digitalocean_ssh_key.ssh_key.id}"]
  size   = "s-1vcpu-1gb"
  count = 3
  private_networking = true
}

resource "digitalocean_loadbalancer" "lb" {
  name = "${var.env}"
  region = "nyc3"

  forwarding_rule {
    entry_port = 80
    entry_protocol = "tcp"
    target_port = 80
    target_protocol = "tcp"
  }

  forwarding_rule {
    entry_port = 443
    entry_protocol = "tcp"
    target_port = 443
    target_protocol = "tcp"
  }

  droplet_ids = "${digitalocean_droplet.cluster.*.id}"
}

resource "digitalocean_spaces_bucket" "bucket" {
  name   = "${var.env}-videos"
  region = "nyc3"
}

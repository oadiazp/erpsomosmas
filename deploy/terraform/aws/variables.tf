variable "region" {
  default = "eu-central-1"
}

variable "environment" {}

variable "cidr_vpc" {}

variable "cidrs_public" {
  type = "list"
}

variable "cidrs_private" {
  type = "list"
}

variable "ssl_cert_arn" {}

variable "nodes_amount" {}

variable "instance_type" {}

variable "redis_subnet_cidr" {}

variable "create_redis" {}

variable "create_db" {}

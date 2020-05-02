data "aws_availability_zones" "available" {
}

module "vpc" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "2.17.0"

  name                 = "${var.environment}-vpc"
  cidr                 = var.cidr_vpc
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = var.cidrs_private
  public_subnets       = var.cidrs_public

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
}

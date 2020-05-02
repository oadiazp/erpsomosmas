locals {
  cluster_name = "bajanda-${var.environment}"
}

resource "aws_instance" "cluster_node" {
  ami                    = "${data.aws_ami.ubuntu.id}"
  instance_type          = "${var.instance_type}"
  subnet_id              = module.vpc.public_subnets.0
  key_name               = "ZCKey-${var.environment}"
  security_groups        = ["${aws_security_group.cluster.id}"]
  vpc_security_group_ids = ["${aws_security_group.cluster.id}"]
  count                  = "${var.nodes_amount}"

  tags = {
    env = "${var.environment}"
  }
}

resource "aws_security_group" "cluster" {
  name        = "cluster-${var.environment}"
  description = "Cluster security group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "videos-storage" {
  bucket = "${var.environment}-bajanda"
  acl    = "private"
}

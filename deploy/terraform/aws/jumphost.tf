resource "aws_key_pair" "ssh_key" {
  key_name   = "ZCKey-${var.environment}"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC2dlV+E5VKFbZ8EBh2OozAq4zGdeORUVDZyyy1DXHshcWfiYLl3l1HeBoxypGjBW9HUrF9JqKYKaFvhkrRpvYlZpQpO5Ckx5kEpguBXSlE9f4SaUroVU4tWXHAjDS6dbwdOTGAVOYBYVXgf5fXOabMMRlMMHypN6mX321L5MSAMQEZPuSUG3TU0tizwxwfuJrXk9wu6wXWeoqI7QeuCsKCr1xCFHa0GjLTsZT4GFcsk3G3nVqopPwrudb3Ll77IeF+EgudqfmVUYeqcJgjlOtewpVOOZqDxiJXI2DKL1fuVPCgtIAM4w4V+xziTAOSyPfB0xvAkGpQ1XuCDwkmFEyUvYmvmYZ6PklO1il4PIYkZTtBjZ/FrPv5XKzW+K7sZkwZSAml9VAuXYqqD0TEcz88hxbB3e6c1hDKwKnOnhg1Yj1F2mNfABulSPU5hrQrmbAU6OQOniDIDhDzsiDVIGkKsQluKKyjfxjvHPQ/L35pypF02pH7FDhxGj36H/Jzf6yAGNKQd7Nlemr5aipSrGZMIZS/EsX8/1Mo/rnKB1R3sH342WaLuby7e+N/2vQtu2jaxvC0yxQpa3kh+mSh5LpavwZNFnGqKGnV98HH8EWvasBq3Ru8Sas9rICaiTYHZwHF+MT8DWU7lbg6b2RHfljQKVSC7xWCXoCbA2bR6OFezw== zcool@zclaptop"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "jumphost" {
  ami                    = "${data.aws_ami.ubuntu.id}"
  instance_type          = "t2.micro"
  subnet_id              = module.vpc.public_subnets.0
  key_name               = "ZCKey-${var.environment}"
  vpc_security_group_ids = ["${aws_security_group.jumphost.id}"]
  tags = {
    env = "${var.environment}"
  }
}

resource "aws_security_group" "jumphost" {
  name        = "cluster-${var.environment}-jumphost"
  description = "Jumphost security group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

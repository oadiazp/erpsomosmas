resource "random_password" "pgsql_password" {
  length = 20
  special = false
}

resource "aws_db_instance" "pgsql" {
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "postgres"
  instance_class         = "db.t2.micro"
  name                   = "${var.environment}"
  username               = "postgres"
  password               = "${random_password.pgsql_password.result}"
  db_subnet_group_name   = "${aws_db_subnet_group.db.name}"
  skip_final_snapshot    = true
  count                  = "${var.create_db ? 1 : 0}"
  vpc_security_group_ids = [
    "${aws_security_group.jumphost.id}",
    "${aws_security_group.cluster.id}",
    "${aws_security_group.db.id}"
  ]
}

resource "aws_security_group" "db" {
  name        = "sftp-${var.environment}-db"
  description = "DB security group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = "${concat(var.cidrs_private, var.cidrs_public)}"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_db_subnet_group" "db" {
  subnet_ids = module.vpc.private_subnets
  name       = "sftp-${var.environment}-db"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_subnet" "redis-subnet" {
  vpc_id            = "${module.vpc.vpc_id}"
  cidr_block        = "${var.redis_subnet_cidr}"
}

resource "aws_elasticache_subnet_group" "redis-subnet-group" {
  name       = "cache-${var.environment}-subnet"
  subnet_ids = ["${aws_subnet.redis-subnet.id}"]
}

resource "aws_security_group" "redis" {
  name        = "sftp-${var.environment}-redis"
  description = "DB security group"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = "${concat(var.cidrs_private, var.cidrs_public)}"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "sftp-${var.environment}"
  engine               = "redis"
  node_type            = "cache.t2.micro"
  num_cache_nodes      = 1
  port                 = 6379
  subnet_group_name    = "${aws_elasticache_subnet_group.redis-subnet-group.name}"
  count                = "${var.create_redis ? 1 : 0}"
  security_group_ids   = [
    "${aws_security_group.jumphost.id}",
    "${aws_security_group.cluster.id}",
    "${aws_security_group.redis.id}"
  ]
}
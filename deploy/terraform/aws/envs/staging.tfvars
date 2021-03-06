environment       = "staging"
cidr_vpc          = "10.0.0.0/16"
cidrs_private     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
cidrs_public      = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
region            = "us-east-1"
ssl_cert_arn      = "arn:aws:acm:us-east-1:227172279387:certificate/d4df632e-7bb8-4bf1-a43c-5b92e763659a"
instance_type     = "t2.small"
nodes_amount      = 3
redis_subnet_cidr = "10.0.7.0/24"
create_db         = false
create_redis      = false

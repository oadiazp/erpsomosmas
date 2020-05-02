provider "aws" {
  version = ">= 2.28.1"
  region  = var.region
  profile = "bj"
}

provider "random" {
  version = "~> 2.1"
}

provider "local" {
  version = "~> 1.2"
}

provider "null" {
  version = "~> 2.1"
}

output "cluster-private-ips" {
  value = "${aws_instance.cluster_node.*.private_ip}"
}


output "cluster-public-ips" {
  value = "${aws_instance.cluster_node.*.public_ip}"
}


output "jumphost" {
  value = "${aws_instance.jumphost.public_ip}"
}

output "bucket" {
  value = "${aws_s3_bucket.videos-storage.bucket_domain_name}"
}

//output "pgsql" {
//  value = "${var.create_db ? aws_db_instance.pgsql.address: 0}"
//}
//
//output "redis" {
//  value = "${var.create_redis ? aws_elasticache_cluster.redis.cache_nodes : 0}"
//}

output "pgsql_passwd" {
  value = "${random_password.pgsql_password.result}"
}
output "ecs_cluster_name" {
  value = aws_ecs_cluster.discord_bot_cluster.name
}

output "ecs_service_name" {
  value = aws_ecs_service.discord_bot_service.name
}

output "cloudwatch_log_group" {
  value = aws_cloudwatch_log_group.discord_bot.name
}
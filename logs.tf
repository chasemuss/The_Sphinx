resource "aws_cloudwatch_log_group" "discord_bot" {
  name              = "/ecs/discord-bot"
  retention_in_days = 30
  tags = {
    Project = "Discord_Bot"
  }
}
variable "ecr_repository_url" {
  description = "URL of your ECR repository"
  type        = string
}

variable "discord_bot_token" {
  description = "Discord Bot Token"
  type        = string
  sensitive   = true
}
resource "aws_ecs_cluster" "discord_bot_cluster" {
  name = "discord-bot-cluster"
  tags = {
    Project = "Discord_Bot"
  }
}

resource "aws_ecs_task_definition" "discord_bot" {
  family                   = "discord-bot-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"  # 0.25 vCPU
  memory                   = "512"  # 0.5GB
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([{
    name  = "discord-bot"
    image = var.ecr_repository_url
    essential = true
    environment = [
      {
        name  = "DISCORD_TOKEN"
        value = var.discord_bot_token
      }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/discord-bot"
        "awslogs-region"        = "us-east-2"  # Changed to us-east-2
        "awslogs-stream-prefix" = "discord"
      }
    }
  }])

  depends_on = [aws_cloudwatch_log_group.discord_bot]

  tags = {
    Project = "Discord_Bot"
  }
}

resource "aws_ecs_service" "discord_bot_service" {
  name            = "discord-bot-service"
  cluster         = aws_ecs_cluster.discord_bot_cluster.id
  task_definition = aws_ecs_task_definition.discord_bot.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.discord_bot_sg.id]
    assign_public_ip = true
  }

  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  depends_on = [aws_iam_role_policy_attachment.ecs_execution_policy, aws_cloudwatch_log_group.discord_bot]

  tags = {
    Project = "Discord_Bot"
  }
}
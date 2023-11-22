module "authors_api_image_registry" {
  source          = "terraform-aws-modules/ecr/aws"
  repository_name = "authors-api"
  repository_read_access_arns = [module.iam_authors_api_role.iam_role_arn]
  repository_force_delete = true
  repository_policy = jsonencode({
    Version =  "2012-10-17",
    Statement: []
  })

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 10 images",
        selection = {
          tagStatus     = "tagged",
          tagPrefixList = ["v"],
          countType     = "imageCountMoreThan",
          countNumber   = 10
        },
        action = {
          type = "expire"
        }
      }
    ]
  })

  tags = {
    Terraform   = "true"
    App         = "authors-api"
  }
  
  depends_on = [ module.iam_authors_api_role ]
}

module "iam_authors_api_role" {
  source  = "yutaka0m/service-role/aws"
  version = "~> 1.0"

  iam_role_name = "AuthorsApi"

  trusted_entity = "build.apprunner.amazonaws.com"

  predefined_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"]
  
  tags = {
    Terraform = "true"
    App       = "authors-api"
  }
}

module "app_runner_authors_api" {
  source       = "terraform-aws-modules/app-runner/aws"
  service_name = "authors-api"

  create_instance_iam_role = false

  private_ecr_arn = module.iam_authors_api_role.iam_role_arn

  source_configuration = {
    auto_deployments_enabled = true

    authentication_configuration = {
      access_role_arn = module.iam_authors_api_role.iam_role_arn
    }

    image_repository = {

      image_configuration = {
        port = 8080
      }
      image_identifier = "${module.authors_api_image_registry.repository_url}:latest"
      image_repository_type = "ECR"
    }
  }

  enable_observability_configuration = false

  tags = {
    Terraform = "true"
    App       = "authors-api"
  }
}

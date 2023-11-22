
module "author_batch_resolver" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "author-batch-resolver"
  handler       = "index.handler"
  runtime       = "nodejs18.x"  
  source_path = "../graphql-api/author-batch-resolver"

  environment_variables = {
    AUTHORS_API_URL = module.app_runner_authors_api.service_url
  }

  tags = {
    Terraform = true
    App       = "graphql-api"
    Name      = "author-batch-resolver"
  }

  depends_on = [ module.app_runner_authors_api ]
}

module "graphql_api" {
  source = "terraform-aws-modules/appsync/aws"
  name = "graphql-api"
  schema = file("../graphql-api/schema.graphql")
  visibility = "GLOBAL"

  api_keys = {
    default = null # such key will expire in 7 days
  }

  additional_authentication_provider = {
    iam = {
      authentication_type = "AWS_IAM"
    }

    openid_connect_1 = {
      authentication_type = "OPENID_CONNECT"

      openid_connect_config = {
        issuer    = "https://www.issuer1.com/"
        client_id = "client_id1"
      }
    }
  }

  datasources = {
    autor_batch_ds_resolver = {
      type         = "AWS_LAMBDA"
      function_arn = module.author_batch_resolver.lambda_function_arn
    }

    books_api = {
      type     = "HTTP"
      endpoint = module.app_runner_books_api.service_url
    }

    authors_api = {
      type     = "HTTP"
      endpoint = module.app_runner_authors_api.service_url
    }
  }

  resolvers = {
    "Book.Author" = {
      Kind = "UNIT"
      type =  "Query"
      code = file("../graphql-api/query-resolvers/queryBatchAuthors.js")
      field = "queryAuthors"
      runtime = {
        name = "APPSYNC_JS"
        runtime_version = "1.0.0"
      }
      data_source   = "autor_batch_ds_resolver"
      max_batch_size = 100
    }

    "Query.queryAuthors" = {
      Kind = "UNIT"
      type =  "Query"
      code = file("../graphql-api/query-resolvers/queryAuthors.js")
      field = "queryAuthors"
      runtime = {
        name = "APPSYNC_JS"
        runtime_version = "1.0.0"
      }
      data_source = "authors_api"
    }

    "Query.queryAuthor" = {
      Kind = "UNIT"
      type =  "Query"
      code = file("../graphql-api/query-resolvers/queryAuthors.js")
      field = "queryAuthor"
      runtime = {
        name = "APPSYNC_JS"
        runtime_version = "1.0.0"
      }
      data_source = "authors_api"
    }

    "Query.queryBooks" = {
      Kind = "UNIT"
      type =  "Query"
      code = file("../graphql-api/query-resolvers/queryBooks.js")
      field = "queryBooks"
      runtime = {
        name = "APPSYNC_JS"
        runtime_version = "1.0.0"
      }
      data_source = "books_api"
    }

    "Query.queryBook" = {
      Kind = "UNIT"
      type =  "Query"
      code = file("../graphql-api/query-resolvers/queryBook.js")
      field = "queryBook"
      runtime = {
        name = "APPSYNC_JS"
        runtime_version = "1.0.0"
      }
      data_source = "books_api"
    }


  }

  tags = {
    Terraform = true
    App       = "graphql-api"
  }

  depends_on = [module.author_batch_resolver, module.app_runner_authors_api, module.app_runner_books_api]
}

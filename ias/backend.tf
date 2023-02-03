terraform {
  backend "remote" {
    organization = "itclever"
    token = "TF_TOKEN_FOR_TF_CLOUD"
    workspaces {
      name = "aws-demo-myfunc"
    }
  }

  required_version = ">= 0.14.0"
}
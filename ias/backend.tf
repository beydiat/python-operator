terraform {
  backend "remote" {
    organization = "itclever"

    workspaces {
      name = "aws-demo-myfunc"
    }
  }

  required_version = ">= 0.14.0"
}
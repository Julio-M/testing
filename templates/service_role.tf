module "template_service_script_role" {
    source      = "cloudposse/eks-iam-role/aws"
    version     = ">= 0.11.1"

    aws_account_number          = data.aws_caller_identity.current.account_id
    eks_cluster_oidc_issuer_url = var.cluster_oidc_issuer_url

    # Create a role for the service account named `template_service_script` in the Kubernetes namespace `template_service_script`
    service_account_name      = "${var.environment_code}-${var.resource_region}-template-service-script-sa"
    service_account_namespace = "template-service-script"
    # JSON IAM policy document to assign to the service account role
    aws_iam_policy_document   = [data.aws_iam_policy_document.template_service_script.json]
    }

    data "aws_iam_policy_document" "template_service_script" {
    statement {
        sid = "AllowAllOnS3Objects"

        actions = [
        "s3:*"
        ]

        effect    = "Allow"
        resources = ["*"]
    }
    }
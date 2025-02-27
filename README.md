# Cloud Engineer Guardrail Challenge: SQS Security Compliance



## Deployment Instructions:
  1. First we can set up a GitHub Actions pipeline using the file .github/workflows/deploy.yml.

  2. This file contains mainly two stages:

   a. The first step is a validation job where we make sure that both CloudFormation template and lambda function code is valid and safe through some libraries like black and flake8.

   b. Once the code is validated we can proceed to create our CloudFormation stack based on our template and push the lambda code to an S3 bucket.

   c. Once lambda code is pushed, the CloudFormation Stack can pick up this source code to create the lambda resource along with the other necessary resources like Event Bridge rule and IAM roles.


## Design Decisions:
  - My approach for the permission boundary is to restrict permissions only to allow the necessary API calls and not allowing write permissions in order to avoid any unintended resource deletion or modification. We can also deploy a Stack Set throught the organization together with the required roles and policies so we can create all the resources in every desired account and implement the solution across the whole organization.


- **File Structure:**

  ```
  /CloudGuardRailChallenge.zip
  ├── README.md
  ├── template.yaml         # CloudFormation template in YAML
  └── lambda_function
      └── lambda_function.py  # Python Lambda code
  ```

- **Submission:**  
  - Fork this GitHub repository for this test.
  - Commit your changes and submit a pull request for evaluation.

#draft

1. Create a new Google Cloud project.

2. Enable the Compute Engine API.

3. Clone the repository:
git clone https://github.com/oriasnoi/temp-tsks
cd temp-tsks

4. Edit the terraform.tfvars file.

5. Initialize and apply the Terraform configuration:
terraform init
terraform apply

6. Run:
telnet <GCP-VM-EXTERNAL-IP> 5432

7. PostgreSQL Kaboom!!

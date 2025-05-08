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

8. Some notes:

$ sudo netstat -tuln
	Proto Recv-Q Send-Q Local Address           Foreign Address         State      
	tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
	tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN     
	tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN
	udp        0      0 127.0.0.1:323           0.0.0.0:*                          
	udp        0      0 0.0.0.0:68              0.0.0.0:*

$ PG_VERSION=$(psql -V | awk '{print $3}' | cut -d. -f1) #13
$ CONF_DIR="/etc/postgresql/$PG_VERSION/main"
$ echo "listen_addresses = '*'" | sudo tee -a $CONF_DIR/postgresql.conf
$ echo "host all all 0.0.0.0/0 md5" | sudo tee -a $CONF_DIR/pg_hba.conf
$ sudo systemctl restart postgresql

$ sudo netstat -tuln
	Proto Recv-Q Send-Q Local Address           Foreign Address         State      
	tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
	tcp        0      0 0.0.0.0:5432            0.0.0.0:*               LISTEN     
	tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN
	udp        0      0 127.0.0.1:323           0.0.0.0:*                          
	udp        0      0 0.0.0.0:68              0.0.0.0:*

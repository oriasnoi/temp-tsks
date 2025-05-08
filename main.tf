provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

resource "google_compute_firewall" "postgres_firewall" {
  name    = "allow-postgres"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-postgres"]
}

resource "google_compute_firewall" "ssh_firewall" {
  name    = "allow-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-ssh"]
}

resource "google_compute_instance" "default" {
  name         = "postgres-vm"
  machine_type = "e2-micro"
  zone         = var.zone

  tags = ["allow-postgres", "allow-ssh]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name

    access_config {
      # Ephemeral external IP
    }
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install -y postgresql

    PG_VERSION=$(psql -V | awk '{print $3}' | cut -d. -f1,2)
    CONF_DIR="/etc/postgresql/$PG_VERSION/main"

    echo "listen_addresses = '*'" >> $CONF_DIR/postgresql.conf
    echo "host all all 0.0.0.0/0 md5" >> $CONF_DIR/pg_hba.conf

    systemctl restart postgresql
  EOF
}

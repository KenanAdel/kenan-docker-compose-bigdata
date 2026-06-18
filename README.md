# Comprehensive Big Data Learning Lab Environment

Welcome to your Python-first, multi-architecture Big Data Learning Lab. This environment integrates Apache Hadoop, Hive, Spark, Kafka, NiFi, Airflow, Iceberg, ClickHouse and Jupyter into a single, flawless grid. 

##  Architecture & Universal Connectors

This infrastructure has been strictly optimized for **Python-based Omni-Connectivity**. 
The "Universal Connector Strategy" guarantees that Jupyter Notebook and Apache Spark can communicate natively with any tool in the grid out of the box.

### Key Architectural Fixes & Optimizations
1. **Global Spark Configuration (`spark-defaults.conf`)**: All Spark runtime packages (Kafka, Iceberg, Postgres, ClickHouse) and catalog settings are centrally injected via a global `./conf/spark-defaults.conf` file. This file is bind-mounted directly into the Master, Worker, and Jupyter instances. As a result, you can launch PySpark sessions instantly without supplying any `.config()` or `--packages` boilerplate.


##  Deployment Guide

### Repository Folder Structure
For this project to run properly, ensure the following directory structure and files are present in the root of the repository before launching the cluster:

```text
.
├── Documentation.txt       # Advanced troubleshooting & cluster architecture reference
├── README.md               # Main project documentation
├── docker-compose.yaml     # The core infrastructure definition file
├── dags/                   # Apache Airflow DAGs (Workflows)
│   ├── test_airflow_grid.py    # Airflow connectivity test DAG
│   └── test_timezone_grid.py   # Airflow timezone testing DAG
├── logs/                   # Apache Airflow execution logs (auto-generated)
├── plugins/                # Apache Airflow custom plugins (empty by default)
├── jdbc/                   # Offline JDBC drivers
│   └── postgresql.jar      # Required for Hive Metastore to connect to PostgreSQL
├── conf/                   # Global configuration files
│   ├── spark-defaults.conf # Centralized Spark configurations injected into all nodes
│   ├── core-site.xml       # Hadoop Core configuration (Injected into NiFi)
│   └── hdfs-site.xml       # Hadoop HDFS configuration (Injected into NiFi)
└── notebooks/              # Jupyter Notebooks workspace
    ├── Iceberg.ipynb       # Iceberg testing notebook
    ├── Kafka.ipynb         # Kafka Streaming testing notebook
    ├── ClickHouse.ipynb    # ClickHouse connectivity notebook
    └── CSV.ipynb           # Standard data manipulation notebook
```

### Prerequisites
- Docker Engine & Docker Compose installed.
- Ensure at least 12GB+ of RAM allocated to Docker for this grid.

#### Included Offline Dependencies (JDBC Driver)
All required JDBC drivers and JAR files (including the PostgreSQL driver `postgresql-42.7.3.jar`) are already included in the `./jdbc` directory inside this repository. You do not need to download them manually.

**Volume Mapping Structure**: This `./jdbc` local directory is mapped directly into the Apache Hive components (`hive-init`, `hive-metastore`, `hive-server2`) via a Docker bind mount (`./jdbc:/opt/hive/lib/custom_jdbc`). This bypasses the need for an internet connection when the containers boot.

### 1. Launch the Cluster
Open a terminal in the directory containing `docker-compose.yaml` and run:

```bash
docker-compose up -d
```

### 2. Verify Health Status
Due to the dependency checks, the containers will boot in the correct sequence. Wait about 2-3 minutes, then verify everything is `healthy`:
```bash
docker-compose ps
```
Ensure there are no containers showing `(unhealthy)` or `Exit`.

### 3. Accessing the UI Interfaces

| Service | Address | Credentials / Info |
|---|---|---|
| **Jupyter Notebook** | `http://localhost:8888` | No password required. Open-grid access. |
| **Apache Airflow** | `http://localhost:8085` | User: `admin`, Password: `admin` |
| **Hadoop NameNode** | `http://localhost:9870` | Browse HDFS Filesystem |
| **Hadoop ResourceManager**| `http://localhost:8088` | Monitor YARN Jobs |
| **Spark Master** | `http://localhost:8081` | Monitor Spark Cluster Jobs |
| **Kafka UI** | `http://localhost:8090` | View Topics and Streams |
| **Apache NiFi** | `https://localhost:8443` | User: `admin`, Password: `SuperSecretPassword123!` (Note:HTTPS) |
| **ClickHouse** | `http://localhost:8123` | Native OLAP Analytics (User: `clickhouse`, Password: `clickhouse`, TCP: `9001`) |

##  Visual Data Ingestion via Apache NiFi

Apache NiFi is deployed to visually design data routing pipelines.
- **Access**: Navigate to [https://localhost:8443](https://localhost:8443) (Bypass the self-signed certificate warning).
- **Credentials**: Username: `admin` | Password: `SuperSecretPassword123!`

### Example Pipeline: Generate -> Kafka -> HDFS
To build a seamless pipeline routing generated data to both Kafka and HDFS, configure your processors as follows:

1. **GenerateFlowFile**:
   - Generates sample payload records (e.g., JSON) to initiate the flow.

2. **PublishKafka_2_6**:
   - **Kafka Brokers**: `kafka:9092` (Routes via the internal Docker bridge).
   - **Topic Name**: `sensor_data` (Must match your Kafka topic).
   - **Use Transactions**: `false` *(Critical Best Practice: Prevents `InitProducerId` timeouts and guarantees fluid delivery without transaction bottlenecking in lightweight grids).*
   - **Delivery Guarantee**: `1` or `all`.

3. **PutHDFS**:
   - **Hadoop Configuration Resources**: `/opt/nifi/nifi-current/conf/core-site.xml,/opt/nifi/nifi-current/conf/hdfs-site.xml` *(These topology files are pre-injected into the container).*
   - **Directory**: `/user/nifi/data`
   - **Conflict Resolution Strategy**: `replace` or `ignore`.

---

##  Testing the Universal Connectivity

**Zero Boilerplate Workflow:** Thanks to the `./conf/spark-defaults.conf` global injection, you do *not* need to pass `.config()` or `--packages` inside your notebooks anymore. Iceberg, ClickHouse, Postgres, and Kafka plugins are natively pre-baked!

### Universal Connectivity Notebooks

All connection tests are already created and saved inside the `notebooks` directory of this repository. To run them, simply open Jupyter Notebook (`http://localhost:8888`) and execute the following test notebooks:

- **`Iceberg.ipynb`**: Tests Jupyter to HDFS & Iceberg using the global 'hive_prod' catalog.
- **`Kafka.ipynb`**: Tests native Kafka Streaming integration (writing and reading).
- **`ClickHouse.ipynb`**: Tests Jupyter to ClickHouse natively via PySpark JDBC.
- **`CSV.ipynb`**: Standard data manipulation and file saving tests.

Happy Engineering!

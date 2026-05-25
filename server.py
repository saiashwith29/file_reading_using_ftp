from sqlalchemy import create_engine

# =====================================================
# SQL SERVER
# =====================================================

server_name = "172.16.206.111"
database_name = "Sai_Test"

username = "sa"
password = "Yp#Di$S8GhML%2T6X*Ax"

# =====================================================
# FTP / SFTP
# =====================================================

ftp_host = "sparkling-water-50295.sftptogo.com"
ftp_port = 22

ftp_username = "DHR_Test_User"
ftp_password = "sU9cYZAcMLS3CeJkbSTHzDfiP4LxKsXFhl66MFWq"

ftp_file_path = "/Today/transfer_real_1gb_data.csv"

# =====================================================
# TABLE
# =====================================================

table_name = "da"

# =====================================================
# PERFORMANCE
# =====================================================

READ_CHUNK_SIZE = 10000

SQL_BATCH_SIZE = 1000

# =====================================================
# OPTIONS
# =====================================================

create_new_table = True
create_new_columns = True

# =====================================================
# PERFORMANCE
# =====================================================

READ_CHUNK_SIZE = 50000
INSERT_CHUNK_SIZE = 50000

# =====================================================
# SQL ENGINE
# =====================================================

connection_string = (
    f"mssql+pyodbc://{username}:{password}"
    f"@{server_name}/{database_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(
    connection_string,
    fast_executemany=True
)

# =====================================================
# MOVE FILE SETTINGS
# =====================================================

MOVE_FILE_AFTER_SUCCESS = True

archive_folder = "/Test/Archive"
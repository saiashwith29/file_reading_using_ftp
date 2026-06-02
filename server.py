from sqlalchemy import create_engine

# =====================================================
# SQL
# =====================================================

server_name = " 172.16.206.111"
database_name = "Sai_Test"

username = "sa"
password = "Yp#Di$S8GhML%2T6X*Ax"

# =====================================================
# FTP
# =====================================================

ftp_host = "sparkling-water-50295.sftptogo.com"
ftp_port = 22

ftp_username = "DHR_Test_User"
ftp_password = "sU9cYZAcMLS3CeJkbSTHzDfiP4LxKsXFhl66MFWq"

# =====================================================
# FILES
# =====================================================

FILES_TO_PROCESS = [

    {
        "ftp_file_path": "/Today/airports.json",
        "table_name": "table10",
        "create_new_table": True,
        "create_new_columns": True
    },
    # {
    #     "ftp_file_path": "/Today/future_Orders_20260408.csv",
    #     "table_name": "table2",
    #     "create_new_table": True,
    #     "create_new_columns": True
    # },
    # {
    #     "ftp_file_path": "/Today/future_Orders_20260409.csv",
    #     "table_name": "table3",
    #     "create_new_table": True,
    #     "create_new_columns": True
    # },
    # {
    #     "ftp_file_path": "/Today/future_Orders_20260410.csv",
    #     "table_name": "table4",
    #     "create_new_table": True,
    #     "create_new_columns": True
    # },
    # {
    #     "ftp_file_path": "/Today/future_Orders_20260413.csv",
    #     "table_name": "table5",
    #     "create_new_table": True,
    #     "create_new_columns": True
    # }
]

# =====================================================
# PERFORMANCE
# =====================================================

READ_CHUNK_SIZE = 50000

SQL_BATCH_SIZE = 5000

INSERT_CHUNK_SIZE = 5000

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
# ARCHIVE
# =====================================================

archive_folder = "/Today/Archive"


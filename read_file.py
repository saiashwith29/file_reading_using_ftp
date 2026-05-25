import pandas as pd
import paramiko
import tempfile
import json
import io,os

from server import (
    ftp_host,
    ftp_port,
    ftp_username,
    ftp_password,
    ftp_file_path,
    READ_CHUNK_SIZE
)

# =====================================================
# READ FILE
# =====================================================

def read_any_file():

    print("\nCONNECTING TO SFTP...\n")

    # =====================================================
    # CONNECT SFTP
    # =====================================================

    transport = paramiko.Transport(
        (ftp_host, ftp_port)
    )

    transport.connect(
        username=ftp_username,
        password=ftp_password
    )

    sftp = paramiko.SFTPClient.from_transport(
        transport
    )

    print("\nSFTP CONNECTED!\n")

    # =====================================================
    # FILE EXTENSION
    # =====================================================

    extension = (
        ftp_file_path
        .split(".")[-1]
        .lower()
    )

    # =====================================================
    # DOWNLOAD FILE TO TEMP
    # =====================================================

    print("\nDOWNLOADING FILE...\n")

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{extension}"
    )

    sftp.getfo(
        ftp_file_path,
        temp_file
    )

    temp_file.close()

    print("\nDOWNLOAD COMPLETED!\n")

    # =====================================================
    # CLOSE FTP
    # =====================================================

    sftp.close()

    transport.close()

    # =====================================================
    # READ CSV
    # =====================================================

    print("\nREADING FILE...\n")

    if extension == "csv":

        chunks = pd.read_csv(
            temp_file.name,
            dtype=str,
            encoding="latin1",
            engine="c",
            chunksize=READ_CHUNK_SIZE,
            low_memory=False
        )

        return chunks, extension, temp_file.name

    # =====================================================
    # READ EXCEL
    # =====================================================

    elif extension in ["xlsx", "xls"]:

        df = pd.read_excel(
            temp_file.name,
            dtype=str
        )

        return df, extension, temp_file.name

    # =====================================================
    # READ JSON
    # =====================================================

    elif extension == "json":

        with open(
            temp_file.name,
            "r",
            encoding="latin1"
        ) as f:

            json_data = json.load(f)

        if isinstance(json_data, list):

            df = pd.DataFrame(json_data)

        elif isinstance(json_data, dict):

            df = pd.DataFrame([json_data])

        else:

            raise Exception(
                "Unsupported JSON format"
            )

        return df, extension, temp_file.name

    # =====================================================
    # UNSUPPORTED
    # =====================================================

    else:

        raise Exception(
            f"Unsupported file type: {extension}"
        )
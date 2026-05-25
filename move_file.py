import posixpath
import paramiko

from server import (
    ftp_host,
    ftp_port,
    ftp_username,
    ftp_password,
    ftp_file_path,
    archive_folder
)

# =====================================================
# MOVE FILE TO ARCHIVE
# =====================================================

def move_file_to_archive():

    print("\nMOVING FILE TO ARCHIVE...\n")

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

    # =====================================================
    # FILE NAME
    # =====================================================

    file_name = posixpath.basename(
        ftp_file_path
    )

    # =====================================================
    # NEW FILE NAME
    # =====================================================

    archive_file_name = (
        "transfer_" + file_name
    )

    # =====================================================
    # DESTINATION PATH
    # =====================================================

    destination_path = posixpath.join(
        archive_folder,
        archive_file_name
    )

    # =====================================================
    # MOVE + RENAME
    # =====================================================

    sftp.rename(
        ftp_file_path,
        destination_path
    )

    print(
        f"\nFILE MOVED TO:\n{destination_path}"
    )

    sftp.close()

    transport.close()

    print("\nARCHIVE COMPLETED!\n")
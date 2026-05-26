import time
import os
import pandas as pd

from read_file import read_any_file

from sql import insert_into_sql

from move_file import move_file_to_archive

from server import (
    FILES_TO_PROCESS,
    engine
)

# =====================================================
# START TIMER
# =====================================================

start_time = time.time()

print("\nSTARTING ETL PROCESS...\n")

# =====================================================
# PROCESS EACH FILE
# =====================================================

for file_config in FILES_TO_PROCESS:

    ftp_file_path = file_config["ftp_file_path"]

    table_name = file_config["table_name"]

    create_new_table = file_config["create_new_table"]

    create_new_columns = file_config["create_new_columns"]

    temp_file_path = None

    try:

        print(f"\nPROCESSING FILE: {ftp_file_path}\n")

        # =====================================================
        # READ FILE
        # =====================================================

        data, extension, temp_file_path = read_any_file(
            ftp_file_path
        )

        total_rows = 0

        # =====================================================
        # CSV
        # =====================================================

        if extension == "csv":

            first_chunk = True

            for chunk in data:

                if chunk is None:
                    continue

                if chunk.empty:
                    continue

                rows = len(chunk)

                total_rows += rows

                print(
                    f"\nPROCESSING {rows} ROWS...\n"
                )

                insert_into_sql(
                    chunk=chunk,
                    engine=engine,
                    table_name=table_name,
                    first_chunk=first_chunk,
                    create_new_table=create_new_table,
                    create_new_columns=create_new_columns
                )

                first_chunk = False

        # =====================================================
        # EXCEL / JSON
        # =====================================================

        else:

            chunk = data

            if chunk is not None and not chunk.empty:

                rows = len(chunk)

                total_rows += rows

                print(
                    f"\nPROCESSING {rows} ROWS...\n"
                )

                insert_into_sql(
                    chunk=chunk,
                    engine=engine,
                    table_name=table_name,
                    first_chunk=True,
                    create_new_table=create_new_table,
                    create_new_columns=create_new_columns
                )

        # =====================================================
        # MOVE FILE AFTER SUCCESS
        # =====================================================

        move_file_to_archive(
            ftp_file_path
        )

        print(
            f"\nTOTAL ROWS INSERTED: "
            f"{total_rows}"
        )

        print(
            f"\nFILE COMPLETED: "
            f"{ftp_file_path}"
        )

    # =====================================================
    # ERROR
    # =====================================================

    except Exception as e:

        print("\nFILE FAILED!\n")

        print(str(e))

    # =====================================================
    # ALWAYS DELETE TEMP FILE
    # =====================================================

    finally:

        try:

            if (
                temp_file_path
                and
                os.path.exists(temp_file_path)
            ):

                os.remove(temp_file_path)

                print(
                    "\nTEMP FILE DELETED "
                    "SUCCESSFULLY!\n"
                )

        except Exception as delete_error:

            print(
                "\nFAILED TO DELETE TEMP FILE:\n"
            )

            print(str(delete_error))

# =====================================================
# END TIMER
# =====================================================

end_time = time.time()

print(
    f"\nTOTAL ETL TIME: "
    f"{end_time - start_time:.2f} seconds"
)

print("\nETL PROCESS COMPLETED!\n")


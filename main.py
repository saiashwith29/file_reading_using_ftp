import time
import pandas as pd

from server import (
    engine,
    table_name
)

from read_file import read_any_file

from sql import insert_into_sql

from move_file import move_file_to_archive

# =====================================================
# START TIMER
# =====================================================

start_time = time.time()

print("\nSTARTING ETL PROCESS...\n")

# =====================================================
# TOTAL ROW COUNTER
# =====================================================

total_rows = 0

# =====================================================
# READ FILE
# =====================================================

data, extension, temp_file_path = read_any_file()

# =====================================================
# CSV FILE
# =====================================================

if extension == "csv":

    first_chunk = True

    for chunk in data:

        # SKIP EMPTY CHUNKS
        if chunk is None:
            continue

        if len(chunk) == 0:
            continue

        # ROW COUNT
        chunk_rows = len(chunk)

        total_rows += chunk_rows

        print(
            f"\nPROCESSING {chunk_rows} ROWS...\n"
        )

        # INSERT INTO SQL
        insert_into_sql(
            chunk=chunk,
            engine=engine,
            table_name=table_name,
            first_chunk=first_chunk
        )

        first_chunk = False

# =====================================================
# EXCEL / JSON
# =====================================================

elif extension in ["xlsx", "xls", "json"]:

    chunk = data

    if chunk is not None and len(chunk) > 0:

        chunk_rows = len(chunk)

        total_rows += chunk_rows

        print(
            f"\nPROCESSING {chunk_rows} ROWS...\n"
        )

        insert_into_sql(
            chunk=chunk,
            engine=engine,
            table_name=table_name,
            first_chunk=True
        )

# =====================================================
# UNSUPPORTED
# =====================================================

else:

    raise Exception(
        f"Unsupported extension: {extension}"
    )

# =====================================================
# END TIMER
# =====================================================

end_time = time.time()

# =====================================================
# TOTAL TIME
# =====================================================

total_time = (
    end_time - start_time
)

print(
    f"\nTOTAL ROWS INSERTED: {total_rows}"
)

print(
    f"\nTOTAL TIME: {total_time:.2f} seconds"
)

# =====================================================
# MOVE FILE TO ARCHIVE
# =====================================================

move_file_to_archive()

# =====================================================
# DONE
# =====================================================

import os

if os.path.exists(temp_file_path):

    os.remove(temp_file_path)

    print("\nTEMP FILE DELETED!\n")

    
print(
    "\nETL COMPLETED SUCCESSFULLY!\n"
)
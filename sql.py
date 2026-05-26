import pandas as pd
import traceback

from sqlalchemy import inspect
from sqlalchemy import text

from server import (
     INSERT_CHUNK_SIZE
)

# =====================================================
# INSERT INTO SQL SERVER
# =====================================================

def insert_into_sql(
    chunk,
    engine,
    table_name,
    first_chunk=False,
    create_new_table=True,
    create_new_columns=True
):

    try:

        print("\nPREPARING DATA...\n")

        # =====================================================
        # CLEAN COLUMN NAMES
        # =====================================================

        chunk.columns = (
            chunk.columns
            .astype(str)
            .str.strip()
        )

        # =====================================================
        # CLEAN DATA
        # =====================================================

        chunk.fillna(
            '',
            inplace=True
        )

        chunk = chunk.astype(str)

        chunk.replace(
            'nan',
            '',
            inplace=True
        )

        # =====================================================
        # SQL INSPECTOR
        # =====================================================

        inspector = inspect(engine)

        tables = inspector.get_table_names()

        # =====================================================
        # CREATE TABLE
        # =====================================================

        if first_chunk:

            if table_name not in tables:

                if create_new_table:

                    print(
                        "\nTABLE NOT FOUND "
                        "→ CREATING TABLE...\n"
                    )

                    chunk.head(0).to_sql(
                        name=table_name,
                        con=engine,
                        if_exists='replace',
                        index=False
                    )

                    print(
                        "\nTABLE CREATED SUCCESSFULLY!\n"
                    )

                else:

                    raise Exception(
                        f"TABLE {table_name} "
                        f"DOES NOT EXIST"
                    )

        # =====================================================
        # GET SQL COLUMNS
        # =====================================================

        inspector = inspect(engine)

        sql_columns = [
            col["name"]
            for col in inspector.get_columns(
                table_name
            )
        ]

        # =====================================================
        # NORMALIZE FUNCTION
        # =====================================================

        def normalize(col):

            return (
                str(col)
                .lower()
                .replace(" ", "")
                .replace("_", "")
            )

        # =====================================================
        # COLUMN MATCHING
        # =====================================================

        rename_map = {}

        for file_col in chunk.columns:

            for sql_col in sql_columns:

                if (
                    normalize(file_col)
                    ==
                    normalize(sql_col)
                ):

                    rename_map[file_col] = sql_col

        chunk.rename(
            columns=rename_map,
            inplace=True
        )

        # =====================================================
        # CREATE NEW COLUMNS
        # =====================================================

        if create_new_columns:

            extra_columns = [

                c for c in chunk.columns

                if c not in sql_columns
            ]

            if extra_columns:

                print(
                    "\nADDING NEW COLUMNS...\n"
                )

                with engine.begin() as conn:

                    for col in extra_columns:

                        try:

                            query = text(
                                f"""
                                ALTER TABLE {table_name}
                                ADD [{col}] VARCHAR(MAX)
                                """
                            )

                            conn.execute(query)

                            print(
                                f"ADDED COLUMN: {col}"
                            )

                        except Exception as e:

                            print(
                                f"FAILED COLUMN "
                                f"{col}: {e}"
                            )

                # refresh columns

                inspector = inspect(engine)

                sql_columns = [

                    col["name"]

                    for col in inspector.get_columns(
                        table_name
                    )
                ]

        # =====================================================
        # KEEP MATCHING COLUMNS ONLY
        # =====================================================

        chunk = chunk[
            [
                c for c in chunk.columns
                if c in sql_columns
            ]
        ]

        # =====================================================
        # REMOVE DUPLICATE COLUMNS
        # =====================================================

        chunk = chunk.loc[
            :,
            ~chunk.columns.duplicated()
        ]

        # =====================================================
        # EMPTY CHECK
        # =====================================================

        if chunk.empty:

            print("\nEMPTY CHUNK SKIPPED!\n")

            return

        # =====================================================
        # INSERT INTO SQL
        # =====================================================

        print(
            f"\nINSERTING "
            f"{len(chunk)} ROWS...\n"
        )

        try:

            chunk.to_sql(
                name=table_name,
                con=engine,
                if_exists='append',
                index=False,
                method=None,
                chunksize=INSERT_CHUNK_SIZE
            )

            print(
                "\nINSERT COMPLETED!\n"
            )

        except Exception as e:

            print(
                "\nSQL INSERT FAILED!\n"
            )

            print(str(e))

            engine.dispose()

            raise

    except Exception:

        print("\nERROR OCCURRED:\n")

        traceback.print_exc()

        raise
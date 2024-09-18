import subprocess
import time
import os


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connection" in result.stdout:
                print("successfully connected to postgrs")
                return True

        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("max retries reached. Exiting")
    return False


if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("Starting etl script")

source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'source_postgres'
}

destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'destination_postgres'
}

dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'
]

subprocess_env = dict(PGPASSWORD=source_config['password'])

subprocess.run(dump_command, env=subprocess_env, check=True)

load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql',
]

subprocess_env = dict(PGPASSWORD=destination_config['password'])
subprocess.run(load_command, env=subprocess_env, check=True)

print("Ending etl Script ...")


# source_config = {
#     'dbname': 'source_db',
#     'user': 'postgres',
#     'password': 'postgres',
#     'host': 'source_postgres'
# }
#
# destination_config = {
#     'dbname': 'destination_db',
#     'user': 'postgres',
#     'password': 'postgres',
#     'host': 'destination_postgres'
# }
#
# # Corrected dump command
# dump_command = [
#     'pg_dump',
#     '-h', source_config['host'],
#     '-U', source_config['user'],  # corrected
#     '-d', source_config['dbname'],
#     '-f', 'data_dump.sql',
#     '-w'
# ]
#
# # Combine existing environment variables with PGPASSWORD
# subprocess_env = {**os.environ, 'PGPASSWORD': source_config['password']}
#
# # Run the dump command
# try:
#     subprocess.run(dump_command, env=subprocess_env, check=True)
#     print("Data dump completed successfully.")
# except subprocess.CalledProcessError as e:
#     print(f"Failed to dump data: {e}")
#     exit(1)
#
# # Corrected load command
# load_command = [
#     'psql',
#     '-h', destination_config['host'],
#     '-U', destination_config['user'],  # corrected
#     '-d', destination_config['dbname'],
#     '-a', '-f', 'data_dump.sql',
# ]
#
# # Set the password for the destination database
# subprocess_env = {**os.environ, 'PGPASSWORD': destination_config['password']}
#
# # Run the load command
# try:
#     subprocess.run(load_command, env=subprocess_env, check=True)
#     print("Data load completed successfully.")
# except subprocess.CalledProcessError as e:
#     print(f"Failed to load data: {e}")
#     exit(1)
#
# print("Ending ETL script...")

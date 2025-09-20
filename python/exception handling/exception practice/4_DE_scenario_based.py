import os
import sqlite3
import pandas as pd
import requests
import json

# Data Engineering / Real-World Scenarios

# 31. Write a program that raises a custom exception if a data file is missing.
print("31. Write a program that raises a custom exception if a data file is missing.")
class DataFileMissingError(Exception):
    pass
try:
    file_path = "data_file.json"
    if os.path.exists(file_path):
        with open(file_path,"r",encoding="utf-8") as f:
            print(f.read())
    else:
        raise DataFileMissingError(f"Required data file not found: {file_path}")
except DataFileMissingError as fnf:
    print("ERROR:", fnf)
print("###########################################")

# 32. Write a program that raises exceptions when schema mismatch occurs in a dataset.
print("32. Write a program that raises exceptions when schema mismatch occurs in a dataset.")
class SchemaMismatchError(Exception):
    pass

expected_cols = {"id", "name", "age"}
dataset_cols = {"id", "fullname", "age"}  # actual columns in dataset
try:
    if dataset_cols != expected_cols:
        raise SchemaMismatchError(f"Expected {expected_cols}, but got {dataset_cols}")
    print("Schema matches. Proceed.")
except SchemaMismatchError as e:
    print("ERROR:", e)
print("###########################################")

# 33. Write a program that handles KeyError while accessing dictionary values in a dataset.
print("33. Write a program that handles KeyError while accessing dictionary values in a dataset.")
record = {"id": 1, "name": "Uditesh"}
try:
    # 'age' key does not exist → KeyError
    print("Age:", record["age"])
except KeyError as e:
    print(f"KeyError: Missing key {e} in record {record}")
print("###########################################")

# 34. Write a program to simulate ETL pipeline exception handling (Extract → Transform → Load).
print("34. Write a program to simulate ETL pipeline exception handling (Extract → Transform → Load).")
class MissingColumnError(Exception):
    pass

def extract(path_file):
    try:
        df = pd.read_csv(path_file)
        return df
    except FileNotFoundError as e:
        print("ERROR:", e)

def transform(df):
    required_cols = ["name", "age", "salary"]
    for col in required_cols:
        if col not in df.columns:
            raise MissingColumnError(f"Required column missing: {col}")
    df["name"].fillna("Anonymous",inplace=True)

    median_age = df["age"].median()
    df["age"].fillna(median_age, inplace=True)

    median_salary = df["salary"].median()
    df["salary"].fillna(median_salary, inplace=True)

    return df

def load(df):
    try:
        df.to_csv("transformed_data.csv", index=False)
    except Exception as e:
        print("Failed to save transformed data:", e)
try:
    path_file = "data.csv"
    raw = extract(path_file)
    print(raw)
    transformed = transform(raw)
    print(transformed)
    load(transformed)
except MissingColumnError as e:
    print("Transformation error:", e)
except Exception as e:
    print("Pipeline failed:", e)
print("###########################################")

# 35. Write a program to catch exceptions while reading data from an API.
print("35. Write a program to catch exceptions while reading data from an API.")

# The JSONPlaceholder API
# it’s free, public, and doesn’t need authentication.
url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    # 0.001 seconds timeout
    resp = requests.get(url, timeout=0.001)
    # raise HTTPError for 4xx/5xx   
    resp.raise_for_status()              
    # convert to dict
    data = resp.json()                   
    print("API Data:", data)
except requests.Timeout:
    print("Error: The request timed out.")
except requests.HTTPError as e:
    print("HTTP Error:", e)
except requests.RequestException as e:
    print("Other Request Error:", e)
print("###########################################")

# 36. Write a program to handle exceptions while connecting to Azure Blob Storage (mocked).
print("36. Write a program to handle exceptions while connecting to Azure Blob Storage (mocked).")
class AzureBlobConnectionError(Exception): 
    pass

def connect_to_blob(account_name, key):
    # simulate failure
    raise AzureBlobConnectionError("Invalid credentials or network issue")

try:
    connect_to_blob("myaccount", "badkey")
except AzureBlobConnectionError as e:
    print("Blob connection failed:", e)
print("###########################################")

# 37. Write a program that handles exceptions when reading from a corrupted JSON file.
print("37. Write a program that handles exceptions when reading from a corrupted JSON file.")

filename = "data.json"
try:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f) 
    print("Loaded data:", data)
except FileNotFoundError:
    print("File not found:", filename)
except json.JSONDecodeError as e:
    print("Corrupted JSON file:", e)
print("###########################################")

# 38. Write a program that raises an exception when duplicate data is found in a dataset.
print("38. Write a program that raises an exception when duplicate data is found in a dataset.")
class DuplicateDataError(Exception): 
    pass

records = [1, 2, 3, 3, 4]
try:
    if len(records) != len(set(records)):
        raise DuplicateDataError("Duplicate values found in dataset")
    print("No duplicates.")
except DuplicateDataError as e:
    print("ERROR! ", e)
print("###########################################")

# 39. Write a program to catch exceptions while writing data into SQL database.
print("39. Write a program to catch exceptions while writing data into SQL database.")
class DatabaseWriteError(Exception):
    pass

# sqlite3 → Python’s built-in library to work with SQLite, a lightweight database stored in 
# a single file (example.db).

# conn.cursor() → creates a cursor object, used to run SQL commands (like SELECT, INSERT).
# cursor = the messenger (person who goes inside, talks to the DB, and brings results back)
# conn.commit() → saves (commits) all changes you made into the database file.
def write_to_db(record):
    try:
        conn = sqlite3.connect("example.db")   # create/connect to DB file
        cur = conn.cursor()

        # create table if not exists
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")

        # try inserting record
        cur.execute("INSERT INTO users (id, name) VALUES (?, ?)", (record["id"], record["name"]))
        conn.commit()
        print("Record inserted:", record)

    except sqlite3.Error as e:   # catches database-related errors
        raise DatabaseWriteError(f"Database error: {e}")
    finally:
        conn.close()
try:
    write_to_db({"id": 1, "name": "Alice"})
    # this will raise UNIQUE constraint error
    write_to_db({"id": 1, "name": "Duplicate"})  
except DatabaseWriteError as e:
    print("Write error:", e)
print("###########################################")

# 40. Write a program that retries failed API requests 3 times using exception handling.
print("40. Write a program that retries failed API requests 3 times using exception handling.")

# httpbin is a free, public testing service for HTTP requests.
# Built by the same people who made the requests library.
url = "https://httpbin.org/status/500"
def retry_api_request(url, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=1)  # 1s timeout
            response.raise_for_status()  # raises HTTPError for bad responses (4xx, 5xx)
            return response.text  # success
        except requests.RequestException as e:
            attempt += 1
            if attempt < retries:
                print(f"Attempt {attempt}/{retries}: API request failed — Retrying...")
            else:
                print(f"Attempt {attempt}/{retries}: API request fail exhausted — No retries left.")
                # re-raise the original requests.RequestException
                raise  
try:
    print(retry_api_request(url, 3))
except Exception as e:
    print("Final error:", e)
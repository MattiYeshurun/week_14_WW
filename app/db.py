import pymysql
import dotenv
import pandas as pd
import os

def get_connect():
    conn = pymysql.connect(host=os.getenv("DB_HOST", "localhost")
                           , user=os.getenv("DB_USER", "user")
                           , password=os.getenv("DB_PASS", "secret_password"
                           , cursorclass=pymysql.cursors.DictCursor))
    return conn


def create_db(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS db_weapons")
    conn.select_db("db_weapons")
    conn.commit()
    cursor.close()


def create_tabel(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS weapon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    weapon_id VARCHAR(50),
    weapon_name VARCHAR(50),
    weapon_type VARCHAR(50),
    range_km INT ,
    weight_kg float, 
    manufacturer VARCHAR(50),
    origin_country VARCHAR(50),
    storage_location VARCHAR(50),
    year_estimated INT,
    risk_level VARCHAR(50))  """)
    conn.commit()
    cursor.close()

def insert_into_db(conn,data):
    cursor = conn.cursor()
    sql = """INSERT INTO weapon
        (weapon_id, weapon_name, weapon_type, range_km,
        weight_kg, manufacturer, origin_country,
        storage_location, year_estimated, risk_level)
        VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)
        """
    for d in data:
        cursor.execute(sql, (d['weapon_id'], d['weapon_name'], d['weapon_type'],
                            d['range_km'], d['weight_kg'], d['manufacturer'],
                            d['origin_country'], d['storage_location'],
                            d['year_estimated'], d['risk_level']))
    conn.commit()
    cursor.close()


def create_df(data):
    df = pd.DataFrame(data)
    return df

def analysis_range_km(df):
    df["risk_level"] =  pd.cut(x= df["range_km"] ,bins= [-int('inf'), 20, 100, 300, int('inf')] ,labels=["low", "medium", "high", "extreme"])
    return df

def replacing_missing_values(df):
    df["manufacturer"] = df["manufacturer"].fillna("Unknown")
    return df

get_connect()
import mysql.connector
import pandas as pd
from datetime import datetime
import os

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'shu',
    'password': 'CAROLjung77!',
    'database': 'oldman',
    'charset': 'utf8mb4'
}

# Import translations for frontend display
from translations import translate_column_name, get_translated_columns

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")
        return None

def execute_query(query, params=None, fetch=True):
    """Execute a database query"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
    except mysql.connector.Error as err:
        print(f"查询执行错误: {err}")
        if connection:
            connection.close()
        return None

def get_service_users():
    """Get all service users"""
    query = "SELECT * FROM service_users ORDER BY id"
    result = execute_query(query)
    if result:
        df = pd.DataFrame(result)
        return df
    return pd.DataFrame()

def get_service_users_translated():
    """Get all service users with translated column names for frontend"""
    df = get_service_users()
    if not df.empty:
        df.columns = get_translated_columns(df.columns)
    return df

def get_service_providers():
    """Get all service providers"""
    query = "SELECT * FROM service_providers ORDER BY id"
    result = execute_query(query)
    if result:
        df = pd.DataFrame(result)
        return df
    return pd.DataFrame()

def get_service_providers_translated():
    """Get all service providers with translated column names for frontend"""
    df = get_service_providers()
    if not df.empty:
        df.columns = get_translated_columns(df.columns)
    return df

def get_service_logs():
    """Get all service logs"""
    query = """
    SELECT sl.provider_id, sl.provider_name, sl.user_id, sl.user_name, 
           sl.time, sl.service_type, sl.duration, sl.image_data
    FROM service_logs sl 
    ORDER BY sl.time DESC
    """
    result = execute_query(query)
    if result:
        df = pd.DataFrame(result)
        return df
    return pd.DataFrame()

def get_service_logs_translated():
    """Get all service logs with translated column names for frontend"""
    df = get_service_logs()
    if not df.empty:
        df.columns = get_translated_columns(df.columns)
    return df

def get_family_accounts():
    """Get all family accounts"""
    query = "SELECT * FROM family_accounts ORDER BY user_id"
    result = execute_query(query)
    return pd.DataFrame()  # This table doesn't exist in current structure

def get_family_accounts_from_users():
    """Get family accounts from service_users table"""
    query = "SELECT id as user_id, guardian_user as username, guardian_pwd as password FROM service_users ORDER BY id"
    result = execute_query(query)
    if result:
        df = pd.DataFrame(result)
        return df
    return pd.DataFrame()

def get_family_accounts_translated():
    """Get family accounts with translated column names for frontend"""
    df = get_family_accounts_from_users()
    if not df.empty:
        df.columns = get_translated_columns(df.columns)
    return df

def get_admin_accounts():
    """Get all admin accounts"""
    query = "SELECT * FROM admin_accounts ORDER BY username"
    result = execute_query(query)
    if result:
        df = pd.DataFrame(result)
        return df
    return pd.DataFrame()

def get_admin_accounts_translated():
    """Get admin accounts with translated column names for frontend"""
    df = get_admin_accounts()
    if not df.empty:
        df.columns = get_translated_columns(df.columns)
    return df

def get_provider_accounts():
    """Get all provider accounts"""
    query = "SELECT * FROM provider_accounts ORDER BY provider_id"
    result = execute_query(query)
    return pd.DataFrame()  # This table doesn't exist in current structure

def get_provider_accounts_from_providers():
    """Get provider accounts from service_providers table"""
    query = "SELECT id as provider_id, username, password FROM service_providers ORDER BY id"
    result = execute_query(query)
    if result:
        df = pd.DataFrame(result)
        return df
    return pd.DataFrame()

def get_provider_accounts_translated():
    """Get provider accounts with translated column names for frontend"""
    df = get_provider_accounts_from_providers()
    if not df.empty:
        df.columns = get_translated_columns(df.columns)
    return df

def add_service_log(log_entry):
    """Add a new service log"""
    # Format datetime for MySQL
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Debug: Print the data types being sent
    print(f"Debug - Data types in add_service_log:")
    print(f"provider_id: {log_entry['provider_id']} (类型: {type(log_entry['provider_id'])})")
    print(f"user_id: {log_entry['user_id']} (类型: {type(log_entry['user_id'])})")
    print(f"provider_name: {log_entry['provider_name']} (类型: {type(log_entry['provider_name'])})")
    print(f"user_name: {log_entry['user_name']} (类型: {type(log_entry['user_name'])})")
    
    # Ensure all data types are correct for MySQL
    provider_id = int(log_entry['provider_id'])
    user_id = int(log_entry['user_id'])
    provider_name = str(log_entry['provider_name'])
    user_name = str(log_entry['user_name'])
    
    query = """
    INSERT INTO service_logs (provider_id, provider_name, user_id, user_name, time, service_type, duration, image_data)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        provider_id,
        provider_name,
        user_id,
        user_name,
        current_time,
        log_entry['service_type'],
        log_entry['duration'],
        log_entry.get('image_data', None)
    )
    return execute_query(query, params, fetch=False)

def add_service_user(user_data):
    """Add a new service user"""
    query = """
    INSERT INTO service_users (name, address, guardian_user, guardian_pwd)
    VALUES (%s, %s, %s, %s)
    """
    params = (
        user_data['name'],
        user_data['address'],
        user_data['guardian_user'],
        user_data['guardian_pwd']
    )
    return execute_query(query, params, fetch=False)

def add_service_provider(provider_data):
    """Add a new service provider"""
    query = """
    INSERT INTO service_providers (name, phone, role, username, password)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        provider_data['name'],
        provider_data['phone'],
        provider_data['role'],
        provider_data['username'],
        provider_data['password']
    )
    return execute_query(query, params, fetch=False)

def delete_service_user(user_id):
    """Delete a service user"""
    query = "DELETE FROM service_users WHERE id = %s"
    return execute_query(query, (user_id,), fetch=False)

def delete_service_provider(provider_id):
    """Delete a service provider"""
    query = "DELETE FROM service_providers WHERE id = %s"
    return execute_query(query, (provider_id,), fetch=False)

def delete_service_log(provider_id, user_id, time):
    """Delete a service log using composite key"""
    query = "DELETE FROM service_logs WHERE provider_id = %s AND user_id = %s AND time = %s"
    return execute_query(query, (provider_id, user_id, time), fetch=False)

def update_service_user(user_id, user_data):
    """Update a service user"""
    query = """
    UPDATE service_users 
    SET name = %s, address = %s, guardian_user = %s, guardian_pwd = %s
    WHERE id = %s
    """
    params = (
        user_data['name'],
        user_data['address'],
        user_data['guardian_user'],
        user_data['guardian_pwd'],
        user_id
    )
    return execute_query(query, params, fetch=False)

def update_service_provider(provider_id, provider_data):
    """Update a service provider"""
    query = """
    UPDATE service_providers 
    SET name = %s, phone = %s, role = %s, username = %s, password = %s
    WHERE id = %s
    """
    params = (
        provider_data['name'],
        provider_data['phone'],
        provider_data['role'],
        provider_data['username'],
        provider_data['password'],
        provider_id
    )
    return execute_query(query, params, fetch=False)

def get_service_types():
    """Get all service types"""
    query = "SELECT * FROM service_types ORDER BY service_types"
    result = execute_query(query)
    if result:
        return [row['service_types'] for row in result]
    return ["理发", "医疗", "血压检测", "家政服务", "其他"]

def add_service_type(service_type):
    """Add a new service type"""
    query = "INSERT INTO service_types (service_types) VALUES (%s)"
    return execute_query(query, (service_type,), fetch=False)

def delete_service_type(service_type):
    """Delete a service type"""
    query = "DELETE FROM service_types WHERE service_types = %s"
    return execute_query(query, (service_type,), fetch=False)

def get_duration_options():
    """Get duration options"""
    return ["30分钟", "40分钟", "一小时", "两小时", "半天", "全天"]

def add_duration_option(duration):
    """Add a new duration option (this would need a separate table in real implementation)"""
    # For now, we'll use a predefined list
    pass

def delete_duration_option(duration):
    """Delete a duration option (this would need a separate table in real implementation)"""
    # For now, we'll use a predefined list
    pass

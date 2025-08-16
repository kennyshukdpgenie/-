# Frontend Display Translations
# This file contains translations for displaying database columns in Chinese
# The actual database operations use English column names

# Column name translations for frontend display
COLUMN_TRANSLATIONS = {
    # service_users table
    'id': 'ID',
    'name': '姓名',
    'address': '地址',
    'guardian_user': '家属用户名',
    'guardian_pwd': '家属密码',
    
    # service_providers table
    'phone': '联系电话',
    'role': '服务类型',
    'username': '用户名',
    'password': '密码',
    
    # service_logs table
    'provider_id': '服务人员ID',
    'provider_name': '服务人员姓名',
    'user_id': '用户ID',
    'user_name': '用户姓名',
    'time': '时间',
    'service_type': '服务类型',
    'duration': '服务时长',
    'notes': '备注',
    'image_path': '图片路径',
}

# Table name translations
TABLE_TRANSLATIONS = {
    'service_users': '长者信息',
    'service_providers': '服务人员信息',
    'service_logs': '服务记录',
    'admin_accounts': '管理员账户',
    'family_accounts': '家属账户',
    'provider_accounts': '服务人员账户',
}

def translate_column_name(english_name):
    """Translate English column name to Chinese for frontend display"""
    return COLUMN_TRANSLATIONS.get(english_name, english_name)

def translate_table_name(english_name):
    """Translate English table name to Chinese for frontend display"""
    return TABLE_TRANSLATIONS.get(english_name, english_name)

def get_translated_columns(english_columns):
    """Translate a list of English column names to Chinese"""
    return [translate_column_name(col) for col in english_columns]

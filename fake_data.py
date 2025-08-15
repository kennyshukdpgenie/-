import pandas as pd
from datetime import datetime

# Mock elderly users
service_users_df = pd.DataFrame([
    {'id': 1, 'name': '张三', 'address': '奉贤区xx路88号', 'assigned_provider_id': 100},
    {'id': 2, 'name': '李四', 'address': '奉贤区yy路22号', 'assigned_provider_id': 101},
])

# Mock service providers
service_providers_df = pd.DataFrame([
    {'id': 100, 'name': '王医生', 'phone': '13812345678', 'role': '家庭医生'},
    {'id': 101, 'name': '陈阿姨', 'phone': '13912345678', 'role': '家政服务'},
])

# Mock service logs
service_logs_df = pd.DataFrame([
    {'id': 1, 'provider_id': 100, 'user_id': 1, 'time': datetime.now(), 'service_type': '血压检测',
     'duration': '30分钟', 'notes': '一切正常', 'image_path': 'static/uploads/服务老人.jpg'},
])

# Mock family accounts
family_accounts_df = pd.DataFrame([
    {'user_id': 1, 'username': 'zhangsan', 'password': '88888888'},
    {'user_id': 2, 'username': 'lisi', 'password': '88888888'},
])

# Mock admin accounts
admin_accounts_df = pd.DataFrame([
    {'username': 'admin', 'password': 'admin'},
])

# Mock provider accounts
provider_accounts_df = pd.DataFrame([
    {'provider_id': 100, 'username': 'wangyisheng', 'password': 'password123'},
    {'provider_id': 101, 'username': 'chenayi', 'password': 'password123'},
])

def get_service_users():
    return service_users_df

def get_service_providers():
    return service_providers_df

def get_service_logs():
    return service_logs_df

def get_family_accounts():
    return family_accounts_df

def get_admin_accounts():
    return admin_accounts_df

def get_provider_accounts():
    return provider_accounts_df

def add_service_log(log_entry):
    global service_logs_df
    log_entry['id'] = len(service_logs_df) + 1
    log_entry['time'] = datetime.now()
    service_logs_df = pd.concat([service_logs_df, pd.DataFrame([log_entry])], ignore_index=True) 
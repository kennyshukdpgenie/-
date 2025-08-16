import streamlit as st
import pandas as pd
from database import (
    get_service_users_translated, get_service_providers_translated, get_service_logs_translated,
    get_family_accounts_translated, get_admin_accounts_translated, get_provider_accounts_translated,
    get_service_users, get_service_providers, get_service_logs,
    get_family_accounts_from_users, get_admin_accounts, get_provider_accounts_from_providers,
    add_service_log, delete_service_user, delete_service_provider, 
    delete_service_log, update_service_user, update_service_provider,
    add_service_user, add_service_provider, get_service_types,
    add_service_type, delete_service_type
)
import os
from datetime import datetime

# 设置Streamlit主题和移动端优先的CSS
st.set_page_config(
    page_title="奉贤老干部局智守护", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile-first CSS with responsive design
st.markdown(
    '''
    <style>
    /* 移动设备模拟 - 在所有屏幕上固定移动视口 */
    .stApp {
        max-width: 375px !important;
        margin: 0 auto !important;
        background-color: #f8f6f2 !important;
        min-height: 100vh !important;
        position: relative !important;
        overflow-x: hidden !important;
    }
    
    /* 移动模拟容器 */
    .mobile-container {
        width: 375px !important;
        max-width: 375px !important;
        margin: 0 auto !important;
        background: #fff !important;
        min-height: 100vh !important;
        position: relative !important;
        box-shadow: 0 0 20px rgba(0,0,0,0.1) !important;
        border-radius: 20px !important;
        overflow: hidden !important;
    }
    
    /* 主内容区域 */
    .main > div {
        background-color: #fff !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        padding: 16px !important;
        margin: 0 !important;
        max-width: 375px !important;
        width: 100% !important;
    }
    
    /* 移动状态栏模拟 */
    .mobile-status-bar {
        height: 44px !important;
        background: #000 !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 1000 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: white !important;
        font-size: 14px !important;
        font-weight: bold !important;
    }
    
    /* 移动导航栏 */
    .mobile-nav-bar {
        height: 44px !important;
        background: #fff !important;
        border-bottom: 1px solid #ddd !important;
        position: sticky !important;
        top: 44px !important;
        z-index: 999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 16px !important;
    }
    
    /* 移动底部导航 */
    .mobile-bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 375px !important;
        max-width: 375px !important;
        background: #fff !important;
        border-top: 1px solid #ddd !important;
        padding: 8px 16px !important;
        z-index: 1000 !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
    }
    
    /* 为主内容添加底部内边距以容纳底部导航 */
    .main > div:last-child {
        padding-bottom: 80px !important;
    }
    
    /* 移动优化的按钮 */
    .stButton > button {
        background-color: #b22222 !important;
        color: #fff !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 16px !important;
        min-height: 44px !important;
        width: 100% !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #d32f2f !important;
        color: #fff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(178, 34, 34, 0.3) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* 移动优化的表单元素 */
    .stSelectbox > div > div {
        height: 44px !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
    }
    .stTextInput > div > div > input {
        height: 44px !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
        padding: 12px !important;
    }
    .stTextArea > div > div > textarea {
        min-height: 120px !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
        padding: 12px !important;
    }
    .stFileUploader > div {
        border: 2px dashed #ddd !important;
        border-radius: 8px !important;
        padding: 20px !important;
        text-align: center !important;
    }
    .stFileUploader > div:hover {
        border-color: #b22222 !important;
    }
    
    /* 隐藏所有文件上传器的英文文本 */
    .stFileUploader p, .stFileUploader span, .stFileUploader div[data-testid="stFileUploader"] p,
    .stFileUploader small, .stFileUploader label, .stFileUploader button {
        display: none !important;
    }
    
    /* 隐藏所有Streamlit英文提示和警告 */
    .stAlert, .stAlert p, .stAlert span {
        font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif !important;
    }
    
    /* 隐藏所有可能包含英文的元素 */
    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] label {
        display: none !important;
    }
    
    /* 隐藏默认的拖拽提示 */
    .uploadedFile, .uploadedFileName {
        font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif !important;
    }
    
    /* 隐藏所有可能的英文错误消息 */
    .stException, .stException p, .stException span {
        display: none !important;
    }
    
    /* 移动优化的排版 */
    h1 {
        font-size: 20px !important;
        margin-bottom: 16px !important;
        text-align: center !important;
    }
    h2 {
        font-size: 18px !important;
        margin-bottom: 12px !important;
    }
    h3 {
        font-size: 16px !important;
        margin-bottom: 8px !important;
    }
    .stMarkdown p, .stText, .stSubheader {
        font-size: 14px !important;
        line-height: 1.5 !important;
    }
    
    /* 移动优化的数据表格 */
    .stDataFrame {
        font-size: 12px !important;
        max-width: 100% !important;
        overflow-x: auto !important;
    }
    .stDataFrame thead tr th {
        background-color: #b22222 !important;
        color: #fff !important;
        font-size: 12px !important;
        font-weight: bold !important;
        padding: 8px 4px !important;
    }
    .stDataFrame tbody tr td {
        font-size: 12px !important;
        padding: 6px 4px !important;
    }
    
    /* 移动优化的单选按钮 */
    .stRadio > div {
        flex-direction: row !important;
        gap: 8px !important;
    }
    .stRadio > div > label {
        margin: 4px 0 !important;
        padding: 12px 8px !important;
        border: 1px solid #ddd !important;
        border-radius: 8px !important;
        background: #f9f9f9 !important;
        flex: 1 !important;
        text-align: center !important;
        font-size: 14px !important;
    }
    .stRadio > div > label:hover {
        background: #f0f0f0 !important;
    }
    .stRadio > div > label[data-baseweb="radio"] {
        margin: 4px 0 !important;
    }
    
    /* 移动端服务卡片 */
    .service-card {
        background: #fff !important;
        border: 1px solid #ddd !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin: 12px 0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    .service-card h4 {
        color: #b22222 !important;
        margin-bottom: 8px !important;
        font-size: 16px !important;
    }
    .service-card p {
        margin: 4px 0 !important;
        font-size: 14px !important;
    }
    
    /* 移动优化的图片 */
    .stImage {
        max-width: 100% !important;
        height: auto !important;
    }
    .stImage img {
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* 移动优化的弹出框 */
    .stPopover {
        max-width: 320px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
    }
    .stPopover > div {
        padding: 16px !important;
    }
    
    /* 完全隐藏侧边栏 */
    .stSidebar {
        display: none !important;
    }
    .main {
        margin-left: 0 !important;
        width: 100% !important;
        max-width: 375px !important;
    }
    
    /* 基础样式 */
    body {
        background-color: #f8f6f2;
        font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    
    /* 标题 */
    h1, h2, h3, h4, h5, h6 {
        color: #b22222 !important;
        font-weight: bold !important;
        font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif;
        margin-top: 0 !important;
    }
    
    /* 成功和错误消息 */
    .stAlert {
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin: 8px 0 !important;
        font-size: 14px !important;
    }
    
    /* 响应式列 */
    .stColumns > div {
        padding: 0 4px !important;
    }
    
    /* 移动应用头部 */
    .mobile-header {
        display: flex !important;
        align-items: center !important;
        padding: 8px 16px !important;
        background: #fff !important;
        border-bottom: 1px solid #eee !important;
    }
    .mobile-header img {
        width: 40px !important;
        height: 40px !important;
        border-radius: 8px !important;
    }
    .mobile-header span {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #b22222 !important;
        margin-left: 12px !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

def app_header():
    st.markdown(
        '''
        <div class="mobile-status-bar">
            奉贤老干部局智守护
        </div>
        <div class="mobile-header">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iOCIgZmlsbD0iI2IyMjIyMiIvPgo8cGF0aCBkPSJNMTIgMTJIMjhWMjBIMTJWMjBaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K" alt="Logo" />
            <span>智守护</span>
        </div>
        ''',
        unsafe_allow_html=True
    )

def entry_page():
    """入口页面 - 显示三个用户类型选择按钮"""
    app_header()
    st.title("智守护")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 三个用户类型选择按钮
    st.markdown("""
    <style>
    .user-type-button {
        background-color: #8B4513 !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 20px 40px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        margin: 15px 0 !important;
        width: 100% !important;
        min-height: 60px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .user-type-button:hover {
        background-color: #A0522D !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(139, 69, 19, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 服务人员按钮
    if st.button("服务人员", key="service_staff", use_container_width=True):
        st.session_state['selected_user_type'] = 'provider'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 长者家属按钮
    if st.button("长者家属", key="family_member", use_container_width=True):
        st.session_state['selected_user_type'] = 'family'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 管理人员按钮
    if st.button("管理人员", key="admin_staff", use_container_width=True):
        st.session_state['selected_user_type'] = 'admin'
        st.rerun()

def login():
    """登录页面 - 根据选择的用户类型显示对应登录界面"""
    app_header()
    
    user_type = st.session_state.get('selected_user_type', None)
    
    if user_type == 'provider':
        st.title("服务人员登录")
        login_type_text = "服务人员"
    elif user_type == 'family':
        st.title("长者家属登录")
        login_type_text = "家属"
    elif user_type == 'admin':
        st.title("管理人员登录")
        login_type_text = "管理员"
    else:
        # 如果没有选择用户类型，返回入口页面
        entry_page()
        return
    
    username = st.text_input("用户名", placeholder="请输入用户名")
    password = st.text_input("密码", type="password", placeholder="请输入密码")

    # 全宽登录按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("登录", use_container_width=True):
            if user_type == 'provider':
                provider_accounts = get_provider_accounts_from_providers()
                user = provider_accounts[(provider_accounts['username'] == username) & (provider_accounts['password'] == password)]
                if not user.empty:
                    st.session_state['logged_in'] = True
                    st.session_state['user_type'] = 'provider'
                    st.session_state['user_id'] = user.iloc[0]['provider_id']
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
            elif user_type == 'family':
                family_accounts = get_family_accounts_from_users()
                user = family_accounts[(family_accounts['username'] == username) & (family_accounts['password'] == password)]
                if not user.empty:
                    st.session_state['logged_in'] = True
                    st.session_state['user_type'] = 'family'
                    st.session_state['user_id'] = user.iloc[0]['user_id']
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
            elif user_type == 'admin':
                admin_accounts = get_admin_accounts()
                user = admin_accounts[(admin_accounts['username'] == username) & (admin_accounts['password'] == password)]
                if not user.empty:
                    st.session_state['logged_in'] = True
                    st.session_state['user_type'] = 'admin'
                    st.session_state['user_id'] = 'admin'
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
    
    # 返回按钮
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("返回选择用户类型", use_container_width=True):
        st.session_state.pop('selected_user_type', None)
        st.rerun()

def provider_upload():
    app_header()
    st.title("上传服务记录")
    provider_id = st.session_state['user_id']
    service_users = get_service_users()
    # For now, show all users since there's no assigned_provider_id relationship
    # In a real system, you might want to create a separate assignment table
    assigned_users = service_users.copy()
    
    if assigned_users.empty:
        st.warning("您没有分配的服务对象。")
        return

    selected_user_id = st.selectbox("选择服务对象", assigned_users['id'], format_func=lambda x: assigned_users[assigned_users['id']==x]['name'].iloc[0])
    
    st.subheader("添加新服务记录")
    
    # 移动端友好的表单布局
    service_type = st.selectbox("服务类型", ["理发", "医疗", "血压检测", "家政服务", "其他"])
    duration = st.selectbox("服务时长", ["30分钟", "40分钟", "一小时", "两小时", "半天", "全天"])
    
    st.markdown("**上传服务照片**")
    
    # 直接显示文件上传器
    uploaded_image = st.file_uploader(
        "选择照片文件", 
        type=['jpg', 'png', 'jpeg'], 
        label_visibility="collapsed",
        key="service_photo_upload"
    )
    
    # 图片大小验证
    if uploaded_image is not None:
        # 检查文件大小 (5MB = 5 * 1024 * 1024 bytes)
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if uploaded_image.size > max_size:
            st.error(f"图片文件过大！最大允许 5MB，当前文件大小: {uploaded_image.size / (1024*1024):.1f}MB")
            uploaded_image = None
        else:
            st.success(f"图片文件大小: {uploaded_image.size / (1024*1024):.1f}MB ✓")
    
    # 隐藏默认上传区域的英文文本，但保留功能
    st.markdown('''
        <style>
        /* 隐藏文件上传器的所有英文文本 */
        .stFileUploader p, .stFileUploader span, .stFileUploader small {
            display: none !important;
        }
        /* 自定义上传按钮样式 */
        .stFileUploader > div {
            border: 2px dashed #b22222 !important;
            border-radius: 8px !important;
            padding: 20px !important;
            text-align: center !important;
            background: #fff !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        .stFileUploader > div:hover {
            border-color: #d32f2f !important;
            background: #f8f6f2 !important;
        }
        /* 隐藏所有默认按钮和文本 */
        .stFileUploader button, .stFileUploader label {
            display: none !important;
        }
        /* 添加自定义中文提示 */
        .stFileUploader > div::before {
            content: "点击选择照片文件" !important;
            display: block !important;
            font-size: 16px !important;
            color: #b22222 !important;
            font-weight: bold !important;
            margin-bottom: 8px !important;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    # 图片预览
    if uploaded_image is not None:
        st.markdown("**已选择的照片预览：**")
        st.image(uploaded_image, caption="服务照片", use_container_width=True)

    # 全宽提交按钮
    if st.button("提交服务记录", use_container_width=True):
        if selected_user_id and service_type and duration:
            try:
                # Get provider and user names from their respective tables
                from database import get_service_providers
                providers_df = get_service_providers()
                provider_name = providers_df[providers_df['id'] == provider_id]['name'].iloc[0]
                user_name = assigned_users[assigned_users['id'] == selected_user_id]['name'].iloc[0]
                
                # Convert numpy types to Python types for MySQL compatibility
                provider_id_int = int(provider_id)
                selected_user_id_int = int(selected_user_id)
                
                # Handle image upload - store directly in database
                image_data = None
                if uploaded_image is not None:
                    # Read image data as bytes for LONGBLOB storage
                    image_data = uploaded_image.getbuffer().tobytes()
                    st.info(f"图片已读取，大小: {len(image_data)} bytes")
                else:
                    st.info("未上传图片")
                
                new_log = {
                    'provider_id': provider_id_int,
                    'provider_name': provider_name,
                    'user_name': user_name,
                    'user_id': selected_user_id_int,
                    'service_type': service_type,
                    'duration': duration,
                    'image_data': image_data
                }
                
                # Debug: Print the data being sent to database
                st.info(f"调试信息 - 准备保存到数据库:")
                st.info(f"provider_id: {provider_id_int} (类型: {type(provider_id_int)})")
                st.info(f"user_id: {selected_user_id_int} (类型: {type(selected_user_id_int)})")
                st.info(f"provider_name: {provider_name}")
                st.info(f"user_name: {user_name}")
                
                # Add service log to database
                if add_service_log(new_log):
                    # Success popup message
                    st.success("🎉 服务记录上传成功！")
                    
                    # Create a success card with all details
                    st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                        border: 2px solid #28a745;
                        border-radius: 10px;
                        padding: 20px;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    ">
                        <h3 style="color: #155724; margin-top: 0;">✅ 上传成功确认</h3>
                        <div style="color: #155724;">
                            <p><strong>📋 服务记录已保存到数据库</strong></p>
                            <p><strong>👨‍⚕️ 服务人员:</strong> {}</p>
                            <p><strong>👴 服务对象:</strong> {}</p>
                            <p><strong>🔧 服务类型:</strong> {}</p>
                            <p><strong>⏱️ 服务时长:</strong> {}</p>
                            <p><strong>📸 照片状态:</strong> {}</p>
                        </div>
                    </div>
                    """.format(
                        provider_name,
                        user_name,
                        service_type,
                        duration,
                        "✅ 已保存到数据库" if image_data else "❌ 未上传照片"
                    ), unsafe_allow_html=True)
                    
                    # Additional success information
                    if image_data:
                        st.info(f"📸 照片已成功保存到数据库，文件大小: {len(image_data)} bytes")
                    
                    st.balloons()  # Add celebration effect
                    
                    # Wait a moment then refresh
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ 保存服务记录失败，请重试")
            except Exception as e:
                st.error(f"上传过程中发生错误: {str(e)}")
                st.error("请检查所有字段是否正确填写")
        else:
            st.error("请选择服务对象、服务类型和服务时长。")

def provider_history():
    app_header()
    st.title("历史服务记录")
    provider_id = st.session_state['user_id']
    # Get data with English column names for operations
    service_logs_raw = get_service_logs()
    # Get data with Chinese column names for display
    service_logs_display = get_service_logs_translated()
    
    provider_logs_raw = service_logs_raw[service_logs_raw['provider_id'] == provider_id].copy()
    provider_logs_display = service_logs_display[service_logs_display['服务人员ID'] == provider_id].copy()

    if provider_logs_raw.empty:
        st.info("您还没有服务记录。")
    else:
        # 移动端友好的服务记录卡片布局
        for idx, row in provider_logs_display.iterrows():
            # Get corresponding raw data row for image data access
            raw_row = provider_logs_raw.iloc[idx]
            
            with st.container():
                st.markdown(
                    f"""
                    <div class="service-card">
                        <h4>服务记录 #{idx + 1}</h4>
                        <p><strong>用户:</strong> {row['用户姓名']}</p>
                        <p><strong>时间:</strong> {row['时间']}</p>
                        <p><strong>服务:</strong> {row['服务类型']} : {row['服务时长']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 移动端优化的图片显示 - 从数据库读取图片数据
                if 'image_data' in raw_row and raw_row['image_data'] is not None:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("查看服务照片", key=f"view_img_{idx}", use_container_width=True):
                            st.session_state[f'popup_img_{idx}'] = not st.session_state.get(f'popup_img_{idx}', False)
                    
                    # 直接显示图片，不使用popover（移动端更友好）
                    if st.session_state.get(f'popup_img_{idx}', False):
                        st.markdown("**服务照片：**")
                        try:
                            # Convert bytes to image and display
                            import io
                            from PIL import Image
                            image_bytes = raw_row['image_data']
                            if image_bytes:
                                image = Image.open(io.BytesIO(image_bytes))
                                st.image(image, use_container_width=True, caption=f"服务记录 #{idx + 1} 的照片")
                            else:
                                st.warning("图片数据为空")
                        except Exception as e:
                            st.error(f"图片显示错误: {str(e)}")
                            st.info("图片数据可能已损坏")
                else:
                    st.info("此服务记录没有照片")
                
                st.markdown("---")

def family_view():
    app_header()
    st.title("查看服务记录")
    user_id = st.session_state['user_id']
    # Get data with English column names for operations
    service_logs_raw = get_service_logs()
    # Get data with Chinese column names for display
    service_logs_display = get_service_logs_translated()
    
    user_logs_raw = service_logs_raw[service_logs_raw['user_id'] == user_id].copy()
    user_logs_display = service_logs_display[service_logs_display['用户ID'] == user_id].copy()

    if user_logs_raw.empty:
        st.info("目前没有服务记录。")
    else:
        # 移动端友好的卡片布局
        for index, row in user_logs_display.iterrows():
            # Get corresponding raw data row for image data access
            raw_row = user_logs_raw.iloc[index]
            
            with st.container():
                st.markdown(
                    f"""
                    <div class="service-card">
                        <h4>服务时间: {row['时间']}</h4>
                        <p><strong>服务人员:</strong> {row['服务人员姓名']}</p>
                        <p><strong>服务:</strong> {row['服务类型']} : {row['服务时长']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 显示图片（如果有）- 从数据库读取图片数据
                if 'image_data' in raw_row and raw_row['image_data'] is not None:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("查看服务照片", key=f"family_view_img_{index}", use_container_width=True):
                            st.session_state[f'family_popup_img_{index}'] = not st.session_state.get(f'family_popup_img_{index}', False)
                    
                    # 直接显示图片，不使用popover（移动端更友好）
                    if st.session_state.get(f'family_popup_img_{index}', False):
                        st.markdown("**服务照片：**")
                        try:
                            # Convert bytes to image and display
                            import io
                            from PIL import Image
                            image_bytes = raw_row['image_data']
                            if image_bytes:
                                image = Image.open(io.BytesIO(image_bytes))
                                st.image(image, use_container_width=True, caption=f"服务时间: {row['时间']} 的照片")
                            else:
                                st.warning("图片数据为空")
                        except Exception as e:
                            st.error(f"图片显示错误: {str(e)}")
                            st.info("图片数据可能已损坏")
                else:
                    st.info("此服务记录没有照片")
                st.markdown("---")

def admin_service_records():
    """查询服务记录"""
    app_header()
    st.title("查询服务记录")
    
    # Get data with English column names for operations
    service_logs_raw = get_service_logs().copy()
    # Get data with Chinese column names for display
    service_logs_display = get_service_logs_translated().copy()
    
    if service_logs_raw.empty:
        st.info("暂无服务记录。")
    else:
        # 移动端友好的服务记录显示
        for idx, row in service_logs_display.iterrows():
            raw_row = service_logs_raw.iloc[idx]  # Get corresponding raw data row
            
            with st.container():
                st.markdown(
                    f"""
                    <div class="service-card">
                        <h4>服务记录 #{idx + 1}</h4>
                        <p><strong>服务人员:</strong> {row['服务人员姓名']}</p>
                        <p><strong>用户:</strong> {row['用户姓名']}</p>
                        <p><strong>时间:</strong> {row['时间']}</p>
                        <p><strong>服务:</strong> {row['服务类型']} : {row['服务时长']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Delete button
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("删除记录", key=f"del_log_{idx}", use_container_width=True):
                        if delete_service_log(raw_row['provider_id'], raw_row['user_id'], raw_row['time']):
                            st.success("记录删除成功")
                            st.rerun()
                        else:
                            st.error("删除失败")
                
                # 图片显示 - 从数据库读取图片数据
                if 'image_data' in raw_row and raw_row['image_data'] is not None:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("查看服务照片", key=f"admin_view_img_{idx}", use_container_width=True):
                            st.session_state[f'admin_popup_img_{idx}'] = not st.session_state.get(f'admin_popup_img_{idx}', False)
                    
                    # 直接显示图片，不使用popover（移动端更友好）
                    if st.session_state.get(f'admin_popup_img_{idx}', False):
                        st.markdown("**服务照片：**")
                        try:
                            # Convert bytes to image and display
                            import io
                            from PIL import Image
                            image_bytes = raw_row['image_data']
                            if image_bytes:
                                image = Image.open(io.BytesIO(image_bytes))
                                st.image(image, use_container_width=True, caption=f"服务记录 #{idx + 1} 的照片")
                            else:
                                st.warning("图片数据为空")
                        except Exception as e:
                            st.error(f"图片显示错误: {str(e)}")
                            st.info("图片数据可能已损坏")
                else:
                    st.info("此服务记录没有照片")
                
                st.markdown("---")
    
    # 返回主菜单按钮
    st.markdown("---")
    if st.button("返回主菜单", use_container_width=True):
        st.session_state['admin_function'] = None
        st.rerun()

def admin_elderly_management():
    """长者信息管理"""
    app_header()
    st.title("长者信息管理")
    
    # Get data with English column names for operations
    users_df_raw = get_service_users()
    # Get data with Chinese column names for display
    users_df_display = get_service_users_translated()
    
    st.subheader("长者信息列表")
    
    # Display users with delete and edit options
    if not users_df_display.empty:
        for idx, row in users_df_display.iterrows():
            raw_row = users_df_raw.iloc[idx]  # Get corresponding raw data row
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.text(f"姓名: {row['姓名']}")
                    st.text(f"地址: {row['地址']}")
                    st.text(f"家属用户名: {row['家属用户名']}")
                with col2:
                    if st.button("编辑", key=f"edit_user_{idx}", use_container_width=True):
                        st.session_state[f'editing_user_{idx}'] = True
                with col3:
                    if st.button("删除", key=f"del_user_{idx}", use_container_width=True):
                        if delete_service_user(raw_row['id']):
                            st.success(f"已删除长者：{row['姓名']}")
                            st.rerun()
                        else:
                            st.error("删除失败")
                
                # Edit form
                if st.session_state.get(f'editing_user_{idx}', False):
                    st.markdown("---")
                    st.subheader(f"编辑长者：{row['姓名']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_name = st.text_input("姓名", value=row['姓名'], key=f"edit_name_{idx}")
                        edit_address = st.text_input("地址", value=row['地址'], key=f"edit_address_{idx}")
                    with col2:
                        edit_guardian_user = st.text_input("家属用户名", value=row['家属用户名'], key=f"edit_guardian_user_{idx}")
                        edit_guardian_pwd = st.text_input("家属密码", value=row['家属密码'], key=f"edit_guardian_pwd_{idx}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("保存", key=f"save_user_{idx}", use_container_width=True):
                            user_data = {
                                'name': edit_name,
                                'address': edit_address,
                                'guardian_user': edit_guardian_user,
                                'guardian_pwd': edit_guardian_pwd
                            }
                            if update_service_user(raw_row['id'], user_data):
                                st.success("更新成功")
                                st.session_state[f'editing_user_{idx}'] = False
                                st.rerun()
                            else:
                                st.error("更新失败")
                    with col2:
                        if st.button("取消", key=f"cancel_user_{idx}", use_container_width=True):
                            st.session_state[f'editing_user_{idx}'] = False
                            st.rerun()
                
                st.markdown("---")
    else:
        st.info("暂无长者信息")
    
    st.subheader("添加新长者")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("姓名", key="new_user_name")
        new_address = st.text_input("地址", key="new_user_address")
    with col2:
        new_guardian_user = st.text_input("家属用户名", key="new_guardian_user")
        new_guardian_pwd = st.text_input("家属密码", type="password", key="new_guardian_pwd")
    
    if st.button("添加长者", use_container_width=True):
        if new_name and new_address and new_guardian_user and new_guardian_pwd:
            user_data = {
                'name': new_name,
                'address': new_address,
                'guardian_user': new_guardian_user,
                'guardian_pwd': new_guardian_pwd
            }
            if add_service_user(user_data):
                st.success(f"已添加长者：{new_name}")
                st.rerun()
            else:
                st.error("添加失败")
        else:
            st.error("请填写所有必填字段：姓名、地址、家属用户名、家属密码")
    
    # 返回主菜单按钮
    st.markdown("---")
    if st.button("返回主菜单", use_container_width=True):
        st.session_state['admin_function'] = None
        st.rerun()

def admin_staff_management():
    """服务人员信息管理"""
    app_header()
    st.title("服务人员信息管理")
    
    # Get data with English column names for operations
    providers_df_raw = get_service_providers()
    # Get data with Chinese column names for display
    providers_df_display = get_service_providers_translated()
    
    st.subheader("服务人员列表")
    
    # Display providers with delete and edit options
    if not providers_df_display.empty:
        for idx, row in providers_df_display.iterrows():
            raw_row = providers_df_raw.iloc[idx]  # Get corresponding raw data row
            
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.text(f"姓名: {row['姓名']}")
                    st.text(f"电话: {row['联系电话']}")
                    st.text(f"服务类型: {row['服务类型']}")
                    st.text(f"用户名: {row['用户名']}")
                with col2:
                    if st.button("编辑", key=f"edit_provider_{idx}", use_container_width=True):
                        st.session_state[f'editing_provider_{idx}'] = True
                with col3:
                    if st.button("删除", key=f"del_provider_{idx}", use_container_width=True):
                        if delete_service_provider(raw_row['id']):
                            st.success(f"已删除服务人员：{row['姓名']}")
                            st.rerun()
                        else:
                            st.error("删除失败")
                
                # Edit form
                if st.session_state.get(f'editing_provider_{idx}', False):
                    st.markdown("---")
                    st.subheader(f"编辑服务人员：{row['姓名']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_name = st.text_input("姓名", value=row['姓名'], key=f"edit_provider_name_{idx}")
                        edit_phone = st.text_input("联系电话", value=row['联系电话'], key=f"edit_provider_phone_{idx}")
                        # Get service types for dropdown
                        service_types = get_service_types()
                        current_role_index = service_types.index(row['服务类型']) if row['服务类型'] in service_types else 0
                        edit_role = st.selectbox("服务类型", options=service_types, index=current_role_index, key=f"edit_provider_role_{idx}")
                    with col2:
                        edit_username = st.text_input("用户名", value=row['用户名'], key=f"edit_provider_username_{idx}")
                        edit_password = st.text_input("密码", value=row['密码'], type="password", key=f"edit_provider_password_{idx}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("保存", key=f"save_provider_{idx}", use_container_width=True):
                            provider_data = {
                                'name': edit_name,
                                'phone': edit_phone,
                                'role': edit_role,
                                'username': edit_username,
                                'password': edit_password
                            }
                            if update_service_provider(raw_row['id'], provider_data):
                                st.success("更新成功")
                                st.session_state[f'editing_provider_{idx}'] = False
                                st.rerun()
                            else:
                                st.error("更新失败")
                    with col2:
                        if st.button("取消", key=f"cancel_provider_{idx}", use_container_width=True):
                            st.session_state[f'editing_provider_{idx}'] = False
                            st.rerun()
                
                st.markdown("---")
    else:
        st.info("暂无服务人员信息")
    
    st.subheader("添加新服务人员")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("姓名", key="new_provider_name")
        new_phone = st.text_input("联系电话", key="new_provider_phone")
        # Get service types for dropdown
        service_types = get_service_types()
        new_role = st.selectbox("服务类型", options=service_types, key="new_provider_role")
    with col2:
        new_username = st.text_input("用户名", key="new_provider_username")
        new_password = st.text_input("密码", type="password", key="new_provider_password")
    
    if st.button("添加服务人员", use_container_width=True):
        if new_name and new_phone and new_username and new_password:
            provider_data = {
                'name': new_name,
                'phone': new_phone,
                'role': new_role,
                'username': new_username,
                'password': new_password
            }
            if add_service_provider(provider_data):
                st.success(f"已添加服务人员：{new_name}")
                st.rerun()
            else:
                st.error("添加失败")
        else:
            st.error("请填写所有必填字段：姓名、联系电话、用户名、密码")
    
    # 返回主菜单按钮
    st.markdown("---")
    if st.button("返回主菜单", use_container_width=True):
        st.session_state['admin_function'] = None
        st.rerun()

def admin_service_config():
    """服务类型配置"""
    app_header()
    st.title("服务类型配置")
    
    st.subheader("当前服务类型")
    current_services = get_service_types()
    
    if current_services:
        # Use enumerate to create unique keys and avoid duplicates
        for idx, service in enumerate(current_services):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(service)
            with col2:
                if st.button("删除", key=f"del_service_{idx}_{service}"):
                    if delete_service_type(service):
                        st.success(f"已删除服务类型：{service}")
                        st.rerun()
                    else:
                        st.error("删除失败")
    else:
        st.info("暂无服务类型")
    
    st.subheader("添加新服务类型")
    col1, col2 = st.columns([3, 1])
    with col1:
        new_service = st.text_input("新服务类型名称", key="new_service_type", placeholder="请输入服务类型名称")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("添加服务类型", key="add_service_type", use_container_width=True):
            if new_service and new_service.strip():
                # Check if service type already exists
                if new_service.strip() in current_services:
                    st.error("该服务类型已存在")
                else:
                    if add_service_type(new_service.strip()):
                        st.success(f"已添加服务类型：{new_service}")
                        st.rerun()
                    else:
                        st.error("添加失败")
            else:
                st.error("请输入服务类型名称")
    
    st.subheader("服务时长配置")
    current_durations = ["30分钟", "40分钟", "一小时", "两小时", "半天", "全天"]
    
    for idx, duration in enumerate(current_durations):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(duration)
        with col2:
            if st.button("删除", key=f"del_dur_{idx}_{duration}"):
                st.warning(f"删除时长选项：{duration}")
                # Note: Duration options are hardcoded for now
    
    # 返回主菜单按钮
    st.markdown("---")
    if st.button("返回主菜单", use_container_width=True):
        st.session_state['admin_function'] = None
        st.rerun()

def admin_dashboard():
    """管理员主界面 - 显示4个选项"""
    app_header()
    st.title("管理员控制台")
    
    # 检查是否已选择管理功能
    if 'admin_function' not in st.session_state:
        st.session_state['admin_function'] = None
    
    admin_function = st.session_state.get('admin_function', None)
    
    if admin_function is None:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 四个管理选项按钮
        if st.button("查询服务记录", key="admin_service_records", use_container_width=True):
            st.session_state['admin_function'] = 'service_records'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("长者信息管理", key="admin_elderly_mgmt", use_container_width=True):
            st.session_state['admin_function'] = 'elderly_management'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("服务人员信息管理", key="admin_staff_mgmt", use_container_width=True):
            st.session_state['admin_function'] = 'staff_management'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("服务类型配置", key="admin_service_config", use_container_width=True):
            st.session_state['admin_function'] = 'service_config'
            st.rerun()
    
    else:
        # 显示对应的管理功能
        if admin_function == 'service_records':
            admin_service_records()
        elif admin_function == 'elderly_management':
            admin_elderly_management()
        elif admin_function == 'staff_management':
            admin_staff_management()
        elif admin_function == 'service_config':
            admin_service_config()
        
        # 返回主菜单按钮
        st.markdown("---")
        if st.button("返回主菜单", key="admin_return_main", use_container_width=True):
            st.session_state['admin_function'] = None
            st.rerun()

def mobile_navigation():
    """移动端底部导航栏"""
    st.markdown(
        """
        <div class="mobile-nav">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 14px; color: #666;">奉贤老干部局智守护</span>
                <button onclick="window.location.reload();" style="background: #b22222; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-size: 12px;">刷新</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        # 检查是否已选择用户类型
        if 'selected_user_type' not in st.session_state:
            entry_page()
        else:
            login()
    else:
        user_type = st.session_state['user_type']
        
        # 移动端友好的导航
        if user_type == 'provider':
            page = st.radio("选择页面", ["上传服务记录", "查看历史服务记录"], horizontal=False)
            if page == "上传服务记录":
                provider_upload()
            elif page == "查看历史服务记录":
                provider_history()
        elif user_type == 'family':
            family_view()
        elif user_type == 'admin':
            admin_dashboard()

        # 移动端登出按钮
        st.markdown("---")
        if st.button("登出", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state.pop('user_type', None)
            st.session_state.pop('user_id', None)
            st.session_state.pop('selected_user_type', None)
            st.session_state.pop('admin_function', None)
            st.rerun()

if __name__ == "__main__":
    main() 
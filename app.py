import streamlit as st
import pandas as pd
from fake_data import (
    get_service_users, get_service_providers, get_service_logs,
    get_family_accounts, get_admin_accounts, get_provider_accounts,
    add_service_log
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
    
    /* 隐藏文件上传器的英文文本 */
    .stFileUploader p, .stFileUploader span, .stFileUploader div[data-testid="stFileUploader"] p {
        display: none !important;
    }
    .stFileUploader button {
        display: none !important;
    }
    
    /* 隐藏所有英文错误消息和警告 */
    .stAlert, .stAlert p, .stAlert span {
        font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif !important;
    }
    /* 隐藏Streamlit的英文警告和错误消息 */
    .stAlert[data-testid="stAlert"] p:contains("deprecated"),
    .stAlert[data-testid="stAlert"] p:contains("removed"),
    .stAlert[data-testid="stAlert"] p:contains("future release"),
    .stAlert[data-testid="stAlert"] p:contains("utilize"),
    .stAlert[data-testid="stAlert"] p:contains("parameter") {
        display: none !important;
    }
    /* 隐藏所有包含英文的警告框 */
    .stAlert:has(p:contains("deprecated")),
    .stAlert:has(p:contains("removed")),
    .stAlert:has(p:contains("future release")),
    .stAlert:has(p:contains("utilize")),
    .stAlert:has(p:contains("parameter")) {
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

def login():
    app_header()
    st.title("登录")
    
    # 移动端友好的登录表单
    login_type = st.selectbox("选择登录类型", ["服务人员", "家属", "管理员"])
    username = st.text_input("用户名", placeholder="请输入用户名")
    password = st.text_input("密码", type="password", placeholder="请输入密码")

    # 全宽登录按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("登录", use_container_width=True):
            if login_type == "服务人员":
                provider_accounts = get_provider_accounts()
                user = provider_accounts[(provider_accounts['username'] == username) & (provider_accounts['password'] == password)]
                if not user.empty:
                    st.session_state['logged_in'] = True
                    st.session_state['user_type'] = 'provider'
                    st.session_state['user_id'] = user.iloc[0]['provider_id']
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
            elif login_type == "家属":
                family_accounts = get_family_accounts()
                user = family_accounts[(family_accounts['username'] == username) & (family_accounts['password'] == password)]
                if not user.empty:
                    st.session_state['logged_in'] = True
                    st.session_state['user_type'] = 'family'
                    st.session_state['user_id'] = user.iloc[0]['user_id']
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
            elif login_type == "管理员":
                admin_accounts = get_admin_accounts()
                user = admin_accounts[(admin_accounts['username'] == username) & (admin_accounts['password'] == password)]
                if not user.empty:
                    st.session_state['logged_in'] = True
                    st.session_state['user_type'] = 'admin'
                    st.session_state['user_id'] = 'admin'
                    st.rerun()
                else:
                    st.error("用户名或密码错误")

def provider_upload():
    app_header()
    st.title("上传服务记录")
    provider_id = st.session_state['user_id']
    service_users = get_service_users()
    assigned_users = service_users[service_users['assigned_provider_id'] == provider_id]
    
    if assigned_users.empty:
        st.warning("您没有分配的服务对象。")
        return

    selected_user_id = st.selectbox("选择服务对象", assigned_users['id'], format_func=lambda x: assigned_users[assigned_users['id']==x]['name'].iloc[0])
    
    st.subheader("添加新服务记录")
    
    # 移动端友好的表单布局
    service_type = st.selectbox("服务类型", ["理发", "医疗", "血压检测", "家政服务", "其他"])
    duration = st.selectbox("服务时长", ["30分钟", "40分钟", "一小时", "两小时", "半天", "全天"])
    notes = st.text_area("服务内容", placeholder="请详细描述服务内容...", height=120)
    
    st.markdown("**上传服务照片**")
    
    # 自定义上传按钮 - 使用Streamlit的原生文件上传器但隐藏默认UI
    uploaded_image = st.file_uploader(
        "点击选择照片", 
        type=['jpg', 'png', 'jpeg'], 
        label_visibility="collapsed",
        key="service_photo_upload"
    )
    
    # 隐藏默认上传区域的英文文本，但保留功能
    st.markdown('''
        <style>
        /* 隐藏文件上传器的英文文本，但保留上传功能 */
        .stFileUploader p, .stFileUploader span {
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
        /* 隐藏默认的"Browse files"按钮 */
        .stFileUploader button {
            display: none !important;
        }
        /* 添加自定义中文提示 */
        .stFileUploader > div::before {
            content: "点击上传服务照片" !important;
            display: block !important;
            font-size: 16px !important;
            color: #b22222 !important;
            font-weight: bold !important;
            margin-bottom: 8px !important;
        }
        .stFileUploader > div::after {
            content: "支持 JPG, PNG, JPEG 格式 • 限制200MB" !important;
            display: block !important;
            font-size: 14px !important;
            color: #666 !important;
            margin-top: 8px !important;
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
            image_path = None
            if uploaded_image is not None:
                if not os.path.exists('static/uploads'):
                    os.makedirs('static/uploads')
                image_path = os.path.join('static/uploads', uploaded_image.name)
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                # 用于显示，使用 '@/uploads/filename'
                display_image_path = f"@/uploads/{uploaded_image.name}"
            else:
                # 如果没有上传图片，使用默认测试图片
                display_image_path = "@/uploads/test.jpeg"
            new_log = {
                'provider_id': provider_id,
                'user_id': selected_user_id,
                'service_type': service_type,
                'duration': duration,
                'notes': notes,
                'image_path': display_image_path
            }
            add_service_log(new_log)
            st.success("服务记录上传成功！")
        else:
            st.error("请选择服务对象、服务类型和服务时长。")

def provider_history():
    app_header()
    st.title("历史服务记录")
    provider_id = st.session_state['user_id']
    service_logs = get_service_logs()
    provider_logs = service_logs[service_logs['provider_id'] == provider_id].copy()

    if provider_logs.empty:
        st.info("您还没有服务记录。")
    else:
        # 移动端友好的服务记录卡片布局
        for idx, row in provider_logs.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div class="service-card">
                        <h4>服务记录 #{row['id']}</h4>
                        <p><strong>时间:</strong> {row['time']}</p>
                        <p><strong>服务类型:</strong> {row['service_type']}</p>
                        <p><strong>服务时长:</strong> {row['duration']}</p>
                        <p><strong>服务内容:</strong> {row['notes']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 移动端优化的图片显示
                if row['image_path']:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("查看服务照片", key=f"view_img_{idx}", use_container_width=True):
                            st.session_state[f'popup_img_{idx}'] = not st.session_state.get(f'popup_img_{idx}', False)
                    
                    # 直接显示图片，不使用popover（移动端更友好）
                    if st.session_state.get(f'popup_img_{idx}', False):
                        st.markdown("**服务照片：**")
                        img_path = row['image_path']
                        if img_path.startswith('@/uploads/'):
                            img_file = img_path.replace('@/uploads/', 'static/uploads/')
                        else:
                            img_file = img_path
                        
                        if os.path.exists(img_file):
                            st.image(img_file, use_container_width=True, caption=f"服务记录 #{row['id']} 的照片")
                        else:
                            st.warning("图片文件不存在")
                            st.info(f"图片路径: {img_file}")
                
                st.markdown("---")

def family_view():
    app_header()
    st.title("查看服务记录")
    user_id = st.session_state['user_id']
    service_logs = get_service_logs()
    user_logs = service_logs[service_logs['user_id'] == user_id]

    if user_logs.empty:
        st.info("目前没有服务记录。")
    else:
        # 移动端友好的卡片布局
        for index, row in user_logs.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div class="service-card">
                        <h4>服务时间: {row['time']}</h4>
                        <p><strong>服务类型:</strong> {row['service_type']}</p>
                        <p><strong>服务时长:</strong> {row['duration']}</p>
                        <p><strong>服务内容:</strong> {row['notes']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 显示图片（如果有）
                img_path = row.get('image_path', None)
                if img_path:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("查看服务照片", key=f"family_view_img_{index}", use_container_width=True):
                            st.session_state[f'family_popup_img_{index}'] = not st.session_state.get(f'family_popup_img_{index}', False)
                    
                    # 直接显示图片，不使用popover（移动端更友好）
                    if st.session_state.get(f'family_popup_img_{index}', False):
                        st.markdown("**服务照片：**")
                        if img_path.startswith('@/uploads/'):
                            img_file = img_path.replace('@/uploads/', 'static/uploads/')
                        else:
                            img_file = img_path
                        
                        if os.path.exists(img_file):
                            st.image(img_file, use_container_width=True, caption=f"服务时间: {row['time']} 的照片")
                        else:
                            st.warning("图片文件不存在")
                            st.info(f"图片路径: {img_file}")
                st.markdown("---")

def admin_dashboard():
    app_header()
    st.title("管理端-全局信息")

    st.subheader("服务人员信息")
    providers_df = get_service_providers()
    st.dataframe(providers_df, use_container_width=True)

    st.subheader("被服务人员信息")
    users_df = get_service_users()
    st.dataframe(users_df, use_container_width=True)

    st.subheader("所有服务记录")
    service_logs = get_service_logs().copy()
    if service_logs.empty:
        st.info("暂无服务记录。")
    else:
        # 移动端友好的服务记录显示
        for idx, row in service_logs.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div class="service-card">
                        <h4>服务记录 #{row['id']}</h4>
                        <p><strong>服务人员ID:</strong> {row['provider_id']}</p>
                        <p><strong>用户ID:</strong> {row['user_id']}</p>
                        <p><strong>时间:</strong> {row['time']}</p>
                        <p><strong>服务类型:</strong> {row['service_type']}</p>
                        <p><strong>服务时长:</strong> {row['duration']}</p>
                        <p><strong>服务内容:</strong> {row['notes']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 图片显示
                if row['image_path']:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("查看服务照片", key=f"admin_view_img_{idx}", use_container_width=True):
                            st.session_state[f'admin_popup_img_{idx}'] = not st.session_state.get(f'admin_popup_img_{idx}', False)
                    
                    # 直接显示图片，不使用popover（移动端更友好）
                    if st.session_state.get(f'admin_popup_img_{idx}', False):
                        st.markdown("**服务照片：**")
                        img_path = row['image_path']
                        if img_path.startswith('@/uploads/'):
                            img_file = img_path.replace('@/uploads/', 'static/uploads/')
                        else:
                            img_file = img_path
                        
                        if os.path.exists(img_file):
                            st.image(img_file, use_container_width=True, caption=f"服务记录 #{row['id']} 的照片")
                        else:
                            st.warning("图片文件不存在")
                            st.info(f"图片路径: {img_file}")
                
                st.markdown("---")

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
            st.rerun()

if __name__ == "__main__":
    main() 
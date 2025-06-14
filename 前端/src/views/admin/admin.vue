<template>
  <div class="admin-dashboard">
    <!-- 固定侧边栏 -->
    <div class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="logo-container">
        <div class="logo">
          <svg class="logo-icon" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
          </svg>
          <span>慧眼视界</span>
        </div>
        <button class="collapse-btn" @click="toggleSidebar" style="margin-left:-15px">
          <svg v-if="!isCollapsed" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
      <div class="menu">
        <div 
    v-for="(item, index) in menuItems" 
    :key="index" 
    class="menu-item" 
    :class="{ active: activeMenuItem === item.key, collapsed: isCollapsed }"
    @click="handleMenuItemClick(item.key)"
>
    <svg class="menu-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" v-html="getIconPath(item.icon)"></svg>
    <span v-if="!isCollapsed" class="menu-text">{{ item.label }}</span>
</div>
      </div>
      <div class="user-info" :class="{ collapsed: isCollapsed }">
        <div class="avatar">
          <div v-if="!adminAvatar" class="default-avatar">
            <svg class="avatar-icon" viewBox="0 0 24 24" width="40" height="40" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <img v-else :src="adminAvatar" alt="管理员头像" />
        </div>
        <div v-if="!isCollapsed" class="user-details">
          <div class="user-name">管理员</div>
          <div class="user-role">系统管理员</div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content" :class="{ 'sidebar-collapsed': isCollapsed }">
      <!-- 固定顶部导航栏 -->
      <div class="top-nav" :class="{ 'sidebar-collapsed': isCollapsed }">
        <div class="breadcrumb">
          <svg class="breadcrumb-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 15 12 15 22"></polyline>
          </svg>
          <span>首页</span>
          <svg class="breadcrumb-separator" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
          <span>{{ getCurrentMenuTitle() }}</span>
        </div>
        <div class="top-nav-right">
          <div class="search-box">
            <svg class="search-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" placeholder="搜索..." />
          </div>
          <div class="notification" @click="showNotifications = !showNotifications">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span class="badge" v-if="notifications.length > 0">{{ notifications.length }}</span>
            <div class="notification-dropdown" v-if="showNotifications">
              <div class="notification-header">
                <span>通知</span>
                <span class="notification-count">{{ notifications.length }}条未读</span>
              </div>
              <div class="notification-list">
                <div v-for="(notification, index) in notifications" :key="index" class="notification-item">
                  <div class="notification-icon" :class="notification.type">
                    <svg v-if="notification.type === 'account'" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                    <svg v-if="notification.type === 'review'" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                      <line x1="16" y1="13" x2="8" y2="13"></line>
                      <line x1="16" y1="17" x2="8" y2="17"></line>
                      <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    <svg v-if="notification.type === 'system'" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                  </div>
                  <div class="notification-content">
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-desc">{{ notification.description }}</div>
                    <div class="notification-time">{{ notification.time }}</div>
                  </div>
                </div>
              </div>
              <div class="notification-footer">
                <button @click="clearNotifications">清空通知</button>
                <button @click="showNotifications = false">关闭</button>
              </div>
            </div>
          </div>
          <div class="settings">
            <svg @click="showSettings = !showSettings" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </div>
        </div>
      </div>

      <!-- 路由视图 -->
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isCollapsed: false,
      showNotifications: false,
      showSettings: false,
      adminAvatar: null, // 管理员头像URL，如果为null则显示默认SVG
      activeMenuItem: 'doctors', // 默认选中第一个菜单项
      notifications: [
        {
          type: 'account',
          title: '新医生注册',
          description: '李医生已提交注册申请，等待审核',
          time: '10分钟前'
        },
        {
          type: 'review',
          title: '信息修改申请',
          description: '张医生提交了个人信息修改申请',
          time: '30分钟前'
        },
        {
          type: 'system',
          title: '系统更新',
          description: '系统将于今晚22:00进行维护更新',
          time: '1小时前'
        }
      ],
      menuItems: [
        { key: 'doctors', label: '医生账号管理', icon: 'users-icon', route: 'doctors' },
        { key: 'review', label: '信息审核', icon: 'file-text-icon', route: 'review' },
        { key: 'model', label: '诊断模型效果', icon: 'bar-chart2-icon', route: 'model' },
       { key: 'logout', label: '退出登录', icon: 'logout-icon', route: 'login' },
      ]
    }
  },
  mounted() {
    // 根据当前路由设置活动菜单项
    this.setActiveMenuItemFromRoute();
  },
  watch: {
    // 监听路由变化，更新活动菜单项
    '$route'() {
      this.setActiveMenuItemFromRoute();
    }
  },
  methods: {
    handleMenuItemClick(key) {
        if (key === 'logout') {
            // 清空本地存储
            localStorage.clear();
            // 跳转到登录页面
            this.$router.push('/login');
        } else {
            this.setActiveMenuItem(key);
        }
    },
    getIconPath(iconName) {
      // 返回SVG路径数据，替代Lucide图标组件
      const iconPaths = {
        'home-icon': '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline>',
        'users-icon': '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
        'file-text-icon': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>',
        'bar-chart2-icon': '<line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>',
        'settings-icon': '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>',
        'logout-icon': '<path d="M9 18l6-6-6-6"></path><circle cx="12" cy="12" r="10"></circle><path d="M12 6v12"></path><path d="M16 10l-4 4-4-4"></path>',

      };
      
      return iconPaths[iconName] || '';
    },
    getCurrentMenuTitle() {
      const activeItem = this.menuItems.find(item => item.key === this.activeMenuItem);
      return activeItem ? activeItem.label : '';
    },
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    clearNotifications() {
      this.notifications = [];
      this.showNotifications = false;
    },
    setActiveMenuItem(key) {
      this.activeMenuItem = key;
      
      // 如果使用了vue-router，可以在这里进行路由跳转
      const menuItem = this.menuItems.find(item => item.key === key);
      if (menuItem && menuItem.route) {
        this.$router.push({ name: menuItem.route });
      }
    },
    setActiveMenuItemFromRoute() {
      // 根据当前路由设置活动菜单项
      const currentRoute = this.$route.name;
      const menuItem = this.menuItems.find(item => item.route === currentRoute);
      if (menuItem) {
        this.activeMenuItem = menuItem.key;
      }
    }
  }
}
</script>

<style scoped>
/* 全局样式 */
.admin-dashboard {
  display: flex;
  min-height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #333;
  background-color: #f5f7fa;
}

/* 侧边栏样式 */
.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #4299e1 0%, #3182ce 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar.collapsed {
  width: 80px;
}

.logo-container {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
}

.logo-icon {
  width: 24px;
  height: 24px;
}

.collapse-btn {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  z-index: 101; /* 确保按钮在折叠时仍然可见 */
}

.menu {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 5px;
  border-radius: 0 25px 25px 0;
  position: relative;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.menu-item.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 添加一个左侧边框指示器 */
.menu-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background-color: white;
  border-radius: 0 2px 2px 0;
}

.menu-icon {
  width: 20px;
  height: 20px;
  margin-right: 15px;
}

.menu-item.collapsed {
  justify-content: center;
  padding: 12px;
}

.menu-item.collapsed .menu-icon {
  margin-right: 0;
}

.user-info {
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info.collapsed {
  justify-content: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.default-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #eaeaea;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  width: 24px;
  height: 24px;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: bold;
  font-size: 14px;
}

.user-role {
  font-size: 12px;
  opacity: 0.8;
}

/* 主内容区样式 */
.main-content {
  flex: 1;
  margin-left: 240px;
  transition: margin-left 0.3s;
}

.main-content.sidebar-collapsed {
  margin-left: 80px;
}

/* 顶部导航栏固定 */
.top-nav {
  background-color: white;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  position: fixed;
  top: 0;
  right: 0;
  left: 240px;
  z-index: 99;
  transition: left 0.3s;
}

.main-content.sidebar-collapsed .top-nav {
  left: 80px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
}

.breadcrumb-icon {
  width: 16px;
  height: 16px;
}

.breadcrumb-separator {
  width: 14px;
  height: 14px;
  opacity: 0.5;
}

.top-nav-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-box {
  position: relative;
  width: 250px;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #999;
}

.search-box input {
  width: 100%;
  padding: 8px 10px 8px 35px;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.search-box input:focus {
  border-color: #4299e1;
}

.notification {
  position: relative;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #e74c3c;
  color: white;
  font-size: 10px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  z-index: 100;
  margin-top: 10px;
  overflow: hidden;
}

.notification-header {
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.notification-count {
  font-size: 12px;
  color: #e74c3c;
}

.notification-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-item {
  padding: 12px 15px;
  display: flex;
  gap: 10px;
  border-bottom: 1px solid #f5f5f5;
  transition: background-color 0.3s;
}

.notification-item:hover {
  background-color: #f9f9f9;
}

.notification-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-icon.account {
  background-color: #4299e1;
  color: white;
}

.notification-icon.review {
  background-color: #f39c12;
  color: white;
}

.notification-icon.system {
  background-color: #e74c3c;
  color: white;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 3px;
}

.notification-desc {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.notification-time {
  font-size: 11px;
  color: #999;
}

.notification-footer {
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #eee;
}

.notification-footer button {
  background: none;
  border: none;
  color: #4299e1;
  cursor: pointer;
  font-size: 12px;
}

.settings {
  cursor: pointer;
}

.content {
  padding: 20px;
  margin-top: 60px; /* 为顶部导航栏留出空间 */
}

/* 响应式样式 */
@media (max-width: 768px) {
  .sidebar {
    width: 80px;
  }
  
  .sidebar.collapsed {
    width: 0;
    overflow: hidden;
  }
  
  .logo span, .menu-text, .user-details {
    display: none;
  }
  
  .menu-icon {
    margin-right: 0;
  }
  
  .menu-item {
    justify-content: center;
    padding: 12px;
  }
  
  .main-content {
    margin-left: 80px;
  }
  
  .main-content.sidebar-collapsed {
    margin-left: 0;
  }
  
  .search-box {
    display: none;
  }
}

@media (max-width: 576px) {
  .sidebar {
    width: 0;
    overflow: hidden;
  }
  
  .sidebar.collapsed {
    width: 80px;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .main-content.sidebar-collapsed {
    margin-left: 80px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
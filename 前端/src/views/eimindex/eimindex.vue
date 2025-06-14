<template>
  <div class="eye-health-system">
    <!-- 左侧导航 -->
    <div class="side-panel" :class="{ 'collapsed': isCollapsed }">
      <div class="logo-container">
         <div class="eye-icon">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                <path d="M12 14c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"/>
              </svg>
            </div>
        <div class="system-name" v-if="!isCollapsed">慧眼视界</div>
        <div class="collapse-btn" @click="toggleCollapse">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6" v-if="!isCollapsed"></polyline>
            <polyline points="9 18 15 12 9 6" v-else></polyline>
          </svg>
        </div>
      </div>
      
      <div class="nav-menu">
        <div 
          v-for="(item, index) in menuItems" 
          :key="index" 
          class="menu-item" 
          :class="{ 'active': currentPage === item.id }"
          @click="changePage(item.id)"
        >
          <div class="menu-icon">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <component :is="item.icon"></component>
            </svg>
          </div>
          <span class="menu-text" v-if="!isCollapsed">{{ item.name }}</span>
          <div class="tooltip" v-if="isCollapsed">{{ item.name }}</div>
        </div>
      </div>
      
      <div class="user-profile" @click="showDoctorTooltip = true" @mouseenter="showDoctorTooltip = true">
    <div class="avatar">
        <img :src="doctorInfo.avatar ? `http://8.155.59.127:34561/user${doctorInfo.avatar}` : defaultAvatar" alt="医生头像" />
    </div>
    <div class="user-info" v-if="!isCollapsed">
        <div class="user-name">{{ doctorInfo.doctor_name || '加载中...' }}</div>
        <div class="user-role">{{ getPositionText(doctorInfo.position) }}</div>
    </div>
    
    <!-- 医生信息悬浮卡片 -->
    <div class="doctor-tooltip" v-if="showDoctorTooltip && doctorInfo.doctor_id">
        <div class="doctor-tooltip-header">
            <div class="doctor-avatar">
                <img :src="doctorInfo.avatar ? `http://8.155.59.127:34561/user${doctorInfo.avatar}` : defaultAvatar" alt="医生头像" />
            </div>
            <div class="doctor-basic-info">
                <h3>{{ doctorInfo.doctor_name }}</h3>
                <div class="doctor-position">{{ getPositionText(doctorInfo.position) }}</div>
            </div>
        </div>
        <div class="doctor-tooltip-body">
            <div class="info-item">
                <div class="info-icon">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                    </svg>
                </div>
                <div class="info-content">
                    <div class="info-label">联系电话</div>
                    <div class="info-value">{{ doctorInfo.phone || '暂无' }}</div>
                </div>
            </div>
            <div class="info-item">
                <div class="info-icon">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                        <polyline points="22,6 12,13 2,6"></polyline>
                    </svg>
                </div>
                <div class="info-content">
                    <div class="info-label">电子邮箱</div>
                    <div class="info-value">{{ doctorInfo.email || '暂无' }}</div>
                </div>
            </div>
            <div class="info-item">
                <div class="info-icon">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <div class="info-content">
                    <div class="info-label">性别</div>
                    <div class="info-value">{{ doctorInfo.gender || '暂无' }}</div>
                </div>
            </div>
            <div class="info-item" v-if="doctorInfo.introduce">
                <div class="info-icon">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                </div>
                <div class="info-content">
                    <div class="info-label">个人简介</div>
                    <div class="info-value intro-text">{{ doctorInfo.introduce }}</div>
                </div>
            </div>
        </div>
        <div class="doctor-tooltip-footer">
            <button class="view-profile-btn" @click.stop="navigateTo('info')">查看完整资料</button>
        </div>
    </div>
</div>
    </div>
    
    <!-- 主内容区域 -->
    <div class="main-content" :class="{ 'expanded': isCollapsed }">
      <!-- 顶部栏 -->
      <div class="top-bar">
        <div class="page-title">
          <h1>{{ pageTitle }}</h1>
          <div class="breadcrumb">
            <span>首页</span>
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>{{ pageTitle }}</span>
          </div>
        </div>
        <div class="top-actions">
          <div class="search-container">
            <input type="text" placeholder="搜索..." />
            <div class="search-icon">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </div>
          </div>
          <div class="notification-bell" @click="toggleNotifications">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span class="notification-badge" v-if="notifications.length">{{ notifications.length }}</span>
            
            <!-- 通知下拉菜单 -->
            <div class="notification-dropdown" v-if="showNotifications">
              <div class="dropdown-header">
                <h3>通知</h3>
                <button class="mark-all-read" @click.stop="markAllAsRead">全部标为已读</button>
              </div>
              <div class="notification-list">
                <div v-if="notifications.length === 0" class="no-notifications">
                  暂无通知
                </div>
                <div v-else v-for="(notification, index) in notifications" :key="index" class="notification-item" :class="{ 'unread': !notification.read }">
                  <div class="notification-icon" :class="notification.type">
                    <svg v-if="notification.type === 'appointment'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="16" y1="2" x2="16" y2="6"></line>
                      <line x1="8" y1="2" x2="8" y2="6"></line>
                      <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    <svg v-else-if="notification.type === 'report'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                      <line x1="16" y1="13" x2="8" y2="13"></line>
                      <line x1="16" y1="17" x2="8" y2="17"></line>
                      <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                  </div>
                  <div class="notification-content">
                    <div class="notification-message">{{ notification.message }}</div>
                    <div class="notification-time">{{ notification.time }}</div>
                  </div>
                  <button class="notification-close" @click.stop="removeNotification(index)">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="dropdown-footer">
                <button class="view-all-btn" @click.stop="viewAllNotifications">查看全部</button>
              </div>
            </div>
          </div>
          <div class="settings-btn">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </div>
        </div>
      </div>
      
      <!-- 路由视图 -->
      <div class="content-wrapper">
        <router-view></router-view>
      </div>
    </div>
    
    <!-- 通知提示 -->
    <div class="notification-toast" v-if="notification.show" :class="notification.type">
      <div class="notification-icon">
        <svg v-if="notification.type === 'success'" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <svg v-else-if="notification.type === 'error'" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <svg v-else viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      <div class="notification-message">{{ notification.message }}</div>
      <button class="close-notification" @click="closeNotification">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppLayout',
  data() {
    return {
      isCollapsed: false,
      currentPage: 'dashboard',
      pageTitle: '数据总览',
      showUserMenu: false,
      showNotifications: false,
      showDoctorTooltip: false,
      currentDate: new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }),
      notification: {
        show: false,
        message: '',
        type: 'success'
      },
      defaultAvatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      doctorInfo: {
        doctor_id: null,
        doctor_name: '加载中...',
        gender: '',
        email: '',
        phone: '',
        position: '',
        avatar: null,
        introduce: ''
      },
      notifications: [
        { id: 1, message: '李华的预约已确认', time: '10分钟前', read: false, type: 'appointment' },
        { id: 2, message: '新的检查报告已上传', time: '1小时前', read: false, type: 'report' },
        { id: 3, message: '系统更新通知', time: '昨天', read: true, type: 'system' }
      ],
      menuItems: [
        { id: 'dashboard', name: '数据总览', icon: 'DashboardIcon', path: '/dashboard' },
        { id: 'diagnosis', name: '眼科诊断', icon: 'EyeIcon', path: '/diagnosis' },
        { id: 'patients', name: '患者管理', icon: 'UsersIcon', path: '/patients' },
        { id: 'dghistory', name: '诊断历史', icon: 'ClockIcon', path: '/dghistory' },
        { id: 'analytics', name: '个人中心', icon: 'BarChartIcon', path: '/info' },
        { id: 'settings', name: '系统设置', icon: 'SettingsIcon', path: '/settings' },
        { id: 'help', name: '帮助中心', icon: 'HelpCircleIcon', path: '/help' }
      ]
    };
  },
  computed: {
    DashboardIcon() {
      return {
        render(h) {
          return h('g', [
            h('rect', { attrs: { x: '3', y: '3', width: '7', height: '7' } }),
            h('rect', { attrs: { x: '14', y: '3', width: '7', height: '7' } }),
            h('rect', { attrs: { x: '14', y: '14', width: '7', height: '7' } }),
            h('rect', { attrs: { x: '3', y: '14', width: '7', height: '7' } })
          ]);
        }
      };
    },
    EyeIcon() {
      return {
        render(h) {
          return h('g', [
            h('path', { attrs: { d: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z' } }),
            h('circle', { attrs: { cx: '12', cy: '12', r: '3' } })
          ]);
        }
      };
    },
    UsersIcon() {
      return {
        render(h) {
          return h('g', [
            h('path', { attrs: { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' } }),
            h('circle', { attrs: { cx: '9', cy: '7', r: '4' } }),
            h('path', { attrs: { d: 'M23 21v-2a4 4 0 0 0-3-3.87' } }),
            h('path', { attrs: { d: 'M16 3.13a4 4 0 0 1 0 7.75' } })
          ]);
        }
      };
    },
    ClockIcon() {
      return {
        render(h) {
          return h('g', [
            h('circle', { attrs: { cx: '12', cy: '12', r: '10' } }),
            h('polyline', { attrs: { points: '12 6 12 12 16 14' } })
          ]);
        }
      };
    },
    BarChartIcon() {
      return {
        render(h) {
          return h('g', [
            h('line', { attrs: { x1: '12', y1: '20', x2: '12', y2: '10' } }),
            h('line', { attrs: { x1: '18', y1: '20', x2: '18', y2: '4' } }),
            h('line', { attrs: { x1: '6', y1: '20', x2: '6', y2: '16' } })
          ]);
        }
      };
    },
    SettingsIcon() {
      return {
        render(h) {
          return h('g', [
            h('circle', { attrs: { cx: '12', cy: '12', r: '3' } }),
            h('path', { attrs: { d: 'M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 5.6 4.6a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09A1.65 1.65 0 0 0 12.6 4.6a1.65 1.65 0 0 0 .33 1.82V9a1.65 1.65 0 0 0 1.51 1z' } })
          ]);
        }
      };
    },
    HelpCircleIcon() {
      return {
        render(h) {
          return h('g', [
            h('circle', { attrs: { cx: '12', cy: '12', r: '10' } }),
            h('path', { attrs: { d: 'M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3' } }),
            h('line', { attrs: { x1: '12', y1: '17', x2: '12', y2: '17' } })
          ]);
        }
      };
    },
    LogOutIcon() {
      return {
        render(h) {
          return h('g', [
            h('path', { attrs: { d: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4' } }),
            h('polyline', { attrs: { points: '16 17 21 12 16 7' } }),
            h('line', { attrs: { x1: '21', y1: '12', x2: '9', y2: '12' } })
          ]);
        }
      };
    }
  },
  methods: {
    // 获取医生信息
    async fetchDoctorInfo() {
      try {
        // 从本地存储获取token和userId
        const infoStr = localStorage.getItem('info');
        if (!infoStr) {
          this.showToast('未找到登录信息，请重新登录', 'error');
          return;
        }
        
        const info = JSON.parse(infoStr);
        if (!info.token || !info.userId) {
          this.showToast('登录信息不完整，请重新登录', 'error');
          return;
        }
        
        // 发送请求获取医生信息
        const response = await fetch('http://8.155.59.127:34561/user/getDoctorInfo/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': info.token
          },
          body: JSON.stringify({ 
            "doctor_id": info.userId 
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          this.doctorInfo = data.data;
          console.log('医生信息获取成功:', this.doctorInfo);
        } else {
          console.error('获取医生信息失败:', data.msg);
          this.showToast(`获取医生信息失败: ${data.msg}`, 'error');
        }
      } catch (error) {
        console.error('获取医生信息出错:', error);
        this.showToast('获取医生信息出错，请稍后重试', 'error');
      }
    },
    
    // 获取职位文本
    getPositionText(position) {
      const positionMap = {
        'chief_physician': '主任医师',
        'associate_chief_physician': '副主任医师',
        'attending_physician': '主治医师',
        'resident_physician': '住院医师',
        'intern': '实习医师'
      };
      
      return position ? positionMap[position] || position : '医生';
    },
    
    updateTopBarPosition() {
      const sidePanel = document.querySelector('.side-panel');
      const topBar = document.querySelector('.top-bar');
      if (sidePanel && topBar) {
        const sidePanelWidth = sidePanel.clientWidth;
        topBar.style.left = `${sidePanelWidth}px`;
      }
    },
    
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
      this.updateTopBarPosition(); // 切换侧边栏时立即更新顶部栏位置
    },
    
    changePage(page) {
      this.currentPage = page;
      const menuItem = this.menuItems.find(item => item.id === page);
      if (menuItem) {
        this.pageTitle = menuItem.name;
        if (this.$router) {
          this.$router.push(menuItem.path);
        }
      }
      
      // 关闭所有下拉菜单
      this.showUserMenu = false;
      this.showNotifications = false;
    },
    
    toggleUserMenu(event) {
      event.stopPropagation();
      this.showUserMenu = !this.showUserMenu;
      this.showNotifications = false;
    },
    
    toggleNotifications(event) {
      event.stopPropagation();
      this.showNotifications = !this.showNotifications;
      this.showUserMenu = false;
    },
    
    navigateTo(page) {
      if (this.$router) {
        this.$router.push(`/${page}`);
      }
      this.showUserMenu = false;
    },
    
    logout() {
      // 实际应用中应该调用登出API
      localStorage.removeItem('info');
      if (this.$router) {
        this.$router.push('/login');
      }
      this.showToast('已成功退出登录', 'success');
    },
    
    showToast(message, type = 'success') {
      this.notification = {
        show: true,
        message,
        type
      };
      
      // 3秒后自动关闭
      setTimeout(() => {
        this.closeNotification();
      }, 3000);
    },
    
    closeNotification() {
      this.notification.show = false;
    },
    
    markAllAsRead() {
      this.notifications.forEach(notification => {
        notification.read = true;
      });
    },
    
    removeNotification(index) {
      this.notifications.splice(index, 1);
    },
    
    viewAllNotifications() {
      if (this.$router) {
        this.$router.push('/notifications');
      }
      this.showNotifications = false;
    },
    
    // 点击页面其他地方关闭下拉菜单
    handleClickOutside(event) {
      if (this.showUserMenu || this.showNotifications) {
        this.showUserMenu = false;
        this.showNotifications = false;
      }
    }
  },
  mounted() {
    // 添加全局点击事件监听器
    document.addEventListener('click', this.handleClickOutside);
    
    // 初始化路由
    if (this.$router) {
      const currentRoute = this.$route.path;
      const matchedMenuItem = this.menuItems.find(item => item.path === currentRoute);
      if (matchedMenuItem) {
        this.currentPage = matchedMenuItem.id;
        this.pageTitle = matchedMenuItem.name;
      }
    }
    
    const sidePanel = document.querySelector('.side-panel');
    sidePanel.addEventListener('transitionend', () => {
      this.updateTopBarPosition();
    });
    
    // 页面加载时获取医生信息
    this.fetchDoctorInfo();
  },
  beforeDestroy() {
    // 移除全局点击事件监听器
    document.removeEventListener('click', this.handleClickOutside);
  },
  watch: {
    '$route'(to) {
      const matchedMenuItem = this.menuItems.find(item => item.path === to.path);
      if (matchedMenuItem) {
        this.currentPage = matchedMenuItem.id;
        this.pageTitle = matchedMenuItem.name;
      }
    }
  }
};
</script>

<style scoped>
/* 基础样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.eye-health-system {
  display: flex;
  min-height: 100vh;
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  background-color: #f8fafc;
}

/* 侧边栏样式 */
.side-panel {
  width: 260px;
  background: linear-gradient(180deg, #72b3e3 0%, #4299e1 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  z-index: 10;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}
.side-panel {
  position: fixed !important; /* 固定侧边栏 */
  height: 100vh; /* 占满整个视口高度 */
}

.side-panel.collapsed {
  width: 80px;
}

.logo-container {
  display: flex;
  align-items: center;
  padding: 24px;
  position: relative;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.eye-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  transition: all 0.3s ease;
}

.side-panel.collapsed .eye-icon {
  margin-right: 0;
}

.system-name {
  font-size: 16px;
  font-weight: 600;
  white-space: nowrap;
  transition: opacity 0.3s ease;
}

.collapse-btn {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-50%) scale(1.1);
}

.nav-menu {
  flex: 1;
  padding: 20px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  margin: 4px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.menu-item.active {
  background: rgba(255, 255, 255, 0.2);
  font-weight: 500;
}

.menu-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  transition: all 0.3s;
}

.side-panel.collapsed .menu-icon {
  margin-right: 0;
}

.menu-text {
  font-size: 14px;
  white-space: nowrap;
  transition: opacity 0.3s;
}

.tooltip {
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  pointer-events: none;
  z-index: 100;
  margin-left: 10px;
}

.tooltip::before {
  content: '';
  position: absolute;
  top: 50%;
  left: -6px;
  transform: translateY(-50%);
  border-width: 6px 6px 6px 0;
  border-style: solid;
  border-color: transparent rgba(0, 0, 0, 0.8) transparent transparent;
}

.menu-item:hover .tooltip {
  opacity: 1;
  visibility: visible;
}

.user-profile {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.1);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s;
}

.side-panel.collapsed .avatar {
  margin-right: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  flex: 1;
  overflow: hidden;
  transition: opacity 0.3s;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 医生信息悬浮卡片 */
.doctor-tooltip {
  position: absolute;
  bottom: 100%;
  left: 0;
  width: 300px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  z-index: 100;
  overflow: hidden;
  animation: fadeIn 0.3s ease;
  margin-bottom: 15px;
  color: #333;
}

.doctor-tooltip::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 30px;
  border-width: 10px 10px 0 10px;
  border-style: solid;
  border-color: white transparent transparent transparent;
}

.doctor-tooltip-header {
  display: flex;
  align-items: center;
  padding: 20px;
  background: linear-gradient(to right, #f0f9ff, #e6f7ff);
  border-bottom: 1px solid #e6f7ff;
}

.doctor-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
  border: 3px solid white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.doctor-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.doctor-basic-info {
  flex: 1;
}

.doctor-basic-info h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
  color: #2d3748;
}

.doctor-position {
  font-size: 14px;
  color: #4a5568;
  font-weight: 500;
}

.doctor-tooltip-body {
  padding: 15px 20px;
}

.info-item {
  display: flex;
  margin-bottom: 12px;
}

.info-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: #4299e1;
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 12px;
  color: #718096;
  margin-bottom: 2px;
}

.info-value {
  font-size: 14px;
  color: #2d3748;
}

.intro-text {
  max-height: 60px;
  overflow-y: auto;
  line-height: 1.5;
}

.doctor-tooltip-footer {
  padding: 15px 20px;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

.view-profile-btn {
  width: 100%;
  padding: 8px 0;
  background: #4299e1;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.view-profile-btn:hover {
  background: #3182ce;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 20px;
  width: 180px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  z-index: 100;
  overflow: hidden;
  animation: fadeIn 0.3s ease;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  color: #4a5568;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background: #f7fafc;
}

.dropdown-item svg {
  margin-right: 12px;
}

.dropdown-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 8px 0;
}

.dropdown-item.logout {
  color: #e53e3e;
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.main-content {
  margin-left: 260px; /* 与侧边栏宽度匹配 */
}

.main-content.expanded {
  margin-left: 80px; /* 与折叠后的侧边栏宽度匹配 */
}


/* 顶部栏样式 */
.top-bar {
  position: fixed; /* 固定顶部栏 */
  top: 0;
  left: 260px; /* 与侧边栏宽度匹配 */
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  z-index: 5;
}

.page-title h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #2d3748;
}

.breadcrumb {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #718096;
}

.breadcrumb svg {
  margin: 0 8px;
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-container {
  position: relative;
  width: 240px;
}

.search-container input {
  width: 100%;
  padding: 10px 16px 10px 40px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  font-size: 14px;
  transition: all 0.3s;
}

.search-container input:focus {
  outline: none;
  border-color: #72b3e3;
  box-shadow: 0 0 0 3px rgba(114, 179, 227, 0.2);
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
}

.notification-bell, .settings-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: all 0.3s;
  color: #4a5568;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.notification-bell:hover, .settings-btn:hover {
  background: #f7fafc;
  color: #2d3748;
  transform: translateY(-2px);
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 18px;
  height: 18px;
  background: #e53e3e;
  color: white;
  border-radius: 50%;
  font-size: 10px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  z-index: 100;
  overflow: hidden;
  margin-top: 12px;
  animation: fadeIn 0.3s ease;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.dropdown-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.mark-all-read {
  font-size: 12px;
  color: #4299e1;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.mark-all-read:hover {
  color: #2b6cb0;
  text-decoration: underline;
}

.notification-list {
  max-height: 320px;
  overflow-y: auto;
}

.no-notifications {
  padding: 24px;
  text-align: center;
  color: #a0aec0;
  font-size: 14px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 12px 16px;
  border-bottom: 1px solid #f7fafc;
  transition: all 0.2s;
  position: relative;
}

.notification-item:hover {
  background: #f7fafc;
}

.notification-item.unread {
  background: #ebf8ff;
}

.notification-item.unread:hover {
  background: #bee3f8;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.notification-icon.appointment {
  background: #ebf8ff;
  color: #4299e1;
}

.notification-icon.report {
  background: #e6fffa;
  color: #38b2ac;
}

.notification-icon.system {
  background: #fefcbf;
  color: #d69e2e;
}

.notification-content {
  flex: 1;
}

.notification-message {
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 4px;
  line-height: 1.4;
}

.notification-time {
  font-size: 12px;
  color: #a0aec0;
}

.notification-close {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #cbd5e0;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0;
}

.notification-item:hover .notification-close {
  opacity: 1;
}

.notification-close:hover {
  background: #edf2f7;
  color: #a0aec0;
}

.dropdown-footer {
  padding: 12px 16px;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

.view-all-btn {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  background: #edf2f7;
  color: #4a5568;
  border: none;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background: #e2e8f0;
}

/* 内容包装器调整 */
.content-wrapper {
  flex: 1;
  padding-top: 80px 24px 24px; /* 顶部留出固定栏的位置 */
  margin-top: 80px;
  overflow-y: auto;
}

/* 通知提示样式 */
.notification-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 16px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1000;
  min-width: 300px;
  animation: slideIn 0.3s ease-out forwards;
}

.notification-toast.success {
  border-left: 4px solid #48bb78;
}

.notification-toast.error {
  border-left: 4px solid #f56565;
}

.notification-toast.info {
  border-left: 4px solid #4299e1;
}

.notification-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-toast.success .notification-icon {
  color: #48bb78;
}

.notification-toast.error .notification-icon {
  color: #f56565;
}

.notification-toast.info .notification-icon {
  color: #4299e1;
}

.notification-message {
  flex: 1;
  font-size: 14px;
  color: #4a5568;
}

.close-notification {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #a0aec0;
}

.close-notification:hover {
  background: #f8fafc;
  color: #718096;
}

/* 动画 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .search-container {
    width: 180px;
  }
}

@media (max-width: 992px) {
  .side-panel {
    width: 80px;
  }
  
  .side-panel.collapsed {
    width: 0;
    overflow: hidden;
  }
  
  .system-name, .menu-text, .user-info {
    display: none;
  }
  
  .eye-icon, .menu-icon, .avatar {
    margin-right: 0;
  }
  
  .main-content {
    margin-left: 80px;
  }
  
  .main-content.expanded {
    margin-left: 0;
  }
  
  .menu-item {
    padding: 12px;
    margin: 4px;
    justify-content: center;
  }
  
  .menu-item:hover {
    transform: none;
  }
  
  .logo-container {
    justify-content: center;
    padding: 16px;
  }
  
  .collapse-btn {
    display: none;
  }
  
  .doctor-tooltip {
    left: 80px;
    bottom: auto;
    top: 0;
  }
  
  .doctor-tooltip::after {
    left: -10px;
    bottom: auto;
    top: 20px;
    border-width: 10px 10px 10px 0;
    border-color: transparent white transparent transparent;
  }
}

@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 16px;
    left: 0;
  }
  
  .top-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .search-container {
    width: 100%;
  }
  
  .notification-dropdown {
    width: 100%;
    right: 0;
    left: 0;
    border-radius: 0;
  }
  
  .content-wrapper {
    padding: 16px;
  }
  
  .notification-toast {
    width: calc(100% - 32px);
    right: 16px;
    left: 16px;
  }
  
  .doctor-tooltip {
    width: 280px;
    left: 50%;
    transform: translateX(-50%);
  }
  
  .doctor-tooltip::after {
    left: 50%;
    transform: translateX(-50%);
    bottom: -10px;
    top: auto;
    border-width: 10px 10px 0 10px;
    border-color: white transparent transparent transparent;
  }
}
</style>
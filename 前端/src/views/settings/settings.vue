<template>
  <div class="settings-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1>管理您的账户和偏好设置</h1>
      </div>
    </div>
    
    <!-- 标签页导航 -->
    <div class="tabs-container">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        class="tab-button" 
        :class="{ active: activeSection === tab.id }"
        @click="activeSection = tab.id"
      >
        <i class="tab-icon" v-html="tab.icon"></i>
        <span>{{ tab.name }}</span>
      </button>
    </div>
    
    <!-- 设置内容区域 -->
    <div class="settings-content">
      <!-- 密码修改部分 -->
      <div class="settings-card" v-if="activeSection === 'password'">
        <div class="card-header">
          <h2>密码修改</h2>
          <p>定期更新您的密码可以提高账户安全性</p>
        </div>
        
        <div class="card-body">
          <div class="form-group">
            <label>当前密码</label>
            <div class="input-wrapper">
              <input 
                :type="showCurrentPassword ? 'text' : 'password'" 
                v-model="passwordInfo.currentPassword" 
                placeholder="请输入当前密码"
                :class="{ 'error': errors.currentPassword }"
              >
              <button 
                type="button" 
                class="toggle-password" 
                @click="showCurrentPassword = !showCurrentPassword"
              >
                <i v-html="showCurrentPassword ? eyeOffIcon : eyeIcon"></i>
              </button>
            </div>
            <span class="error-message" v-if="errors.currentPassword">{{ errors.currentPassword }}</span>
          </div>
          
          <div class="form-group">
            <label>新密码</label>
            <div class="input-wrapper">
              <input 
                :type="showNewPassword ? 'text' : 'password'" 
                v-model="passwordInfo.newPassword" 
                placeholder="请输入新密码"
                :class="{ 'error': errors.newPassword }"
              >
              <button 
                type="button" 
                class="toggle-password" 
                @click="showNewPassword = !showNewPassword"
              >
                <i v-html="showNewPassword ? eyeOffIcon : eyeIcon"></i>
              </button>
            </div>
            <span class="error-message" v-if="errors.newPassword">{{ errors.newPassword }}</span>
            
            <div class="password-strength" v-if="passwordInfo.newPassword">
              <div class="strength-label">密码强度：</div>
              <div class="strength-meter">
                <div 
                  class="strength-value" 
                  :style="{ width: passwordStrength.percent + '%' }"
                  :class="passwordStrength.level"
                ></div>
              </div>
              <div class="strength-text" :class="passwordStrength.level">{{ passwordStrength.text }}</div>
            </div>
            
            <div class="password-tips" v-if="passwordInfo.newPassword">
              <div class="tip-item" :class="{ valid: hasLowerCase }">
                <i v-html="hasLowerCase ? checkIcon : xIcon"></i>
                <span>包含小写字母</span>
              </div>
              <div class="tip-item" :class="{ valid: hasUpperCase }">
                <i v-html="hasUpperCase ? checkIcon : xIcon"></i>
                <span>包含大写字母</span>
              </div>
              <div class="tip-item" :class="{ valid: hasNumber }">
                <i v-html="hasNumber ? checkIcon : xIcon"></i>
                <span>包含数字</span>
              </div>
              <div class="tip-item" :class="{ valid: hasMinLength }">
                <i v-html="hasMinLength ? checkIcon : xIcon"></i>
                <span>至少8个字符</span>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label>确认新密码</label>
            <div class="input-wrapper">
              <input 
                :type="showConfirmPassword ? 'text' : 'password'" 
                v-model="passwordInfo.confirmPassword" 
                placeholder="请再次输入新密码"
                :class="{ 'error': errors.confirmPassword }"
              >
              <button 
                type="button" 
                class="toggle-password" 
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <i v-html="showConfirmPassword ? eyeOffIcon : eyeIcon"></i>
              </button>
            </div>
            <span class="error-message" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
          </div>
          
          <div class="form-group">
            <label>验证码</label>
            <div class="captcha-container">
              <input 
                type="text" 
                v-model="captcha.code" 
                placeholder="请输入验证码"
                :class="{ 'error': errors.captcha }"
              >
              <div class="captcha-wrapper" @click="getCaptcha">
                <img :src="captcha.image" alt="验证码" v-if="captcha.image">
                <div class="captcha-refresh" v-if="captcha.cooldown > 0">{{ captcha.cooldown }}s</div>
                <div class="captcha-loading" v-if="isLoadingCaptcha && !captcha.image">
                  <i v-html="loadingIcon"></i>
                </div>
              </div>
            </div>
            <span class="error-message" v-if="errors.captcha">{{ errors.captcha }}</span>
            <div class="captcha-tip">点击图片可刷新验证码</div>
          </div>
        </div>
        
        <div class="card-footer">
          <button 
            class="primary-button" 
            @click="changePassword"
            :disabled="isSubmitting"
          >
            <i v-html="isSubmitting ? loadingIcon : saveIcon"></i>
            <span>{{ isSubmitting ? '处理中...' : '保存修改' }}</span>
          </button>
        </div>
      </div>
      
      <!-- 外观设置部分 -->
      <div class="settings-card" v-if="activeSection === 'appearance'">
        <div class="card-header">
          <h2>外观设置</h2>
          <p>自定义系统界面以获得更好的使用体验</p>
        </div>
        
        <div class="card-body">
          <div class="form-group">
            <label>主题模式</label>
            <div class="theme-options">
              <div 
                class="theme-option" 
                :class="{ active: displaySettings.theme === 'light' }"
                @click="displaySettings.theme = 'light'"
              >
                <div class="theme-preview light-theme"></div>
                <span>浅色模式</span>
              </div>
              
              <div 
                class="theme-option" 
                :class="{ active: displaySettings.theme === 'dark' }"
                @click="displaySettings.theme = 'dark'"
              >
                <div class="theme-preview dark-theme"></div>
                <span>深色模式</span>
              </div>
              
              <div 
                class="theme-option" 
                :class="{ active: displaySettings.theme === 'auto' }"
                @click="displaySettings.theme = 'auto'"
              >
                <div class="theme-preview auto-theme"></div>
                <span>跟随系统</span>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label>主题色</label>
            <div class="color-options">
              <div 
                v-for="color in themeColors" 
                :key="color.value"
                class="color-option"
                :class="{ active: displaySettings.themeColor === color.value }"
                :style="{ backgroundColor: color.hex }"
                @click="displaySettings.themeColor = color.value"
              >
                <i v-if="displaySettings.themeColor === color.value" v-html="checkIcon"></i>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label>字体大小</label>
            <div class="font-size-slider">
              <span class="size-label">A</span>
              <input 
                type="range" 
                min="0" 
                max="2" 
                step="1" 
                v-model="displaySettings.fontSizeIndex"
              >
              <span class="size-label large">A</span>
            </div>
            <div class="font-size-value">{{ fontSizeOptions[displaySettings.fontSizeIndex] }}</div>
          </div>
          
          <div class="form-group">
            <label>界面动画</label>
            <div class="toggle-container">
              <label class="toggle-switch">
                <input type="checkbox" v-model="displaySettings.enableAnimations">
                <span class="toggle-slider"></span>
              </label>
              <span class="toggle-label">{{ displaySettings.enableAnimations ? '已启用' : '已禁用' }}</span>
            </div>
            <p class="setting-description">启用或禁用界面过渡动画效果</p>
          </div>
          
          <div class="form-group">
            <label>界面布局</label>
            <div class="layout-options">
              <div 
                class="layout-option" 
                :class="{ active: displaySettings.layout === 'compact' }"
                @click="displaySettings.layout = 'compact'"
              >
                <div class="layout-preview compact-layout"></div>
                <span>紧凑布局</span>
              </div>
              
              <div 
                class="layout-option" 
                :class="{ active: displaySettings.layout === 'comfortable' }"
                @click="displaySettings.layout = 'comfortable'"
              >
                <div class="layout-preview comfortable-layout"></div>
                <span>舒适布局</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card-footer">
          <button class="primary-button" @click="saveDisplaySettings">
            <i v-html="saveIcon"></i>
            <span>保存设置</span>
          </button>
          <button class="secondary-button" @click="resetDisplaySettings">
            <i v-html="resetIcon"></i>
            <span>恢复默认</span>
          </button>
        </div>
      </div>
      
      <!-- 通知设置部分 -->
      <div class="settings-card" v-if="activeSection === 'notification'">
        <div class="card-header">
          <h2>通知设置</h2>
          <p>管理系统通知和提醒方式</p>
        </div>
        
        <div class="card-body">
          <div class="notification-options">
            <div class="notification-option">
              <div class="option-info">
                <h3>系统通知</h3>
                <p>接收系统更新、维护和重要公告</p>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" v-model="notificationSettings.system">
                <span class="toggle-slider"></span>
              </label>
            </div>
            
            <div class="notification-option">
              <div class="option-info">
                <h3>预约提醒</h3>
                <p>接收患者预约和日程安排提醒</p>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" v-model="notificationSettings.appointment">
                <span class="toggle-slider"></span>
              </label>
            </div>
            
            <div class="notification-option">
              <div class="option-info">
                <h3>诊断结果</h3>
                <p>接收新的诊断结果和报告通知</p>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" v-model="notificationSettings.diagnosis">
                <span class="toggle-slider"></span>
              </label>
            </div>
            
            <div class="notification-option">
              <div class="option-info">
                <h3>邮件通知</h3>
                <p>通过电子邮件接收重要通知</p>
              </div>
              <div class="input-with-toggle">
                <input 
                  type="email" 
                  v-model="notificationSettings.emailAddress" 
                  placeholder="请输入邮箱地址"
                  :disabled="!notificationSettings.email"
                >
                <label class="toggle-switch">
                  <input type="checkbox" v-model="notificationSettings.email">
                  <span class="toggle-slider"></span>
                </label>
              </div>
            </div>
            
            <div class="notification-option">
              <div class="option-info">
                <h3>短信通知</h3>
                <p>通过短信接收重要通知</p>
              </div>
              <div class="input-with-toggle">
                <input 
                  type="tel" 
                  v-model="notificationSettings.phoneNumber" 
                  placeholder="请输入手机号码"
                  :disabled="!notificationSettings.sms"
                >
                <label class="toggle-switch">
                  <input type="checkbox" v-model="notificationSettings.sms">
                  <span class="toggle-slider"></span>
                </label>
              </div>
            </div>
            
            <div class="notification-option">
              <div class="option-info">
                <h3>通知时段</h3>
                <p>设置接收通知的时间范围</p>
              </div>
              <div class="time-range">
                <select v-model="notificationSettings.startTime">
                  <option v-for="hour in 24" :key="`start-${hour-1}`" :value="hour-1">{{ hour-1 }}:00</option>
                </select>
                <span>至</span>
                <select v-model="notificationSettings.endTime">
                  <option v-for="hour in 24" :key="`end-${hour-1}`" :value="hour-1">{{ hour-1 }}:00</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card-footer">
          <button class="primary-button" @click="saveNotificationSettings">
            <i v-html="saveIcon"></i>
            <span>保存设置</span>
          </button>
        </div>
      </div>
      
      <!-- 隐私安全部分 -->
      <div class="settings-card" v-if="activeSection === 'privacy'">
        <div class="card-header">
          <h2>隐私安全</h2>
          <p>管理账户安全和隐私设置</p>
        </div>
        
        <div class="card-body">
          <div class="security-options">
            <div class="security-option">
              <div class="option-info">
                <h3>两步验证</h3>
                <p>启用两步验证以增强账户安全性</p>
              </div>
              <div class="option-action">
                <label class="toggle-switch">
                  <input type="checkbox" v-model="securitySettings.twoFactor">
                  <span class="toggle-slider"></span>
                </label>
                <button v-if="securitySettings.twoFactor" class="text-button" @click="showTwoFactorSetup = true">
                  配置
                </button>
              </div>
            </div>
            
            <div class="security-option">
              <div class="option-info">
                <h3>登录通知</h3>
                <p>当账户在新设备上登录时接收通知</p>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" v-model="securitySettings.loginAlert">
                <span class="toggle-slider"></span>
              </label>
            </div>
            
            <div class="security-option">
              <div class="option-info">
                <h3>会话管理</h3>
                <p>查看和管理当前登录的设备</p>
              </div>
              <button class="action-button" @click="showSessionsModal = true">
                <i v-html="devicesIcon"></i>
                <span>管理会话</span>
              </button>
            </div>
            
            <div class="security-option">
              <div class="option-info">
                <h3>账户活动日志</h3>
                <p>查看账户的最近活动记录</p>
              </div>
              <button class="action-button" @click="showActivityLogModal = true">
                <i v-html="historyIcon"></i>
                <span>查看日志</span>
              </button>
            </div>
            
            <div class="security-option">
              <div class="option-info">
                <h3>数据导出</h3>
                <p>导出您的个人数据和设置</p>
              </div>
              <button class="action-button" @click="exportUserData">
                <i v-html="downloadIcon"></i>
                <span>导出数据</span>
              </button>
            </div>
          </div>
        </div>
        
        <div class="card-footer">
          <button class="primary-button" @click="saveSecuritySettings">
            <i v-html="saveIcon"></i>
            <span>保存设置</span>
          </button>
          <button class="danger-button" @click="showLogoutConfirm = true">
            <i v-html="logoutIcon"></i>
            <span>退出登录</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 退出登录确认对话框 -->
    <div class="modal-overlay" v-if="showLogoutConfirm" @click="showLogoutConfirm = false">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>确认退出</h3>
          <button class="close-button" @click="showLogoutConfirm = false">
            <i v-html="closeIcon"></i>
          </button>
        </div>
        <div class="modal-content">
          <div class="modal-icon warning">
            <i v-html="warningIcon"></i>
          </div>
          <p>您确定要退出登录吗？</p>
        </div>
        <div class="modal-actions">
          <button class="secondary-button" @click="showLogoutConfirm = false">取消</button>
          <button class="danger-button" @click="logout">确认退出</button>
        </div>
      </div>
    </div>
    
    <!-- 会话管理模态框 -->
    <div class="modal-overlay" v-if="showSessionsModal" @click="showSessionsModal = false">
      <div class="modal-container large" @click.stop>
        <div class="modal-header">
          <h3>会话管理</h3>
          <button class="close-button" @click="showSessionsModal = false">
            <i v-html="closeIcon"></i>
          </button>
        </div>
        <div class="modal-content">
          <div class="sessions-list">
            <div class="session-item current">
              <div class="session-icon">
                <i v-html="deviceIcons.desktop"></i>
              </div>
              <div class="session-info">
                <div class="session-name">Windows 10 - Chrome</div>
                <div class="session-details">
                  <span class="session-location">北京, 中国</span>
                  <span class="session-time">当前会话</span>
                </div>
              </div>
              <div class="session-actions">
                <span class="current-badge">当前设备</span>
              </div>
            </div>
            
            <div class="session-item">
              <div class="session-icon">
                <i v-html="deviceIcons.mobile"></i>
              </div>
              <div class="session-info">
                <div class="session-name">iPhone 13 - Safari</div>
                <div class="session-details">
                  <span class="session-location">北京, 中国</span>
                  <span class="session-time">最近登录: 今天 10:25</span>
                </div>
              </div>
              <div class="session-actions">
                <button class="text-button danger" @click="terminateSession('session1')">
                  <i v-html="logoutIcon"></i>
                  <span>终止</span>
                </button>
              </div>
            </div>
            
            <div class="session-item">
              <div class="session-icon">
                <i v-html="deviceIcons.tablet"></i>
              </div>
              <div class="session-info">
                <div class="session-name">iPad - Safari</div>
                <div class="session-details">
                  <span class="session-location">上海, 中国</span>
                  <span class="session-time">最近登录: 昨天 15:40</span>
                </div>
              </div>
              <div class="session-actions">
                <button class="text-button danger" @click="terminateSession('session2')">
                  <i v-html="logoutIcon"></i>
                  <span>终止</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="danger-button" @click="terminateAllSessions">终止所有其他会话</button>
          <button class="secondary-button" @click="showSessionsModal = false">关闭</button>
        </div>
      </div>
    </div>
    
    <!-- 活动日志模态框 -->
    <div class="modal-overlay" v-if="showActivityLogModal" @click="showActivityLogModal = false">
      <div class="modal-container large" @click.stop>
        <div class="modal-header">
          <h3>账户活动日志</h3>
          <button class="close-button" @click="showActivityLogModal = false">
            <i v-html="closeIcon"></i>
          </button>
        </div>
        <div class="modal-content">
          <div class="activity-filters">
            <div class="filter-group">
              <label>活动类型</label>
              <select v-model="activityLogFilter.type">
                <option value="all">全部活动</option>
                <option value="login">登录活动</option>
                <option value="settings">设置变更</option>
                <option value="security">安全事件</option>
              </select>
            </div>
            <div class="filter-group">
              <label>时间范围</label>
              <select v-model="activityLogFilter.timeRange">
                <option value="7">最近7天</option>
                <option value="30">最近30天</option>
                <option value="90">最近90天</option>
              </select>
            </div>
          </div>
          
          <div class="activity-list">
            <div class="activity-item">
              <div class="activity-icon login">
                <i v-html="loginIcon"></i>
              </div>
              <div class="activity-info">
                <div class="activity-title">账户登录</div>
                <div class="activity-details">
                  <span>Windows 10 - Chrome</span>
                  <span>北京, 中国</span>
                  <span>今天 08:15</span>
                </div>
              </div>
            </div>
            
            <div class="activity-item">
              <div class="activity-icon settings">
                <i v-html="settingsIcon"></i>
              </div>
              <div class="activity-info">
                <div class="activity-title">密码已修改</div>
                <div class="activity-details">
                  <span>Windows 10 - Chrome</span>
                  <span>北京, 中国</span>
                  <span>昨天 16:30</span>
                </div>
              </div>
            </div>
            
            <div class="activity-item">
              <div class="activity-icon login">
                <i v-html="loginIcon"></i>
              </div>
              <div class="activity-info">
                <div class="activity-title">账户登录</div>
                <div class="activity-details">
                  <span>iPhone 13 - Safari</span>
                  <span>北京, 中国</span>
                  <span>昨天 10:25</span>
                </div>
              </div>
            </div>
            
            <div class="activity-item">
              <div class="activity-icon security">
                <i v-html="securityIcon"></i>
              </div>
              <div class="activity-info">
                <div class="activity-title">两步验证已启用</div>
                <div class="activity-details">
                  <span>Windows 10 - Chrome</span>
                  <span>北京, 中国</span>
                  <span>3天前 14:20</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="secondary-button" @click="exportActivityLog">
            <i v-html="downloadIcon"></i>
            <span>导出日志</span>
          </button>
          <button class="secondary-button" @click="showActivityLogModal = false">关闭</button>
        </div>
      </div>
    </div>
    
    <!-- 两步验证设置模态框 -->
    <div class="modal-overlay" v-if="showTwoFactorSetup" @click="showTwoFactorSetup = false">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>设置两步验证</h3>
          <button class="close-button" @click="showTwoFactorSetup = false">
            <i v-html="closeIcon"></i>
          </button>
        </div>
        <div class="modal-content">
          <div class="setup-steps">
            <div class="step active">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>下载验证器应用</h4>
                <p>在您的手机上安装 Google Authenticator 或 Microsoft Authenticator 应用</p>
              </div>
            </div>
            
            <div class="step">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4>扫描二维码</h4>
                <p>打开验证器应用，扫描下方二维码</p>
                <div class="qr-code">
                  <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKQAAACkCAYAAAAZtYVBAAAAAklEQVR4AewaftIAAAYTSURBVO3BQY4cSRLAQDLQ//8yV0c/JZCoain6zYjdYYnFQyzxEEs8xBIPscRDLPEQSzzEEg+xxEMs8RBLPMQSDzHxoUp+UsWbKjcqb6rcqHxS5SdVPrHEQyzxEEs8xMSXVbmp8o0qNyo3Kt+o3FR5o8o3Vb5piYdY4iGWeIiJH1bljcobld+k8kaVNyq/aYmHWOIhlniIiT+Myh9miYdY4iGWeIiJH1SdVPrHEEs8xMSXVbmp8o0qNyo3Kt+o3FR5o8o3Vb5piYdY4iGWeIiJH1bljcobld+k8kaVNyq/aYmHWOIhlniIiT+Myh9miYdY4iGWeIiJH1blf1T5ROU3LfEQSzzEEg8x8cOq/KQqNypvVG5UblTeqNyo3FR5o/JNSzzEEg+xxENM/LCKf5nKGxU3KjcqNyo3Kp9Y4iGWeIglHmLiQ5X8pIpvUvlE5UblRuWmyk2VT1T5xBIPscRDLPEQE1+m8ptUblRuVG5UblRuVN6o3KjcVLmp8k1LPMQSDzHEQ0z8sCpvVN6ofKLyRuUTlTcqb1TeqHzTEg+xxEMs8RATf5jKJyo3KjdVblQ+UblR+aYlHmKJh1jiISb+ZVRuVG5UblRuVG5UblRuVG5UblRuVL5piYdY4iGWeIiJL6vym1TeqLxR+UTlRuWNyk2VNyqfWOIhlniIJR5i4kNVflKVT1TeqNyovFG5UblR+aTKT1riIZZ4iCUeYuLLqtxU+UTlRuWNyk2VG5UblZsqNyo3VW6qfNMSD7HEQyzxEBM/rMoblTcqb1TeqLxReaPyRuWNyhuVNyrftMRDLPEQSzzExB9G5UblpspNlRuVG5WbKjcqNyo3Kp9Y4iGWeIglHmLih1X5psoblZsqNyo3Kp+o3Ki8UXmj8k1LPMQSDzHEQ0z8sCo/qcoblZsqb1TeqNxUuanyRuWbqnzTEg+xxEMs8RATX1blpspNlZsqNyo3VW5UblRuqtxUualyU+Wblnj4f2aJh1jiISZ+WJU3Km9U3qjcVLlReaPyRuWNyhuVNyo/aYmHWOIhlniIiT9M5Y3KGxU3KjdVblRuqtxUuVH5xBIPscRDLPEQEz+syv+Tyk2VG5UblRuVmyo3Kp9Y4iGWeIglHmLiy6r8pCo3VW6q3FS5qXJT5abKTZWbKjdVbqp80xIPscRDLPEQEz+syk+q8kblRuWNyk2VG5U3Km9UPrHEQyzxEEs8xMSHKvlJFTcqb1TeqLxReaPyRuWNyhuVb1riIZZ4iCUeYuLLqtxU+UaVmyo3VW6q3FS5qXJT5abKNy3xEEs8xBIPMfHDqrxReaPyTSpvVN6ovFH5TUs8xBIPscRDTPxhVP4wSzzEEg+xxENM/LAqv0nlExU3KjdVbqrcVLmp8kblm5Z4iCUeYomHmPjDqPxhVG5UblRuVG5UblRuVD6xxEMs8RBLPMTEh6r8pCo3VW5UblRuVG5UblTeqLxR+aYlHmKJh1jiISa+rMpNlW9UuVF5o/JG5UblRuWmyk2Vb1riIZZ4iCUeYuKHVXmj8kblN6m8UXmj8puWeIglHmKJh5j4w6j8YZZ4iCUeYomHmPhhVf4lKm9UblRuVG5UblRuVG5UPrHEQyzxEEs8xMQfRuUPscRDLPEQSzzExA+r8pOqvFG5UXmj8kblRuWNyhuVb1riIZZ4iCUeYuLLqtxU+UaVmyo3Kt+o3FR5o/JNlW9a4iGWeIglHmLih1V5o/JG5TepvFF5o/KblniIJR5iiYeY+MOo/GGWeIglHmKJh5j4l1H5l1G5UblR+cQSD7HEQyzxELvDEouHWOIhlniIJR5iiYdY4iGWeIglHmKJh1jiIZZ4iCUeYomH+B9XYgF2OBbC7QAAAABJRU5ErkJggg==" alt="QR Code">
                </div>
              </div>
            </div>
            
            <div class="step">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>输入验证码</h4>
                <p>输入验证器应用生成的6位验证码</p>
                <div class="verification-code-input">
                  <input type="text" maxlength="6" placeholder="000000" v-model="twoFactorCode">
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="secondary-button" @click="showTwoFactorSetup = false">取消</button>
          <button class="primary-button" @click="verifyTwoFactorSetup">
            <i v-html="checkIcon"></i>
            <span>验证并启用</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 消息提示 -->
    <div class="toast-container" v-if="toast.show">
      <div class="toast" :class="toast.type">
        <div class="toast-icon">
          <i v-html="getToastIcon()"></i>
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ getToastTitle() }}</div>
          <div class="toast-message">{{ toast.message }}</div>
        </div>
        <button class="toast-close" @click="toast.show = false">
          <i v-html="closeIcon"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SystemSettings',
  data() {
    return {
      // 当前激活的设置部分
      activeSection: 'password',
      
      // 标签页配置
      tabs: [
        { 
          id: 'password', 
          name: '密码修改',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
        },
        { 
          id: 'appearance', 
          name: '外观设置',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
        },
        { 
          id: 'notification', 
          name: '通知设置',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>'
        },
        { 
          id: 'privacy', 
          name: '隐私安全',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
        }
      ],
      
      // 密码修改相关数据
      passwordInfo: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      
      // 验证码相关数据
      captcha: {
        code: '',
        key: '',
        image: '',
        cooldown: 0
      },
      isLoadingCaptcha: false,
      isSubmitting: false,
      
      // 外观设置相关数据
      displaySettings: {
        theme: 'light',
        themeColor: 'teal',
        fontSizeIndex: 1,
        enableAnimations: true,
        layout: 'comfortable'
      },
      themeColors: [
        { value: 'teal', hex: '#38b2ac' },
        { value: 'blue', hex: '#4facfe' },
        { value: 'purple', hex: '#805ad5' },
        { value: 'pink', hex: '#ed64a6' },
        { value: 'orange', hex: '#ed8936' },
        { value: 'green', hex: '#48bb78' }
      ],
      fontSizeOptions: ['小', '中', '大'],
      
      // 通知设置相关数据
      notificationSettings: {
        system: true,
        appointment: true,
        diagnosis: true,
        email: false,
        emailAddress: '',
        sms: true,
        phoneNumber: '',
        startTime: 8,
        endTime: 20
      },
      
      // 安全设置相关数据
      securitySettings: {
        twoFactor: false,
        loginAlert: true
      },
      
      // 表单验证错误信息
      errors: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
        captcha: ''
      },
      
      // 用户信息
      info: null,
      userName: '',
      userRole: '',
      
      // 模态框显示状态
      showLogoutConfirm: false,
      showSessionsModal: false,
      showActivityLogModal: false,
      showTwoFactorSetup: false,
      
      // 活动日志筛选
      activityLogFilter: {
        type: 'all',
        timeRange: '7'
      },
      
      // 两步验证码
      twoFactorCode: '',
      
      // 消息提示
      toast: {
        show: false,
        message: '',
        type: 'success'
      },
      
      // 定时器
      captchaTimer: null,
      
      // 图标
      eyeIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>',
      eyeOffIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>',
      checkIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
      xIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
      loadingIcon: '<svg class="spinner" viewBox="0 0 50 50" width="18" height="18"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>',
      saveIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>',
      resetIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v6h6"></path><path d="M3 13a9 9 0 1 0 3-7.7L3 8"></path></svg>',
      closeIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
      logoutIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>',
      warningIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
      successIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
      errorIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
      infoIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>',
      devicesIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>',
      historyIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
      downloadIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
      loginIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>',
      settingsIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>',
      securityIcon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
      deviceIcons: {
        desktop: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>',
        mobile: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>',
        tablet: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>'
      }
    };
  },
  computed: {
    // 密码强度计算
    passwordStrength() {
      const password = this.passwordInfo.newPassword;
      if (!password) {
        return { level: '', text: '', percent: 0 };
      }
      
      let strength = 0;
      let level = '';
      let text = '';
      
      // 长度检查
      if (password.length >= 8) strength += 25;
      
      // 包含小写字母
      if (/[a-z]/.test(password)) strength += 25;
      
      // 包含大写字母
      if (/[A-Z]/.test(password)) strength += 25;
      
      // 包含数字
      if (/[0-9]/.test(password)) strength += 25;
      
      // 包含特殊字符
      if (/[^A-Za-z0-9]/.test(password)) strength += 25;
      
      // 最大值为100
      strength = Math.min(100, strength);
      
      if (strength < 30) {
        level = 'weak';
        text = '弱';
      } else if (strength < 70) {
        level = 'medium';
        text = '中';
      } else {
        level = 'strong';
        text = '强';
      }
      
      return { level, text, percent: strength };
    },
    
    // 密码验证条件
    hasLowerCase() {
      return /[a-z]/.test(this.passwordInfo.newPassword);
    },
    hasUpperCase() {
      return /[A-Z]/.test(this.passwordInfo.newPassword);
    },
    hasNumber() {
      return /[0-9]/.test(this.passwordInfo.newPassword);
    },
    hasMinLength() {
      return this.passwordInfo.newPassword.length >= 8;
    }
  },
  mounted() {
    // 从本地存储获取用户信息
    const storedInfo = localStorage.getItem('info');
    if (storedInfo) {
      try {
        this.info = storedInfo;
        const parsedInfo = JSON.parse(storedInfo);
        if (parsedInfo.userName) {
          this.userName = parsedInfo.userName;
        }
        if (parsedInfo.userRole) {
          this.userRole = parsedInfo.userRole;
        }
      } catch (error) {
        console.error('解析用户信息失败:', error);
      }
    } else {
      this.showToast('请先登录', 'warning');
      // 这里可以添加跳转到登录页面的逻辑
    }
    
    // 获取验证码
    this.getCaptcha();
    
    // 加载保存的设置
    this.loadSavedSettings();
  },
  methods: {
    async getCaptcha() {
      if (this.captcha.cooldown > 0) return;
      
      this.isLoadingCaptcha = true;
      
      try {
        // 定义 POST 请求的配置
        const requestOptions = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({})
        };
        
        const response = await fetch('http://8.155.59.127:34561/Login/ImageCodeView/', requestOptions);
        const data = await response.json();
        
        if (data.code === 200) {
          this.captcha.key = data.key;
          this.captcha.image = data.image;
          this.errors.captcha = '';
          
          // 设置冷却时间
          this.captcha.cooldown = 5;
          this.startCaptchaCooldown();
        } else {
          this.errors.captcha = '获取验证码失败: ' + data.msg;
          this.showToast('获取验证码失败', 'error');
        }
      } catch (error) {
        console.error('Error getting captcha:', error);
        this.errors.captcha = '获取验证码时发生错误: ' + error.message;
        this.showToast('获取验证码失败', 'error');
      } finally {
        this.isLoadingCaptcha = false;
      }
    },
    
    startCaptchaCooldown() {
      // 清除之前的定时器
      if (this.captchaTimer) {
        clearInterval(this.captchaTimer);
      }
      
      // 设置新的定时器
      this.captchaTimer = setInterval(() => {
        if (this.captcha.cooldown > 0) {
          this.captcha.cooldown--;
        } else {
          clearInterval(this.captchaTimer);
        }
      }, 1000);
    },
    
    async changePassword() {
      this.validatePasswordForm();
      
      if (this.hasErrors()) {
        return;
      }
      
      this.isSubmitting = true;
      
      try {
        const parsedInfo = JSON.parse(this.info);
        if (!parsedInfo || !parsedInfo.token) {
          throw new Error('Token不存在');
        }
        
        const token = parsedInfo.token;
        const doctorId = parsedInfo.userId;
        
        const response = await fetch('http://8.155.59.127:34561/Login/alterPasswordView/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': `${token}`
          },
          body: JSON.stringify({
            doctor_id: doctorId,
            captcha_key: this.captcha.key,
            captcha_code: this.captcha.code,
            password: this.passwordInfo.newPassword,
            password_verify: this.passwordInfo.newPassword
          })
        });
        
        const data = await response.json();
        
        if (data.code === 200) {
          this.resetPasswordForm();
          this.showToast('密码修改成功', 'success');
        } else {
          this.errors.captcha = '验证码错误或已过期';
          this.showToast(data.msg || '密码修改失败', 'error');
        }
      } catch (error) {
        console.error('Error changing password:', error);
        this.showToast('修改密码时发生错误: ' + error.message, 'error');
      } finally {
        this.isSubmitting = false;
        // 无论成功与否，都刷新验证码
        this.getCaptcha();
      }
    },
    
    validatePasswordForm() {
      this.errors = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
        captcha: ''
      };
      
      if (!this.passwordInfo.currentPassword) {
        this.errors.currentPassword = '当前密码不能为空';
      }
      
      if (!this.passwordInfo.newPassword) {
        this.errors.newPassword = '新密码不能为空';
      } else if (this.passwordInfo.newPassword.length < 6) {
        this.errors.newPassword = '新密码长度至少为6位';
      }
      
      if (!this.passwordInfo.confirmPassword) {
        this.errors.confirmPassword = '请确认新密码';
      } else if (this.passwordInfo.newPassword !== this.passwordInfo.confirmPassword) {
        this.errors.confirmPassword = '新密码和确认密码不一致';
      }
      
      if (!this.captcha.code) {
        this.errors.captcha = '验证码不能为空';
      }
    },
    
    hasErrors() {
      return Object.values(this.errors).some(error => error !== '');
    },
    
    resetPasswordForm() {
      this.passwordInfo.currentPassword = '';
      this.passwordInfo.newPassword = '';
      this.passwordInfo.confirmPassword = '';
      this.captcha.code = '';
    },
    
    logout() {
      localStorage.removeItem('info');
      this.showToast('已成功退出登录', 'success');
      this.showLogoutConfirm = false;
      
      // 延迟跳转，让用户看到提示
      setTimeout(() => {
        // 这里可以添加跳转到登录页面的逻辑
        window.location.href = '/';
      }, 1500);
    },
    
    loadSavedSettings() {
      // 从本地存储加载设置
      const savedDisplaySettings = localStorage.getItem('displaySettings');
      if (savedDisplaySettings) {
        try {
          this.displaySettings = JSON.parse(savedDisplaySettings);
        } catch (error) {
          console.error('解析显示设置失败:', error);
        }
      }
      
      const savedNotificationSettings = localStorage.getItem('notificationSettings');
      if (savedNotificationSettings) {
        try {
          this.notificationSettings = JSON.parse(savedNotificationSettings);
        } catch (error) {
          console.error('解析通知设置失败:', error);
        }
      }
      
      const savedSecuritySettings = localStorage.getItem('securitySettings');
      if (savedSecuritySettings) {
        try {
          this.securitySettings = JSON.parse(savedSecuritySettings);
        } catch (error) {
          console.error('解析安全设置失败:', error);
        }
      }
    },
    
    saveDisplaySettings() {
      // 保存到本地存储
      localStorage.setItem('displaySettings', JSON.stringify(this.displaySettings));
      this.showToast('显示设置已保存', 'success');
      
      // 应用主题
      document.documentElement.setAttribute('data-theme', this.displaySettings.theme);
      document.documentElement.setAttribute('data-theme-color', this.displaySettings.themeColor);
      document.documentElement.setAttribute('data-font-size', this.fontSizeOptions[this.displaySettings.fontSizeIndex]);
      document.documentElement.setAttribute('data-animations', this.displaySettings.enableAnimations ? 'enabled' : 'disabled');
      document.documentElement.setAttribute('data-layout', this.displaySettings.layout);
    },
    
    resetDisplaySettings() {
      this.displaySettings = {
        theme: 'light',
        themeColor: 'teal',
        fontSizeIndex: 1,
        enableAnimations: true,
        layout: 'comfortable'
      };
      this.showToast('已恢复默认显示设置', 'info');
    },
    
    saveNotificationSettings() {
      // 保存到本地存储
      localStorage.setItem('notificationSettings', JSON.stringify(this.notificationSettings));
      this.showToast('通知设置已保存', 'success');
    },
    
    saveSecuritySettings() {
      // 保存到本地存储
      localStorage.setItem('securitySettings', JSON.stringify(this.securitySettings));
      this.showToast('安全设置已保存', 'success');
    },
    
    terminateSession(sessionId) {
      // 模拟终止会话
      this.showToast(`已终止会话: ${sessionId}`, 'success');
    },
    
    terminateAllSessions() {
      // 模拟终止所有会话
      this.showToast('已终止所有其他会话', 'success');
      this.showSessionsModal = false;
    },
    
    exportActivityLog() {
      // 模拟导出活动日志
      this.showToast('活动日志已导出', 'success');
    },
    
    exportUserData() {
      // 模拟导出用户数据
      this.showToast('用户数据已导出', 'success');
    },
    
    verifyTwoFactorSetup() {
      if (!this.twoFactorCode || this.twoFactorCode.length !== 6) {
        this.showToast('请输入6位验证码', 'error');
        return;
      }
      
      // 模拟验证成功
      this.showToast('两步验证已成功启用', 'success');
      this.showTwoFactorSetup = false;
    },
    
    showToast(message, type = 'success') {
      this.toast = {
        show: true,
        message,
        type
      };
      
      // 3秒后自动关闭
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    },
    
    getToastIcon() {
      switch (this.toast.type) {
        case 'success':
          return this.successIcon;
        case 'error':
          return this.errorIcon;
        case 'warning':
          return this.warningIcon;
        case 'info':
          return this.infoIcon;
        default:
          return this.infoIcon;
      }
    },
    
    getToastTitle() {
      switch (this.toast.type) {
        case 'success':
          return '成功';
        case 'error':
          return '错误';
        case 'warning':
          return '警告';
        case 'info':
          return '提示';
        default:
          return '提示';
      }
    }
  },
  beforeDestroy() {
    // 清除定时器
    if (this.captchaTimer) {
      clearInterval(this.captchaTimer);
    }
  }
};
</script>

<style scoped>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  color: #2c3e50;
  background-color: #f5f7fa;
}

.settings-container {
  max-width: 1000px;
  margin: 30px auto;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  animation: fadeIn 0.5s ease;
}

/* 页面标题 */
.page-header {
  background: linear-gradient(135deg, #69aee2 0%, #449ae1 100%);
  color: white;
  padding: 2.5rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.3;
}

.header-content {
  position: relative;
  z-index: 1;
}

.page-header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  font-weight: 300;
}

/* 标签页导航 */
.tabs-container {
  display: flex;
  background-color: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  overflow-x: auto;
  scrollbar-width: none;
}

.tabs-container::-webkit-scrollbar {
  display: none;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.tab-button:hover {
  color: #4fa0e2;
  background-color: #f1f5f9;
}

.tab-button.active {
  color: #4fa0e2;
  border-bottom-color: #4fa0e2;
  background-color: #f1f5f9;
}

.tab-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 设置内容区域 */
.settings-content {
  padding: 2rem;
}

/* 设置卡片 */
.settings-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  animation: fadeIn 0.4s ease;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: #2d3748;
}

.card-header p {
  margin: 0;
  color: #64748b;
  font-size: 0.95rem;
}

.card-body {
  padding: 1.5rem;
}

.card-footer {
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 表单样式 */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
  background-color: white;
}

.form-group input.error {
  border-color: #e53e3e;
}

.form-group input:focus {
  border-color: #38b2ac;
  box-shadow: 0 0 0 3px rgba(56, 178, 172, 0.2);
  outline: none;
}

.toggle-password {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-password:hover {
  color: #718096;
}

.captcha-container {
  display: flex;
  gap: 1rem;
}

.captcha-container input {
  flex: 1;
}

.captcha-wrapper {
  position: relative;
  width: 120px;
  height: 44px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.captcha-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.captcha-refresh {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.captcha-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.captcha-tip {
  font-size: 0.8rem;
  color: #718096;
  margin-top: 0.5rem;
}

.error-message {
  color: #e53e3e;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  display: block;
}

/* 密码强度指示器 */
.password-strength {
  margin-top: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.strength-label {
  font-size: 0.85rem;
  color: #718096;
}

.strength-meter {
  flex: 1;
  height: 6px;
  background-color: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.strength-value {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.strength-value.weak {
  background-color: #e53e3e;
}

.strength-value.medium {
  background-color: #ed8936;
}

.strength-value.strong {
  background-color: #38a169;
}

.strength-text {
  font-size: 0.85rem;
  font-weight: 500;
}

.strength-text.weak {
  color: #e53e3e;
}

.strength-text.medium {
  color: #ed8936;
}

.strength-text.strong {
  color: #38a169;
}

/* 密码提示 */
.password-tips {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #718096;
}

.tip-item i {
  display: flex;
  align-items: center;
  justify-content: center;
}

.tip-item.valid {
  color: #38a169;
}

/* 按钮样式 */
.primary-button,
.secondary-button,
.danger-button,
.action-button,
.text-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.primary-button {
  background: linear-gradient(135deg, #4fa0e2 0%, #4299e1 100%);
  color: white;
}

.primary-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(56, 178, 172, 0.3);
}

.secondary-button {
  background-color: #edf2f7;
  color: #4a5568;
}

.secondary-button:hover {
  background-color: #e2e8f0;
  color: #2d3748;
}

.danger-button {
  background-color: #e53e3e;
  color: white;
}

.danger-button:hover {
  background-color: #c53030;
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.3);
}

.action-button {
  background-color: #f7fafc;
  color: #4a5568;
  border: 1px solid #e2e8f0;
}

.action-button:hover {
  background-color: #edf2f7;
  color: #2d3748;
}

.text-button {
  background: none;
  color: #38b2ac;
  padding: 0.25rem 0.5rem;
}

.text-button:hover {
  background-color: #f7fafc;
}

.text-button.danger {
  color: #e53e3e;
}

.text-button.danger:hover {
  background-color: #fff5f5;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 主题选择 */
.theme-options {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.theme-preview {
  width: 100px;
  height: 70px;
  border-radius: 8px;
  border: 2px solid #e2e8f0;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.theme-option.active .theme-preview {
  border-color: #38b2ac;
  box-shadow: 0 0 0 3px rgba(56, 178, 172, 0.2);
}

.light-theme {
  background-color: white;
}

.light-theme::after {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  height: 10px;
  background-color: #e2e8f0;
  border-radius: 5px;
}

.dark-theme {
  background-color: #1a202c;
}

.dark-theme::after {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  height: 10px;
  background-color: #4a5568;
  border-radius: 5px;
}

.auto-theme {
  background: linear-gradient(to right, white 50%, #1a202c 50%);
}

.auto-theme::after {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  height: 10px;
  background: linear-gradient(to right, #e2e8f0 50%, #4a5568 50%);
  border-radius: 5px;
}

.theme-option span {
  font-size: 0.9rem;
  color: #4a5568;
}

.theme-option.active span {
  color: #38b2ac;
  font-weight: 500;
}

/* 颜色选择 */
.color-options {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.color-option {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: #2d3748;
  box-shadow: 0 0 0 3px rgba(45, 55, 72, 0.2);
}

/* 字体大小滑块 */
.font-size-slider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.size-label {
  font-size: 1rem;
  color: #4a5568;
}

.size-label.large {
  font-size: 1.5rem;
}

.font-size-slider input[type="range"] {
  flex: 1;
  -webkit-appearance: none;
  height: 6px;
  background-color: #e2e8f0;
  border-radius: 3px;
  outline: none;
}

.font-size-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #38b2ac;
  cursor: pointer;
}

.font-size-value {
  text-align: center;
  font-size: 0.9rem;
  color: #718096;
  margin-bottom: 1.5rem;
}

/* 布局选择 */
.layout-options {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.layout-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.layout-preview {
  width: 100px;
  height: 70px;
  border-radius: 8px;
  border: 2px solid #e2e8f0;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.layout-option.active .layout-preview {
  border-color: #38b2ac;
  box-shadow: 0 0 0 3px rgba(56, 178, 172, 0.2);
}

.compact-layout {
  background-color: #f8fafc;
  display: flex;
  flex-direction: column;
}

.compact-layout::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
}

.compact-layout::after {
  content: '';
  position: absolute;
  top: 25px;
  left: 10px;
  right: 10px;
  height: 30px;
  background-color: #edf2f7;
  border-radius: 4px;
}

.comfortable-layout {
  background-color: #f8fafc;
  display: flex;
  flex-direction: column;
}

.comfortable-layout::before {
  content: '';
  position: absolute;
  top: 15px;
  left: 15px;
  right: 15px;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
}

.comfortable-layout::after {
  content: '';
  position: absolute;
  top: 35px;
  left: 15px;
  right: 15px;
  height: 20px;
  background-color: #edf2f7;
  border-radius: 4px;
}

.layout-option span {
  font-size: 0.9rem;
  color: #4a5568;
}

.layout-option.active span {
  color: #38b2ac;
  font-weight: 500;
}

/* 开关样式 */
.toggle-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e0;
  transition: 0.4s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.toggle-switch input:checked + .toggle-slider {
  background-color: #4299e1;
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.toggle-label {
  font-size: 0.9rem;
  color: #4a5568;
}

.setting-description {
  font-size: 0.85rem;
  color: #718096;
  margin-top: 0.5rem;
}

/* 通知选项 */
.notification-options {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.notification-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.option-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #2d3748;
}

.option-info p {
  margin: 0;
  font-size: 0.9rem;
  color: #718096;
}

.input-with-toggle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.input-with-toggle input {
  width: 200px;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
}

.time-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.time-range select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
}

/* 安全选项 */
.security-options {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.security-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.option-action {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-container {
  background-color: white;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: scaleIn 0.3s ease;
}

.modal-container.large {
  width: 600px;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #2d3748;
}

.close-button {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
}

.close-button:hover {
  color: #718096;
}

.modal-content {
  padding: 1.5rem;
}

.modal-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.modal-icon.warning {
  color: #ed8936;
}

.modal-content p {
  margin: 0;
  color: #4a5568;
  text-align: center;
}

.modal-actions {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 会话列表 */
.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  background-color: #f7fafc;
}

.session-item.current {
  background-color: #e6fffa;
  border: 1px solid #b2f5ea;
}

.session-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #edf2f7;
  color: #4a5568;
}

.session-info {
  flex: 1;
}

.session-name {
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.session-details {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #718096;
}

.session-actions {
  display: flex;
  align-items: center;
}

.current-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background-color: #38b2ac;
  color: white;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* 活动日志 */
.activity-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.85rem;
  color: #718096;
}

.filter-group select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  background-color: #f7fafc;
}

.activity-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
}

.activity-icon.login {
  background-color: #4299e1;
}

.activity-icon.settings {
  background-color: #38b2ac;
}

.activity-icon.security {
  background-color: #ed8936;
}

.activity-info {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.activity-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.85rem;
  color: #718096;
}

/* 两步验证设置 */
.setup-steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step {
  display: flex;
  gap: 1rem;
  opacity: 0.5;
}

.step.active {
  opacity: 1;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #38b2ac;
  color: white;
  font-weight: 600;
}

.step-content h4 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
}

.step-content p {
  margin: 0 0 1rem 0;
  color: #718096;
  font-size: 0.9rem;
}

.qr-code {
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.qr-code img {
  width: 150px;
  height: 150px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.verification-code-input {
  display: flex;
  justify-content: center;
}

.verification-code-input input {
  width: 150px;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1.2rem;
  text-align: center;
  letter-spacing: 2px;
}

/* 消息提示 */
.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1100;
}

.toast {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease;
  background-color: white;
  border-left: 4px solid #38b2ac;
  min-width: 300px;
  max-width: 400px;
}

.toast.success {
  border-left-color: #38a169;
}

.toast.error {
  border-left-color: #e53e3e;
}

.toast.warning {
  border-left-color: #ed8936;
}

.toast.info {
  border-left-color: #4299e1;
}

.toast-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
}

.toast.success .toast-icon {
  color: #38a169;
}

.toast.error .toast-icon {
  color: #e53e3e;
}

.toast.warning .toast-icon {
  color: #ed8936;
}

.toast.info .toast-icon {
  color: #4299e1;
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #2d3748;
}

.toast-message {
  font-size: 0.9rem;
  color: #718096;
}

.toast-close {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  margin-left: 0.5rem;
}

.toast-close:hover {
  color: #718096;
}

/* 加载动画 */
.spinner {
  animation: rotate 2s linear infinite;
}

.spinner .path {
  stroke: currentColor;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
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

@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-content {
    padding: 1rem;
  }
  
  .theme-options,
  .color-options,
  .layout-options {
    flex-wrap: wrap;
  }
  
  .captcha-container {
    flex-direction: column;
  }
  
  .captcha-wrapper {
    width: 100%;
  }
  
  .input-with-toggle {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .input-with-toggle input {
    width: 100%;
  }
  
  .card-footer {
    flex-direction: column;
  }
  
  .card-footer button {
    width: 100%;
  }
  
  .modal-container.large {
    width: 90%;
  }
  
  .activity-filters {
    flex-direction: column;
  }
  
  .password-tips {
    grid-template-columns: 1fr;
  }
}
</style>
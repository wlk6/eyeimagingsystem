<template>
  <div class="login-container" :style="gradientStyle">
    <div class="login-box" :class="{ 'animate-in': animateIn }">
      <div class="login-header">
        <div class="logo-container">
          <div class="logo-circle">
            <div class="eye-icon">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                <path d="M12 14c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"/>
              </svg>
            </div>
          </div>
        </div>
        <h1>慧眼视界</h1>
        <p>AI驱动眼底影像智能诊断</p>
      </div>
      
      <div class="login-form">
        <div class="role-selector">
          <div 
            :class="['role-option', { active: role === 'doctor' }]" 
            @click="role = 'doctor'"
          >
            医生登录
          </div>
          <div 
            :class="['role-option', { active: role === 'admin' }]" 
            @click="role = 'admin'"
          >
            管理员登录
          </div>
        </div>
        
        <div class="input-group" :class="{ 'focused': focusedField === 'id' }">
          <label>账号</label>
          <input 
            type="text" 
            v-model="loginForm.ID" 
            placeholder="请输入账号" 
            @focus="focusedField = 'id'"
            @blur="focusedField = null"
          />
        </div>
        
        <div class="input-group" :class="{ 'focused': focusedField === 'password' }">
          <label>密码</label>
          <input 
            type="password" 
            v-model="loginForm.password" 
            placeholder="请输入密码" 
            @focus="focusedField = 'password'"
            @blur="focusedField = null"
          />
        </div>
        
        <div class="error-message" v-if="errorMsg">
          <transition name="fade">
            <div>{{ errorMsg }}</div>
          </transition>
        </div>
        
        <button class="login-button" @click="handleLogin" :disabled="isLoading">
          <span v-if="!isLoading">登录</span>
          <span v-else class="loading-spinner"></span>
        </button>
        
        <div class="login-footer">
          <a href="#">忘记密码?</a>
          <a href="#">联系管理员</a>
        </div>
      </div>
    </div>

    <!-- 通知弹窗 -->
    <transition name="notification">
      <div v-if="notification.show" class="notification" :class="notification.type">
        <div class="notification-icon">
          <svg v-if="notification.type === 'success'" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <svg v-if="notification.type === 'error'" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        </div>
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
        </div>
        <button class="notification-close" @click="closeNotification">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <div class="notification-progress" :style="{ width: `${notificationProgress}%` }"></div>
      </div>
    </transition>
  </div>
</template>

<script>
import {login} from '@/api/login.js';
import {adminlog} from '@/api/adminlog.js';
export default {
  name: 'Login',
  data() {
    return {
      role: 'doctor', // 默认为医生登录
      loginForm: {
        ID: '',
        password: ''
      },
      errorMsg: '',
      isLoading: false,
      focusedField: null,
      animateIn: false,
      gradientStyle: {
        background: 'linear-gradient(135deg, #72b3e3, #b0d3f1)'
      },
      notification: {
        show: false,
        type: 'success', // 'success' 或 'error'
        title: '',
        message: '',
        timeout: null
      },
      notificationProgress: 100,
      notificationInterval: null
    }
  },
  mounted() {
    // 添加进入动画
    setTimeout(() => {
      this.animateIn = true;
    }, 100);
  },
  methods: {
    validateForm() {
      if (!this.loginForm.ID.trim()) {
        this.errorMsg = '请输入账号';
        return false;
      }
      if (!this.loginForm.password.trim()) {
        this.errorMsg = '请输入密码';
        return false;
      }
      return true;
    },
    async handleLogin() {
      if (!this.validateForm()) {
        return;
      }
      
      this.errorMsg = '';
      this.isLoading = true;
      
      try {
        // 根据角色选择不同的登录API
        let islog;
        if(this.role === 'admin') {
          islog = await adminlog(this.loginForm.ID, this.loginForm.password);
        } else {
          islog = await login(this.loginForm.ID, this.loginForm.password);
        }
        
        // 无论成功与否都显示通知
        if(islog.msg === '登录成功') {
          this.showNotification('success', '登录成功', `欢迎回来，${this.role === 'admin' ? '管理员' : '医生'}！`);
          
          // 存储用户信息并跳转
          this.$store.commit('user/setUserInfo', { userId: this.loginForm.ID, token: islog.token });
          
          // 延迟跳转，让用户看到成功通知
          setTimeout(() => {
            this.$router.push({ path: this.role === 'admin' ? '/admin' : '/doctor' });
          }, 1500);
        } else {
          // 登录失败
          this.showNotification('error', '登录失败', islog.msg || '账号或密码错误，请重试');
        }
      } catch (error) {
        console.error('登录错误:', error);
        this.showNotification('error', '登录失败', '网络错误，请稍后重试');
      } finally {
        this.isLoading = false;
      }
    },
    
    // 显示通知
    showNotification(type, title, message) {
      // 清除之前的通知计时器
      if (this.notification.timeout) {
        clearTimeout(this.notification.timeout);
      }
      
      if (this.notificationInterval) {
        clearInterval(this.notificationInterval);
      }
      
      // 设置新通知
      this.notification = {
        show: true,
        type,
        title,
        message,
        timeout: null
      };
      
      // 设置进度条
      this.notificationProgress = 100;
      const duration = 5000; // 5秒后自动关闭
      const interval = 50; // 每50毫秒更新一次进度条
      const step = (interval / duration) * 100;
      
      this.notificationInterval = setInterval(() => {
        this.notificationProgress -= step;
        if (this.notificationProgress <= 0) {
          this.closeNotification();
        }
      }, interval);
      
      // 设置自动关闭
      this.notification.timeout = setTimeout(() => {
        this.closeNotification();
      }, duration);
    },
    
    // 关闭通知
    closeNotification() {
      this.notification.show = false;
      
      if (this.notification.timeout) {
        clearTimeout(this.notification.timeout);
      }
      
      if (this.notificationInterval) {
        clearInterval(this.notificationInterval);
      }
    }
  }
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-size: 400% 400%;
  animation: gradientAnimation 15s ease infinite;
  position: relative;
  overflow: hidden;
}

@keyframes gradientAnimation {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 60%);
  animation: rotateGradient 30s linear infinite;
  pointer-events: none;
}

@keyframes rotateGradient {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.login-box {
  width: 420px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  padding: 40px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.22, 1, 0.36, 1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-box.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #72b3e3, #b0d3f1);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(114, 179, 227, 0.3);
  position: relative;
  overflow: hidden;
}

.logo-circle::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.3), rgba(255,255,255,0));
  transform: rotate(25deg);
  animation: shimmer 3s infinite;
  background-size: 50% 100%;
}

.eye-icon {
  margin: 0;
  animation: pulse 2s infinite;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
  animation: fadeIn 0.8s ease-out forwards;
  animation-delay: 0.3s;
  opacity: 0;
}

.login-header h1 {
  font-size: 24px;
  color: #333;
  margin: 15px 0 10px;
  font-weight: 600;
}

.login-header p {
  font-size: 14px;
  color: #666;
  opacity: 0.8;
}

.role-selector {
  display: flex;
  margin-bottom: 25px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(114, 179, 227, 0.3);
  position: relative;
  animation: fadeIn 0.8s ease-out forwards;
  animation-delay: 0.5s;
  opacity: 0;
  box-shadow: 0 2px 10px rgba(114, 179, 227, 0.1);
}

.role-option {
  flex: 1;
  text-align: center;
  padding: 14px 0;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  background-color: rgba(245, 247, 250, 0.8);
  color: #666;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.role-option::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #72b3e3, #b0d3f1);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.role-option:hover::before {
  opacity: 0.1;
}

.role-option.active {
  background: linear-gradient(135deg, #72b3e3, #b0d3f1);
  color: white;
  font-weight: 500;
}

.role-option.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: white;
  transform: scaleX(0.7);
  opacity: 0.7;
}

.input-group {
  margin-bottom: 20px;
  position: relative;
  animation: fadeIn 0.8s ease-out forwards;
  opacity: 0;
}

.input-group:nth-child(3) {
  animation-delay: 0.7s;
}

.input-group:nth-child(4) {
  animation-delay: 0.9s;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
  font-weight: 500;
  transition: color 0.3s ease;
}

.input-group.focused label {
  color: #72b3e3;
}

.input-group input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid rgba(114, 179, 227, 0.3);
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: rgba(245, 247, 250, 0.5);
}

.input-group input:focus {
  border-color: #72b3e3;
  outline: none;
  box-shadow: 0 0 0 3px rgba(114, 179, 227, .02);
  background-color: white;
}

.input-group.focused input {
  border-color: #72b3e3;
  box-shadow: 0 0 0 3px rgba(114, 179, 227, 0.2);
  background-color: white;
}

.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-bottom: 15px;
  min-height: 20px;
  animation: fadeIn 0.8s ease-out forwards;
  animation-delay: 1.1s;
  opacity: 0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

.login-button {
  width: 100%;
  padding: 14px 0;
  background: linear-gradient(135deg, #72b3e3, #b0d3f1);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-weight: 500;
  animation: fadeIn 0.8s ease-out forwards;
  animation-delay: 1.3s;
  opacity: 0;
  box-shadow: 0 4px 15px rgba(114, 179, 227, 0.3);
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.2), rgba(255,255,255,0));
  transition: left 0.5s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(114, 179, 227, 0.4);
}

.login-button:hover::before {
  left: 100%;
}

.login-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 10px rgba(114, 179, 227, 0.3);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

.login-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 25px;
  font-size: 14px;
  animation: fadeIn 0.8s ease-out forwards;
  animation-delay: 1.5s;
  opacity: 0;
}

.login-footer a {
  color: #72b3e3;
  text-decoration: none;
  transition: color 0.3s ease;
  position: relative;
}

.login-footer a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: #72b3e3;
  transform: scaleX(0);
  transition: transform 0.3s ease;
  transform-origin: right;
}

.login-footer a:hover {
  color: #5a90b9;
}

.login-footer a:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

/* 通知弹窗样式 */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 360px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: flex-start;
  padding: 16px;
  z-index: 1000;
  overflow: hidden;
  animation: slideInNotification 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes slideInNotification {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-enter-active {
  animation: slideInNotification 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.notification-leave-active {
  animation: slideInNotification 0.5s cubic-bezier(0.22, 1, 0.36, 1) reverse;
}

.notification.success {
  border-left: 4px solid #52c41a;
}

.notification.error {
  border-left: 4px solid #ff4d4f;
}

.notification-icon {
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.notification.success .notification-icon {
  color: #52c41a;
}

.notification.error .notification-icon {
  color: #ff4d4f;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
  color: #333;
}

.notification-message {
  font-size: 14px;
  color: #666;
}

.notification-close {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
  margin-left: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s;
}

.notification-close:hover {
  color: #333;
}

.notification-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #72b3e3, #b0d3f1);
  transition: width 0.1s linear;
}

.notification.success .notification-progress {
  background: linear-gradient(90deg, #b7eb8f, #52c41a);
}

.notification.error .notification-progress {
  background: linear-gradient(90deg, #ffccc7, #ff4d4f);
}
</style>
<template>
  <div class="doctor-profile-container" style="margin-top:0px">
    <div class="main-content">
      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>正在加载个人信息...</p>
      </div>

      <!-- 错误提示 -->
      <div v-else-if="error" class="error-container">
        <div class="error-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <p>{{ error }}</p>
        <button class="btn-retry" @click="fetchDoctorInfo">重试</button>
      </div>

      <!-- 个人信息展示 -->
      <div v-else class="profile-content">
        <div class="profile-card">
          <div class="profile-header-section">
            <div class="avatar-container">
              <div class="avatar" :style="{ backgroundImage: doctorInfo.avatar ? `url(http://8.155.59.127:34561/user${doctorInfo.avatar})` : 'none' }">
                <span v-if="!doctorInfo.avatar">{{ getInitials(doctorInfo.doctor_name) }}</span>
              </div>
              <div class="doctor-name-position">
                <h2>{{ doctorInfo.doctor_name || '未设置姓名' }}</h2>
                <span class="position-badge">{{ getPositionText(doctorInfo.position) }}</span>
              </div>
            </div>
            <button class="btn-edit" @click="toggleEditMode" v-if="!isEditMode">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              编辑资料
            </button>
          </div>

          <!-- 查看模式 -->
          <div v-if="!isEditMode" class="profile-details">
            <div class="detail-row">
              <div class="detail-label">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                姓名
              </div>
              <div class="detail-value">{{ doctorInfo.doctor_name || '未设置' }}</div>
            </div>

            <div class="detail-row">
              <div class="detail-label">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
                电话
              </div>
              <div class="detail-value">{{ doctorInfo.phone || '未设置' }}</div>
            </div>

            <div class="detail-row">
              <div class="detail-label">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
                邮箱
              </div>
              <div class="detail-value">{{ doctorInfo.email || '未设置' }}</div>
            </div>

            <div class="detail-row">
              <div class="detail-label">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="8.5" cy="7" r="4"></circle>
                  <line x1="20" y1="8" x2="20" y2="14"></line>
                  <line x1="23" y1="11" x2="17" y2="11"></line>
                </svg>
                性别
              </div>
              <div class="detail-value">{{ doctorInfo.gender || '未设置' }}</div>
            </div>

            <div class="detail-row">
              <div class="detail-label">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
                职位
              </div>
              <div class="detail-value">{{ getPositionText(doctorInfo.position) }}</div>
            </div>

            <div class="detail-row">
              <div class="detail-label">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                个人简介
              </div>
              <div class="detail-value intro-text">{{ doctorInfo.introduce || '暂无个人简介' }}</div>
            </div>
          </div>

          <!-- 编辑模式 -->
          <div v-else class="profile-edit-form">
            <form @submit.prevent="submitForm">
              <div class="form-group">
                <label>头像</label>
                <div class="avatar-upload-container">
                  <div class="avatar-preview" :style="{ backgroundImage: previewImage ? `url(${previewImage})` : (doctorInfo.avatar ? `url(${doctorInfo.avatar})` : 'none') }"></div>
                  <button type="button" class="avatar-upload-btn" @click="openFilePicker">
                    选择图片
                  </button>
                  <input type="file" ref="avatarInput" accept="image/*" style="display: none;" @change="handleFileChange">
                </div>
              </div>

              <div class="form-group">
                <label for="doctorName">姓名</label>
                <input 
                  type="text" 
                  id="doctorName" 
                  v-model="editForm.doctor_name" 
                  placeholder="请输入姓名"
                />
              </div>

              <div class="form-group">
                <label for="phone">电话</label>
                <input 
                  type="tel" 
                  id="phone" 
                  v-model="editForm.phone" 
                  placeholder="请输入电话号码"
                />
              </div>

              <div class="form-group">
                <label for="email">邮箱</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="editForm.email" 
                  placeholder="请输入邮箱地址"
                />
              </div>

              <div class="form-group">
                <label>性别</label>
                <div class="radio-group">
                  <label class="radio-label">
                    <input type="radio" v-model="editForm.gender" value="男" />
                    <span>男</span>
                  </label>
                  <label class="radio-label">
                    <input type="radio" v-model="editForm.gender" value="女" />
                    <span>女</span>
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label for="introduce">个人简介</label>
                <textarea 
                  id="introduce" 
                  v-model="editForm.introduce" 
                  rows="4" 
                  placeholder="请输入个人简介"
                ></textarea>
              </div>

              <div class="captcha-section">
                <div class="form-group">
                  <label for="captcha">验证码</label>
                  <div class="captcha-container">
                    <input 
                      type="text" 
                      id="captcha" 
                      v-model="editForm.captcha_code" 
                      placeholder="请输入验证码"
                    />
                    <div class="captcha-image" @click="refreshCaptcha">
                      <img v-if="captchaImage" :src="captchaImage" alt="验证码" />
                      <div v-else class="captcha-loading">
                        <div class="loading-spinner-small"></div>
                      </div>
                    </div>
                  </div>
                  <small class="captcha-hint">点击图片刷新验证码</small>
                </div>
              </div>

              <div class="form-actions">
                <button type="button" class="btn-cancel" @click="cancelEdit">取消</button>
                <button type="submit" class="btn-save" :disabled="isSubmitting">
                  {{ isSubmitting ? '保存中...' : '保存修改' }}
                  <span v-if="isSubmitting" class="spinner-small"></span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <div class="profile-stats">
          <div class="stats-card">
            <h3>工作统计</h3>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ getRandomNumber(10, 100) }}</div>
                <div class="stat-label">本月接诊</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ getRandomNumber(100, 1000) }}</div>
                <div class="stat-label">总接诊量</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ getRandomNumber(1, 10) }}年</div>
                <div class="stat-label">从业年限</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ getRandomNumber(90, 100) }}%</div>
                <div class="stat-label">满意度</div>
              </div>
            </div>
          </div>

          <div class="recent-activity">
            <h3>最近活动</h3>
            <div class="activity-list">
              <div class="activity-item">
                <div class="activity-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                </div>
                <div class="activity-content">
                  <div class="activity-title">完成诊断</div>
                  <div class="activity-desc">您完成了一例眼部诊断</div>
                  <div class="activity-time">2小时前</div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                  </svg>
                </div>
                <div class="activity-content">
                  <div class="activity-title">更新病例</div>
                  <div class="activity-desc">您更新了患者张三的病例记录</div>
                  <div class="activity-time">昨天</div>
                </div>
              </div>
              <div class="activity-item">
                <div class="activity-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                </div>
                <div class="activity-content">
                  <div class="activity-title">预约提醒</div>
                  <div class="activity-desc">明天有3位患者预约</div>
                  <div class="activity-time">2天前</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 消息提示 -->
    <div class="toast" v-if="toast.show">
      <div class="toast-content" :class="toast.type">
        <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <svg v-else-if="toast.type === 'error'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorProfile',
  data() {
    return {
      positionMapping: {
        chief_physician: '主任医师',
        associate_physician: '副主任医师',
        attending_doctor: '主治医师'
      },
      isLoading: true,
      error: null,
      doctorInfo: {
        doctor_id: null,
        doctor_name: '',
        phone: '',
        email: '',
        gender: '',
        position: '',
        avatar: null,
        introduce: ''
      },
      isEditMode: false,
      editForm: {
        doctor_name: '',
        phone: '',
        email: '',
        gender: '',
        introduce: '',
        captcha_code: '',
        avatar: null
      },
      captchaKey: '',
      captchaImage: '',
      isSubmitting: false,
      toast: {
        show: false,
        message: '',
        type: 'success'
      },
      previewImage: null
    };
  },
  mounted() {
    this.fetchDoctorInfo();
    document.body.style.overflow = 'hidden';
  },
  beforeDestroy() {
    document.body.style.overflow = 'auto';
  },
  methods: {
    async fetchDoctorInfo() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const info = localStorage.getItem('info');
        if (!info) {
          throw new Error('未找到登录信息，请重新登录');
        }
        
        const parsedInfo = JSON.parse(info);
        if (!parsedInfo.token || !parsedInfo.userId) {
          throw new Error('登录信息不完整，请重新登录');
        }
        
        const response = await fetch('http://8.155.59.127:34561/user/getDoctorInfo/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': parsedInfo.token,
          },
          body: JSON.stringify({ doctor_id: parsedInfo.userId })
        });
        
        const data = await response.json();
        
        if (data.code !== 200) {
          throw new Error(data.msg || '获取医生信息失败');
        }
        
        this.doctorInfo = {
          ...data.data,
          position: this.positionMapping[data.data.position] || data.data.position
        };
        
      } catch (error) {
        console.error('获取医生信息错误:', error);
        this.error = error.message || '获取医生信息失败，请稍后重试';
      } finally {
        this.isLoading = false;
      }
    },
    
    toggleEditMode() {
      document.body.style.overflow = 'auto';
      this.isEditMode = true;
      this.editForm = {
        doctor_name: this.doctorInfo.doctor_name || '',
        phone: this.doctorInfo.phone || '',
        email: this.doctorInfo.email || '',
        gender: this.doctorInfo.gender || '',
        introduce: this.doctorInfo.introduce || '',
        captcha_code: '',
        avatar: this.doctorInfo.avatar
      };
      this.previewImage = this.doctorInfo.avatar;
      this.fetchCaptcha();
    },
    
    cancelEdit() {
      this.isEditMode = false;
      this.previewImage = null;
      this.captchaImage = '';
      this.captchaKey = '';
      document.body.style.overflow = 'hidden';
    },
    
    async fetchCaptcha() {
      try {
        const response = await fetch('http://8.155.59.127:34561/Login/ImageCodeView/', {
          method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.code !== 200) {
          throw new Error('获取验证码失败');
        }
        
        this.captchaKey = data.key;
        this.captchaImage = data.image;
        
      } catch (error) {
        console.error('获取验证码错误:', error);
        this.showToast('获取验证码失败，请刷新重试', 'error');
      }
    },
    
    refreshCaptcha() {
      this.captchaImage = '';
      this.fetchCaptcha();
    },
    
    openFilePicker() {
      this.$refs.avatarInput.click();
    },
    
    handleFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewImage = e.target.result;
        this.editForm.avatar = file;
      };
      reader.readAsDataURL(file);
    },
    
    async submitForm() {
      if (!this.editForm.captcha_code) {
        this.showToast('请输入验证码', 'error');
        return;
      }
      
      this.isSubmitting = true;
      
      try {
        const info = localStorage.getItem('info');
        if (!info) {
          throw new Error('未找到登录信息，请重新登录');
        }
        
        const parsedInfo = JSON.parse(info);
        if (!parsedInfo.token || !parsedInfo.userId) {
          throw new Error('登录信息不完整，请重新登录');
        }
        
        const formData = new FormData();
        formData.append('doctor_id', parsedInfo.userId);
        formData.append('captcha_key', this.captchaKey);
        formData.append('captcha_code', this.editForm.captcha_code);
        
        if (this.editForm.doctor_name !== this.doctorInfo.doctor_name) {
          formData.append('doctor_name', this.editForm.doctor_name);
        }
        
        if (this.editForm.phone !== this.doctorInfo.phone) {
          formData.append('phone', this.editForm.phone);
        }
        
        if (this.editForm.email !== this.doctorInfo.email) {
          formData.append('email', this.editForm.email);
        }
        
        if (this.editForm.gender !== this.doctorInfo.gender) {
          formData.append('gender', this.editForm.gender);
        }
        
        if (this.editForm.introduce !== this.doctorInfo.introduce) {
          formData.append('introduce', this.editForm.introduce);
        }
        
        if (this.editForm.avatar) {
          formData.append('avatar', this.editForm.avatar);
        }
        
        const response = await fetch('http://8.155.59.127:34561/user/doctorAlterInfo/', {
          method: 'POST',
          headers: {
            'token': parsedInfo.token
          },
          body: formData
        });
        
        const data = await response.json();
        
        if (data.code !== 200) {
          throw new Error(data.msg || '更新信息失败');
        }
        
        await this.fetchDoctorInfo();
        this.isEditMode = false;
        this.showToast('个人信息更新成功，等待管理员审核', 'success');
        document.body.style.overflow = 'hidden';
      } catch (error) {
        console.error('更新医生信息错误:', error);
        this.showToast(error.message || '更新信息失败，请稍后重试', 'error');
        this.refreshCaptcha();
      } finally {
        this.isSubmitting = false;
      }
    },
    
    showToast(message, type = 'success') {
      this.toast = {
        show: true,
        message,
        type
      };
      
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    },
    
    getInitials(name) {
      if (!name) return '医';
      return name.charAt(0);
    },
    
    getPositionText(position) {
      const positionMap = {
        'attending_doctor': '主治医师',
        'chief_doctor': '主任医师',
        'associate_chief_doctor': '副主任医师',
        'resident_doctor': '住院医师',
        'intern': '实习医师'
      };
      
      return positionMap[position] || position || '未设置职位';
    },
    
    getRandomNumber(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }
  }
};
</script>

<style scoped>
.doctor-profile-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #2c3e50;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.profile-header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 600;
  letter-spacing: 1px;
}

.subtitle {
  margin-top: 0.5rem;
  font-size: 1.1rem;
  opacity: 0.9;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  margin-top: 65px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(79, 172, 254, 0.2);
  border-radius: 50%;
  border-top-color: #4facfe;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-spinner-small {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(79, 172, 254, 0.2);
  border-radius: 50%;
  border-top-color: #4facfe;
  animation: spin 1s linear infinite;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  text-align: center;
}

.error-icon {
  color: #e53e3e;
  margin-bottom: 1rem;
}

.btn-retry {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background-color: #4facfe;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-retry:hover {
  background-color: #3b9eef;
}

.profile-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
}

.profile-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  margin-bottom: 2rem;
}

.profile-header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar-container {
  display: flex;
  align-items: center;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #4facfe;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 600;
  margin-right: 1.5rem;
  background-size: cover;
  background-position: center;
}

.doctor-name-position {
  display: flex;
  flex-direction: column;
}

.doctor-name-position h2 {
  margin: 0 0 0.5rem;
  font-size: 1.8rem;
  color: #2c3e50;
}

.position-badge {
  display: inline-block;
  background-color: #ebf8ff;
  color: #3182ce;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.9rem;
  font-weight: 500;
}

.btn-edit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #edf2f7;
  color: #4a5568;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit:hover {
  background-color: #e2e8f0;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-row {
  display: flex;
  align-items: flex-start;
  padding-bottom: 1rem;
  border-bottom: 1px solid #edf2f7;
}

.detail-label {
  width: 120px;
  font-weight: 500;
  color: #4a5568;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-value {
  flex: 1;
  color: #2d3748;
}

.intro-text {
  white-space: pre-line;
  line-height: 1.6;
}

.profile-edit-form {
  margin-top: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4a5568;
}

.avatar-upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar-preview {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  background-color: #f0f2f5;
}

.avatar-upload-btn {
  padding: 0.5rem 1rem;
  background-color: #4facfe;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.avatar-upload-btn:hover {
  background-color: #3b9eef;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #4facfe;
  box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.2);
}

.radio-group {
  display: flex;
  gap: 2rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.captcha-container {
  display: flex;
  gap: 1rem;
}

.captcha-container input {
  flex: 1;
}

.captcha-image {
  width: 120px;
  height: 40px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.captcha-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.captcha-loading {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f7fafc;
}

.captcha-hint {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #718096;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background-color: #edf2f7;
  color: #4a5568;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background-color: #e2e8f0;
}

.btn-save {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

.profile-stats {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.stats-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  border-bottom: 2px solid #f0f2f5;
  padding-bottom: 0.75rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background-color: #f8fafc;
  border-radius: 8px;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 600;
  color: #4facfe;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #718096;
  font-size: 0.9rem;
}

.recent-activity {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
}

.recent-activity h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  border-bottom: 2px solid #f0f2f5;
  padding-bottom: 0.75rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #edf2f7;
}

.activity-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #ebf8ff;
  color: #4facfe;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.activity-desc {
  color: #718096;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.activity-time {
  color: #a0aec0;
  font-size: 0.8rem;
}

.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1100;
}

.toast-content {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease;
}

.toast-content.success {
  background-color: #c6f6d5;
  color: #2f855a;
}

.toast-content.error {
  background-color: #fed7d7;
  color: #c53030;
}

.toast-content svg {
  margin-right: 0.75rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .profile-header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .btn-edit {
    align-self: flex-start;
  }
  
  .detail-row {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .detail-label {
    width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .captcha-container {
    flex-direction: column;
  }
  
  .captcha-image {
    width: 100%;
  }
}
</style>
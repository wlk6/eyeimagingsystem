<template>
  <div class="review-page">
    <div class="page-header">
      
      <div class="tabs">
        <button 
          class="tab-button" 
          :class="{ active: activeTab === 'info' }" 
          @click="activeTab = 'info'"
        >
          医生信息修改审核
          <span v-if="infoReviewList.length" class="badge">{{ infoReviewList.length }}</span>
        </button>
        <button 
          class="tab-button" 
          :class="{ active: activeTab === 'password' }" 
          @click="activeTab = 'password'"
        >
          密码修改审核
          <span v-if="passwordReviewList.length" class="badge">{{ passwordReviewList.length }}</span>
        </button>
      </div>
    </div>

    <!-- 医生信息修改审核 -->
    <div v-if="activeTab === 'info'" class="review-section">
      <div class="section-header">
        <h2>待审核医生信息修改列表</h2>
        <div class="actions">
          <button class="refresh-btn" @click="fetchInfoReviewList">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1 4 1 10 7 10"></polyline>
              <polyline points="23 20 23 14 17 14"></polyline>
              <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
            </svg>
            刷新列表
          </button>
        </div>
      </div>

      <div v-if="loadingInfo" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="infoReviewList.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" width="48" height="48" stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <p>暂无待审核的医生信息修改申请</p>
      </div>

      <div v-else class="table-container">
        <table class="review-table">
          <thead>
            <tr>
              <th>审核ID</th>
              <th>医生ID</th>
              <th>医生姓名</th>
              <th>性别</th>
              <th>联系方式</th>
              <th>职称</th>
              <th>头像</th>
              <th>简介</th>
              <th>申请时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in infoReviewList" :key="item.check_info_id">
              <td>{{ item.check_info_id }}</td>
              <td>{{ item.doctor_id }}</td>
              <td>{{ item.doctor_name || '未设置' }}</td>
              <td>{{ item.gender || '未设置' }}</td>
              <td>
                <div v-if="item.phone || item.email">
                  <div v-if="item.phone">电话: {{ item.phone }}</div>
                  <div v-if="item.email">邮箱: {{ item.email }}</div>
                </div>
                <span v-else>未设置</span>
              </td>
              <td>{{ getPositionText(item.position) }}</td>
              <td>
                <div v-if="item.avatar" class="avatar-preview">
                  <img :src="getAvatarUrl(item.avatar)" alt="头像" />
                </div>
                <span v-else>未设置</span>
              </td>
              <td>{{ item.introduce || '未设置' }}</td>
              <td>{{ formatDate(item.alter_time) }}</td>
              <td class="action-buttons">
                <button class="approve-btn" @click="showReviewModal(item, 'info', 1)">
                  <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  通过
                </button>
                <button class="reject-btn" @click="showReviewModal(item, 'info', 0)">
                  <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                  拒绝
                </button>
                <button class="view-btn" @click="showDetailModal(item)">
                  <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  查看
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 密码修改审核 -->
    <div v-if="activeTab === 'password'" class="review-section">
      <div class="section-header">
        <h2>待审核密码修改列表</h2>
        <div class="actions">
          <button class="refresh-btn" @click="fetchPasswordReviewList">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1 4 1 10 7 10"></polyline>
              <polyline points="23 20 23 14 17 14"></polyline>
              <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
            </svg>
            刷新列表
          </button>
        </div>
      </div>

      <div v-if="loadingPassword" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="passwordReviewList.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" width="48" height="48" stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <p>暂无待审核的密码修改申请</p>
      </div>

      <div v-else class="table-container">
        <table class="review-table">
          <thead>
            <tr>
              <th>审核ID</th>
              <th>医生ID</th>
              <th>申请时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in passwordReviewList" :key="item.check_info_id">
              <td>{{ item.check_info_id }}</td>
              <td>{{ item.doctor_id }}</td>
              <td>{{ formatDate(item.alter_time) }}</td>
              <td class="action-buttons">
                <button class="approve-btn" @click="showReviewModal(item, 'password', 1)">
                  <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  通过
                </button>
                <button class="reject-btn" @click="showReviewModal(item, 'password', 0)">
                  <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                  拒绝
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 审核确认模态框 -->
    <div class="modal" v-if="showModal">
      <div class="modal-backdrop" @click="closeModal"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ reviewResult === 1 ? '通过审核确认' : '拒绝审核确认' }}</h3>
          <button class="close-btn" @click="closeModal">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="confirm-message">
            <svg v-if="reviewResult === 1" viewBox="0 0 24 24" width="48" height="48" stroke="#4caf50" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <svg v-else viewBox="0 0 24 24" width="48" height="48" stroke="#f44336" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <p>
              您确定要{{ reviewResult === 1 ? '通过' : '拒绝' }}
              {{ reviewType === 'info' ? '医生信息修改申请' : '密码修改申请' }}吗？
            </p>
            <div class="review-info">
              <p><strong>医生ID:</strong> {{ currentReviewItem.doctor_id }}</p>
              <p v-if="reviewType === 'info' && currentReviewItem.doctor_name"><strong>医生姓名:</strong> {{ currentReviewItem.doctor_name }}</p>
              <p><strong>申请时间:</strong> {{ formatDate(currentReviewItem.alter_time) }}</p>
            </div>
          </div>
          
          <div v-if="reviewResult === 0" class="form-group">
            <label for="rejectReason">拒绝原因 <span class="required">*</span></label>
            <textarea 
              id="rejectReason" 
              v-model="rejectReason" 
              placeholder="请输入拒绝原因，将通知给申请人"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="closeModal">取消</button>
            <button 
              type="button" 
              :class="reviewResult === 1 ? 'approve-confirm-btn' : 'reject-confirm-btn'"
              @click="submitReview"
              :disabled="isSubmitting || (reviewResult === 0 && !rejectReason)"
            >
              {{ isSubmitting ? '提交中...' : (reviewResult === 1 ? '确认通过' : '确认拒绝') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 详情查看模态框 -->
    <div class="modal" v-if="showDetail">
      <div class="modal-backdrop" @click="closeDetailModal"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>医生信息修改详情</h3>
          <button class="close-btn" @click="closeDetailModal">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="detail-row">
              <div class="detail-label">医生ID</div>
              <div class="detail-value">{{ detailItem.doctor_id }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">医生姓名</div>
              <div class="detail-value">{{ detailItem.doctor_name || '未设置' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">性别</div>
              <div class="detail-value">{{ detailItem.gender || '未设置' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">职称</div>
              <div class="detail-value">{{ getPositionText(detailItem.position) }}</div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>联系方式</h4>
            <div class="detail-row">
              <div class="detail-label">电话</div>
              <div class="detail-value">{{ detailItem.phone || '未设置' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">邮箱</div>
              <div class="detail-value">{{ detailItem.email || '未设置' }}</div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>个人资料</h4>
            <div class="detail-row">
              <div class="detail-label">头像</div>
              <div class="detail-value">
                <div v-if="detailItem.avatar" class="avatar-preview-large">
                  <img :src="getAvatarUrl(detailItem.avatar)" alt="头像" />
                </div>
                <span v-else>未设置</span>
              </div>
            </div>
            <div class="detail-row">
              <div class="detail-label">简介</div>
              <div class="detail-value">{{ detailItem.introduce || '未设置' }}</div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>申请信息</h4>
            <div class="detail-row">
              <div class="detail-label">申请时间</div>
              <div class="detail-value">{{ formatDate(detailItem.alter_time) }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">审核ID</div>
              <div class="detail-value">{{ detailItem.check_info_id }}</div>
            </div>
          </div>
          
          <div class="detail-actions">
            <button class="approve-btn" @click="showReviewModal(detailItem, 'info', 1); closeDetailModal()">
              <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              通过审核
            </button>
            <button class="reject-btn" @click="showReviewModal(detailItem, 'info', 0); closeDetailModal()">
              <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
              拒绝审核
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 提示消息 -->
    <div class="toast" v-if="toast.show" :class="toast.type">
      <div class="toast-content">
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <svg v-if="toast.type === 'error'" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        {{ toast.message }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewPage',
  data() {
    return {
      activeTab: 'info', // 'info' or 'password'
      infoReviewList: [],
      passwordReviewList: [],
      loadingInfo: false,
      loadingPassword: false,
      
      // 模态框相关
      showModal: false,
      showDetail: false,
      currentReviewItem: {},
      detailItem: {},
      reviewType: '', // 'info' or 'password'
      reviewResult: 1, // 1: 通过, 0: 拒绝
      rejectReason: '',
      isSubmitting: false,
      
      // 职称映射
      positions: [
        { value: 'chief_physician', label: '主任医师' },
        { value: 'associate_physician', label: '副主任医师' },
        { value: 'attending_doctor', label: '主治医师' }
      ],
      
      // 提示消息
      toast: {
        show: false,
        message: '',
        type: 'success' // 'success' or 'error'
      }
    };
  },
  created() {
    this.fetchInfoReviewList();
    this.fetchPasswordReviewList();
  },
  methods: {
    // 获取本地存储的token
    getToken() {
      try {
        const infoStr = localStorage.getItem('info');
        if (infoStr) {
          const info = JSON.parse(infoStr);
          return info.token;
        }
        return null;
      } catch (error) {
        console.error('获取token失败:', error);
        return null;
      }
    },
    
    // 获取医生信息修改审核列表
    async fetchInfoReviewList() {
      this.loadingInfo = true;
      const token = this.getToken();
      
      if (!token) {
        this.showToast('未登录或登录已过期，请重新登录', 'error');
        this.loadingInfo = false;
        return;
      }
      
      try {
        const response = await fetch('http://8.155.59.127:34561/user/adminGetCheckList/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': token
          }
        });
        
        const result = await response.json();
        
        if (result.code === 200) {
          this.infoReviewList = result.data || [];
          if (this.infoReviewList.length > 0) {
            this.showToast(`获取到 ${this.infoReviewList.length} 条待审核医生信息`, 'success');
          }
        } else {
          this.showToast(result.msg || '获取医生信息审核列表失败', 'error');
        }
      } catch (error) {
        console.error('获取医生信息审核列表失败:', error);
        this.showToast('网络错误，请稍后重试', 'error');
      } finally {
        this.loadingInfo = false;
      }
    },
    
    // 获取密码修改审核列表
    async fetchPasswordReviewList() {
      this.loadingPassword = true;
      const token = this.getToken();
      
      if (!token) {
        this.showToast('未登录或登录已过期，请重新登录', 'error');
        this.loadingPassword = false;
        return;
      }
      
      try {
        const response = await fetch('http://8.155.59.127:34561/Login/checkPasswordView/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': token
          }
        });
        
        const result = await response.json();
        
        if (result.code === 200) {
          this.passwordReviewList = result.data || [];
          if (this.passwordReviewList.length > 0) {
            this.showToast(`获取到 ${this.passwordReviewList.length} 条待审核密码修改`, 'success');
          }
        } else {
          this.showToast(result.msg || '获取密码修改审核列表失败', 'error');
        }
      } catch (error) {
        console.error('获取密码修改审核列表失败:', error);
        this.showToast('网络错误，请稍后重试', 'error');
      } finally {
        this.loadingPassword = false;
      }
    },
    
    // 获取头像完整URL
    getAvatarUrl(avatarPath) {
      if (!avatarPath) return '';
      // 如果已经是完整URL，则直接返回
      if (avatarPath.startsWith('http')) {
        return avatarPath;
      }
      // 否则拼接基础URL
      return `http://8.155.59.127:34561/user${avatarPath}`;
    },
    
    // 显示审核确认模态框
    showReviewModal(item, type, result) {
      this.currentReviewItem = item;
      this.reviewType = type;
      this.reviewResult = result;
      this.rejectReason = '';
      this.showModal = true;
    },
    
    // 关闭审核确认模态框
    closeModal() {
      this.showModal = false;
      this.currentReviewItem = {};
      this.rejectReason = '';
    },
    
    // 显示详情模态框
    showDetailModal(item) {
      this.detailItem = item;
      this.showDetail = true;
    },
    
    // 关闭详情模态框
    closeDetailModal() {
      this.showDetail = false;
      this.detailItem = {};
    },
    
    // 提交审核结果
    async submitReview() {
      if (this.isSubmitting) return;
      
      // 如果是拒绝操作，需要填写拒绝原因
      if (this.reviewResult === 0 && !this.rejectReason) {
        this.showToast('请填写拒绝原因', 'error');
        return;
      }
      
      this.isSubmitting = true;
      const token = this.getToken();
      
      if (!token) {
        this.showToast('未登录或登录已过期，请重新登录', 'error');
        this.isSubmitting = false;
        return;
      }
      
      try {
        let url, requestData;
        
        if (this.reviewType === 'info') {
          url = 'http://8.155.59.127:34561/user/adminGiveCheckAdvice/';
          requestData = {
            doctor_id: this.currentReviewItem.doctor_id,
            result: this.reviewResult
          };
          
          // 如果是拒绝，添加拒绝原因
          if (this.reviewResult === 0) {
            requestData.reason = this.rejectReason;
          }
        } else {
          url = 'http://8.155.59.127:34561/Login/adminGivePasswordCheckAdvice/';
          requestData = {
            doctor_id: this.currentReviewItem.doctor_id,
            result: this.reviewResult
          };
          
          // 如果是拒绝，添加拒绝原因
          if (this.reviewResult === 0) {
            requestData.reason = this.rejectReason;
          }
        }
        
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': token
          },
          body: JSON.stringify(requestData)
        });
        
        const result = await response.json();
        
        if (result.code === 200) {
          this.showToast(
            this.reviewResult === 1 
              ? '审核已通过' 
              : '审核已拒绝',
            'success'
          );
          
          // 刷新列表
          if (this.reviewType === 'info') {
            this.fetchInfoReviewList();
          } else {
            this.fetchPasswordReviewList();
          }
          
          // 关闭模态框
          this.closeModal();
        } else {
          this.showToast(result.msg || '提交审核结果失败', 'error');
        }
      } catch (error) {
        console.error('提交审核结果失败:', error);
        this.showToast('网络错误，请稍后重试', 'error');
      } finally {
        this.isSubmitting = false;
      }
    },
    
    // 获取职称文本
    getPositionText(position) {
      if (!position) return '未设置';
      const positionObj = this.positions.find(p => p.value === position);
      return positionObj ? positionObj.label : position;
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '';
      
      // 处理日期格式
      const date = new Date(dateString.replace(/-/g, '/'));
      
      // 检查日期是否有效
      if (isNaN(date.getTime())) {
        return dateString;
      }
      
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },
    
    // 显示提示消息
  showToast(message, type = 'success') {
    this.toast = {
      show: true,
      message,
      type
    };
    setTimeout(() => {
      this.toast.show = false;
    }, 3000);
  }
}
}
</script>

<style scoped>
.review-page {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
  position: relative;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 20px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: 16px;
  color: #606266;
  cursor: pointer;
  position: relative;
  transition: all 0.3s;
}

.tab-button.active {
  color: #4299e1;
  border-bottom-color: #4299e1;
  font-weight: 500;
}

.tab-button:hover {
  color: #4299e1;
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: #f56c6c;
  color: white;
  font-size: 12px;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
  transform: translate(50%, -50%);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h2 {
  font-size: 18px;
  font-weight: 500;
  color: #2c3e50;
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  color: #606266;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover {
  color: #4299e1;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.review-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 20px;
}

.table-container {
  overflow-x: auto;
}

.review-table {
  width: 100%;
  border-collapse: collapse;
}

.review-table th,
.review-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.review-table th {
  font-weight: 500;
  color: #606266;
  background-color: #f5f7fa;
}

.review-table tbody tr:hover {
  background-color: #f5f7fa;
}

.avatar-preview {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-preview-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-preview-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.approve-btn,
.reject-btn,
.view-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  border: none;
  transition: all 0.3s;
}

.approve-btn {
  background-color: #f0f9eb;
  color: #67c23a;
}

.approve-btn:hover {
  background-color: #e1f3d8;
}

.reject-btn {
  background-color: #fef0f0;
  color: #f56c6c;
}

.reject-btn:hover {
  background-color: #fde2e2;
}

.view-btn {
  background-color: #ecf5ff;
  color: #409eff;
}

.view-btn:hover {
  background-color: #d9ecff;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  margin-top: 10px;
  color: #909399;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #909399;
}

.empty-state svg {
  margin-bottom: 16px;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1001;
}

.modal-content {
  position: relative;
  background-color: white;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  z-index: 1002;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #909399;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #606266;
}

.modal-body {
  padding: 20px;
}

.confirm-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 20px;
}

.confirm-message svg {
  margin-bottom: 16px;
}

.confirm-message p {
  margin: 0 0 16px;
  font-size: 16px;
  color: #303133;
}

.review-info {
  width: 100%;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 12px;
  margin-top: 16px;
  text-align: left;
}

.review-info p {
  margin: 8px 0;
  font-size: 14px;
  color: #606266;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
}

.required {
  color: #f56c6c;
}

.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
  resize: vertical;
}

.form-group textarea:focus {
  outline: none;
  border-color: #409eff;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-btn {
  padding: 8px 16px;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  color: #606266;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.approve-confirm-btn {
  padding: 8px 16px;
  background-color: #67c23a;
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.approve-confirm-btn:hover {
  background-color: #85ce61;
}

.reject-confirm-btn {
  padding: 8px 16px;
  background-color: #f56c6c;
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.reject-confirm-btn:hover {
  background-color: #f78989;
}

.approve-confirm-btn:disabled,
.reject-confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 详情模态框样式 */
.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.detail-row {
  display: flex;
  margin-bottom: 8px;
}

.detail-label {
  width: 80px;
  font-size: 14px;
  color: #909399;
}

.detail-value {
  flex: 1;
  font-size: 14px;
  color: #606266;
}

.detail-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

/* 提示消息 */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 2000;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  font-size: 14px;
  animation: slideIn 0.3s ease;
}

.toast-content.success {
  background-color: #f0f9eb;
  color: #67c23a;
}

.toast-content.error {
  background-color: #fef0f0;
  color: #f56c6c;
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

/* 响应式样式 */
@media (max-width: 768px) {
  .review-table th:nth-child(3),
  .review-table td:nth-child(3),
  .review-table th:nth-child(5),
  .review-table td:nth-child(5) {
    display: none;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
  
  .modal-content {
    width: 95%;
  }
}

@media (max-width: 576px) {
  .review-table th:nth-child(4),
  .review-table td:nth-child(4),
  .review-table th:nth-child(6),
  .review-table td:nth-child(6) {
    display: none;
  }
  
  .tabs {
    flex-direction: column;
    gap: 8px;
    border-bottom: none;
  }
  
  .tab-button {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
  }
  
  .tab-button.active {
    border-color: #4299e1;
  }
}
</style>
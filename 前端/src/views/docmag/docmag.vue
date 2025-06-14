<template>
  <div class="section">
    <div class="section-header">
      <h2>医生账号管理</h2>
      <button class="primary-btn" @click="showAddDoctorModal = true">
        <svg class="btn-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        添加医生
      </button>
    </div>
    
    <div class="filter-bar">
      <div class="search-filter">
        <input type="text" v-model="doctorSearchQuery" placeholder="搜索医生姓名/ID" @input="filterDoctors" />
        <svg class="filter-search-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>
    </div>
    
    <div class="table-wrapper">
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>性别</th>
              <th>电话</th>
              <th>邮箱</th>
              <th>职称</th>
              <th>个人介绍</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doctor in paginatedDoctors" :key="doctor.doctor_id">
              <td>{{ doctor.doctor_id }}</td>
              <td class="doctor-name">
                <img 
                  :src="doctor.avatar ? formatAvatarUrl(doctor.avatar) : '/placeholder.svg?height=30&width=30'" 
                  alt="医生头像" 
                  class="doctor-avatar" 
                />
                <span>{{ doctor.doctor_name }}</span>
              </td>
              <td>{{ doctor.gender || '未设置' }}</td>
              <td>{{ doctor.phone || '未设置' }}</td>
              <td>{{ doctor.email || '未设置' }}</td>
              <td>{{ getPositionText(doctor.position) }}</td>
              <td>{{ doctor.introduce || '未设置' }}</td>
              <td class="action-buttons">
                <button class="action-btn delete" @click="confirmDeleteDoctor(doctor)">
                  <svg class="action-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- 无数据状态 -->
      <div v-if="!loading && filteredDoctors.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" width="48" height="48" stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
        <p>暂无医生数据</p>
      </div>
    </div>
    
    <div class="pagination" v-if="totalPages > 1">
      <button class="pagination-btn" :disabled="currentPage === 1" @click="currentPage--">
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      
      <div class="page-info">
        <span>{{ currentPage }} / {{ totalPages }}</span>
      </div>
      
      <button class="pagination-btn" :disabled="currentPage === totalPages" @click="currentPage++">
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>

    <!-- 添加医生模态框 -->
    <div class="modal" v-if="showAddDoctorModal">
      <div class="modal-backdrop" @click="showAddDoctorModal = false"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>添加医生</h3>
          <button class="close-btn" @click="showAddDoctorModal = false">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>姓名 <span class="required">*</span></label>
            <input type="text" v-model="newDoctor.doctor_name" placeholder="请输入医生姓名" />
          </div>
          <div class="form-group">
            <label>密码 <span class="required">*</span></label>
            <input type="password" v-model="newDoctor.password" placeholder="请输入密码" />
          </div>
          <div class="form-group">
            <label>确认密码 <span class="required">*</span></label>
            <input type="password" v-model="newDoctor.password_confirm" placeholder="请再次输入密码" />
          </div>
          <div class="form-group">
            <label>性别</label>
            <select v-model="newDoctor.gender">
              <option value="">请选择性别</option>
              <option value="男">男</option>
              <option value="女">女</option>
            </select>
          </div>
          <div class="form-group">
            <label>职称 <span class="required">*</span></label>
            <select v-model="newDoctor.position">
              <option value="">请选择职称</option>
              <option v-for="(position, index) in positions" :key="index" :value="position.value">
                {{ position.label }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="secondary-btn" @click="showAddDoctorModal = false">取消</button>
          <button class="primary-btn" @click="addDoctor" :disabled="addingDoctor">
            {{ addingDoctor ? '添加中...' : '确认添加' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 删除确认模态框 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-backdrop" @click="showDeleteModal = false"></div>
      <div class="modal-content delete-confirm">
        <div class="modal-header">
          <h3>确认删除</h3>
          <button class="close-btn" @click="showDeleteModal = false">
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="delete-warning">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="1">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <p>您确定要删除医生 <strong>{{ doctorToDelete ? doctorToDelete.doctor_name : '' }}</strong> 吗？</p>
            <p class="warning-text">此操作不可逆，删除后将无法恢复医生数据。</p>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="showDeleteModal = false">取消</button>
            <button type="button" class="btn-delete-confirm" @click="deleteDoctor" :disabled="deletingDoctor">
              {{ deletingDoctor ? '删除中...' : '确认删除' }}
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
  name: 'DoctorsPage',
  data() {
    return {
      doctors: [],
      filteredDoctors: [],
      doctorSearchQuery: '',
      currentPage: 1,
      itemsPerPage: 10,
      showAddDoctorModal: false,
      showDeleteModal: false,
      loading: true,
      addingDoctor: false,
      deletingDoctor: false,
      baseAvatarUrl: 'http://8.155.59.127:34561/user',
      positions: [
        { value: 'chief_physician', label: '主任医师' },
        { value: 'associate_physician', label: '副主任医师' },
        { value: 'attending_doctor', label: '主治医师' }
      ],
      newDoctor: {
        doctor_name: '',
        password: '',
        password_confirm: '',
        gender: '',
        position: ''
      },
      doctorToDelete: null,
      toast: {
        show: false,
        message: '',
        type: 'success'
      }
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredDoctors.length / this.itemsPerPage);
    },
    paginatedDoctors() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredDoctors.slice(start, end);
    }
  },
  created() {
    this.fetchDoctors();
  },
  mounted() {
    document.body.style.overflow = 'hidden';
  },
  beforeDestroy() {
    document.body.style.overflow = 'auto';
  },
  methods: {
    // 格式化头像URL
    formatAvatarUrl(avatarPath) {
      if (!avatarPath) return '';
      
      // 如果已经是完整的URL，则直接返回
      if (avatarPath.startsWith('http')) {
        return avatarPath;
      }
      
      // 确保头像路径格式正确
      const path = avatarPath.startsWith('/') ? avatarPath : `/${avatarPath}`;
      return `${this.baseAvatarUrl}${path}`;
    },
    
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
    
    async fetchDoctors() {
      this.loading = true;
      const token = this.getToken();
      
      if (!token) {
        this.showToast('未登录或登录已过期，请重新登录', 'error');
        this.loading = false;
        return;
      }
      
      try {
        const response = await fetch('http://8.155.59.127:34561/user/getDoctorListView/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': `${token}`
          },
        });
        
        const result = await response.json();
        
        if (result.code === 200) {
          this.doctors = result.data;
          this.filteredDoctors = [...this.doctors];
        } else {
          this.showToast(result.msg || '获取医生列表失败', 'error');
        }
      } catch (error) {
        console.error('获取医生列表失败:', error);
        this.showToast('网络错误，请稍后重试', 'error');
      } finally {
        this.loading = false;
      }
    },
    
    filterDoctors() {
      if (!this.doctorSearchQuery) {
        this.filteredDoctors = [...this.doctors];
      } else {
        const query = this.doctorSearchQuery.toLowerCase();
        this.filteredDoctors = this.doctors.filter(doctor => 
          doctor.doctor_name.toLowerCase().includes(query) || 
          doctor.doctor_id.toString().includes(query) ||
          (doctor.phone && doctor.phone.includes(query))
        );
      }
      
      // 重置到第一页
      this.currentPage = 1;
    },
    
    getPositionText(position) {
      const positionObj = this.positions.find(p => p.value === position);
      return positionObj ? positionObj.label : position;
    },
    
    viewDoctor(doctor) {
      // 查看医生详情的逻辑
      console.log('查看医生:', doctor);
    },
    
    confirmDeleteDoctor(doctor) {
      this.doctorToDelete = doctor;
      this.showDeleteModal = true;
    },
    
    async deleteDoctor() {
      if (!this.doctorToDelete || this.deletingDoctor) return;
      
      this.deletingDoctor = true;
      const token = this.getToken();
      
      if (!token) {
        this.showToast('未登录或登录已过期，请重新登录', 'error');
        this.deletingDoctor = false;
        this.showDeleteModal = false;
        return;
      }
      
      try {
        const response = await fetch('http://8.155.59.127:34561/user/adminDelDoctorAccount/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': `${token}`
          },
          body: JSON.stringify({
            doctor_id: this.doctorToDelete.doctor_id.toString()
          })
        });
        
        const result = await response.json();
        
        if (result.code === 200) {
          this.showToast('删除医生成功');
          // 重新获取医生列表
          this.fetchDoctors();
        } else {
          this.showToast(result.msg || '删除医生失败', 'error');
        }
      } catch (error) {
        console.error('删除医生失败:', error);
        this.showToast('网络错误，请稍后重试', 'error');
      } finally {
        this.deletingDoctor = false;
        this.showDeleteModal = false;
        this.doctorToDelete = null;
      }
    },
    
    async addDoctor() {
      if (this.addingDoctor) return;
      
      // 表单验证
      if (!this.newDoctor.doctor_name) {
        this.showToast('请输入医生姓名', 'error');
        return;
      }
      
      if (!this.newDoctor.password) {
        this.showToast('请输入密码', 'error');
        return;
      }
      
      if (this.newDoctor.password !== this.newDoctor.password_confirm) {
        this.showToast('两次输入的密码不一致', 'error');
        return;
      }
      
      if (!this.newDoctor.position) {
        this.showToast('请选择职称', 'error');
        return;
      }
      
      this.addingDoctor = true;
      const token = this.getToken();
      
      if (!token) {
        this.showToast('未登录或登录已过期，请重新登录', 'error');
        this.addingDoctor = false;
        return;
      }
      
      try {
        const requestData = {
          ...this.newDoctor,
          token
        };
        
        const response = await fetch('http://8.155.59.127:34561/user/adminAddDoctorAccount/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': `${token}`
          },
          body: JSON.stringify(requestData)
        });
        
        const result = await response.json();
        
        if (result.code === 200) {
          this.showToast('添加医生成功');
          this.showAddDoctorModal = false;
          
          // 重置表单
          this.newDoctor = {
            doctor_name: '',
            password: '',
            password_confirm: '',
            gender: '',
            position: ''
          };
          
          // 重新获取医生列表
          this.fetchDoctors();
        } else {
          this.showToast(result.msg || '添加医生失败', 'error');
        }
      } catch (error) {
        console.error('添加医生失败:', error);
        this.showToast('网络错误，请稍后重试', 'error');
      } finally {
        this.addingDoctor = false;
      }
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
    }
  }
}
</script>

<style scoped>
.section {
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 20px;
  position: relative;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.primary-btn {
  background-color: #4299e1;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.3s;
}

.primary-btn:hover {
  background-color: #3182ce;
}

.primary-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.secondary-btn {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.secondary-btn:hover {
  background-color: #e5e5e5;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* 医生账号管理样式 */
.filter-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.search-filter {
  position: relative;
  width: 250px;
}

.filter-search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #999;
}

.search-filter input {
  width: 100%;
  padding: 8px 10px 8px 35px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}

/* 表格容器样式 */
.table-wrapper {
  position: relative;
  min-height: 300px;
}

.table-container {
  overflow-y: auto;
  width: 100%;
  border: 1px solid #eee;
  border-radius: 4px;
  height: 400px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px; /* 确保表格有最小宽度，触发滚动 */
}

.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f9f9f9;
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 10;
}

.data-table tbody tr:hover {
  background-color: #f5f7fa;
}

.doctor-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.doctor-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.action-buttons {
  display: flex;
  gap: 5px;
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-btn.view {
  background-color: #e8f5e9;
  color: #4caf50;
}

.action-btn.view:hover {
  background-color: #c8e6c9;
}

.action-btn.delete {
  background-color: #ffebee;
  color: #f44336;
}

.action-btn.delete:hover {
  background-color: #ffcdd2;
}

.action-icon {
  width: 16px;
  height: 16px;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 15px;
}

.pagination-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e0e0;
  background-color: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #606266;
}

/* 加载状态 */
.loading-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
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

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #a0aec0;
}

.empty-state svg {
  margin-bottom: 10px;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
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
  border-radius: 5px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  z-index: 1002;
}

.delete-confirm {
  width: 400px;
}

.modal-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #eee;
}

.form-group {
  display: grid;
  gap: 8px;
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  font-size: 14px;
}

.required {
  color: #f44336;
}

.form-group input, .form-group select {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.form-group input:focus, .form-group select:focus {
  border-color: #4299e1;
}

/* 删除确认样式 */
.delete-warning {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.delete-warning svg {
  color: #f56c6c;
  margin-bottom: 16px;
}

.delete-warning p {
  text-align: center;
  margin: 8px 0;
  font-size: 14px;
  color: #606266;
}

.warning-text {
  color: #f56c6c;
  font-size: 12px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
}

.btn-cancel {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  background: white;
  color: #4a5568;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f7fafc;
}

.btn-delete-confirm {
  background-color: #f56c6c;
  border: none;
  border-radius: 4px;
  padding: 8px 20px;
  font-size: 14px;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-delete-confirm:hover:not(:disabled) {
  background-color: #f78989;
}

.btn-delete-confirm:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 提示消息 */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 2000;
  min-width: 250px;
  border-radius: 4px;
  padding: 12px 16px;
  animation: fadeIn 0.3s, fadeOut 0.3s 2.7s;
}

.toast.success {
  background-color: #4caf50;
  color: white;
}

.toast.error {
  background-color: #f44336;
  color: white;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(20px); }
}

/* 响应式样式 */
@media (max-width: 768px) {
  .filter-bar {
    flex-direction: column;
    gap: 10px;
  }

  .search-filter {
    width: 100%;
  }

  .modal-content {
    width: 95%;
  }
}
</style>
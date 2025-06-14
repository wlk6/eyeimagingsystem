<template>
  <div class="patient-management" style="margin-top: -40px;">
    <!-- 页面标题和操作区 -->
    <div class="page-header">
      <div class="header-left">
      </div>
      <div class="header-actions">
        <div class="search-box">
          <input 
            type="text" 
            placeholder="搜索患者姓名、电话..." 
            v-model="searchQuery"
            @input="handleSearch"
          />
          <svg class="search-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <button class="btn-add" @click="openPatientModal()">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          添加患者
        </button>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-group">
        <div class="filter-item">
          <label>性别</label>
          <select v-model="filters.gender" @change="applyFilters">
            <option value="">全部</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        <div class="filter-item">
          <label>患者ID</label>
          <input 
            type="text" 
            v-model="filters.patientId" 
            placeholder="输入患者ID" 
            @input="applyFilters"
          />
        </div>
        <div class="filter-item">
          <label>手机号</label>
          <input 
            type="text" 
            v-model="filters.phone" 
            placeholder="输入手机号" 
            @input="applyFilters"
          />
        </div>
      </div>
      <button class="btn-reset" @click="resetFilters">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12h18M3 6h18M3 18h18"></path>
        </svg>
        重置筛选
      </button>
    </div>

    <!-- 患者列表 -->
    <div class="patient-list-container">
      <div class="patient-list-header">
        <div class="list-header-item" @click="sortBy('patientName')">
          患者姓名
          <svg v-if="sortKey === 'patientName'" class="sort-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline :points="sortOrder === 'asc' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"></polyline>
          </svg>
        </div>
        <div class="list-header-item" @click="sortBy('gender')">
          性别
          <svg v-if="sortKey === 'gender'" class="sort-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline :points="sortOrder === 'asc' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"></polyline>
          </svg>
        </div>
        <div class="list-header-item" @click="sortBy('id')">
          患者ID
          <svg v-if="sortKey === 'id'" class="sort-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline :points="sortOrder === 'asc' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"></polyline>
          </svg>
        </div>
        <div class="list-header-item" @click="sortBy('phone')">
          联系电话
          <svg v-if="sortKey === 'phone'" class="sort-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline :points="sortOrder === 'asc' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"></polyline>
          </svg>
        </div>
        <div class="list-header-item" @click="sortBy('record')">
          病情记录
          <svg v-if="sortKey === 'record'" class="sort-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline :points="sortOrder === 'asc' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"></polyline>
          </svg>
        </div>
        <div class="list-header-item">操作</div>
      </div>

      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="filteredPatients.length === 0" class="no-data">
        <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" stroke-width="1">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <p>没有找到符合条件的患者记录</p>
      </div>

      <div v-else class="patient-list">
        <div 
          v-for="patient in paginatedPatients" 
          :key="patient.id" 
          class="patient-item"
          :class="{ 'selected': selectedPatient && selectedPatient.id === patient.id }"
          @click="selectPatient(patient)"
        >
          <div class="patient-info patient-name">
           <div class="patient-avatar">
  <svg class="avatar" viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
    <circle cx="12" cy="7" r="4"></circle>
  </svg>
</div>
            <span>{{ patient.patientName }}</span>
          </div>
          <div class="patient-info">{{ patient.gender }}</div>
          <div class="patient-info">{{ patient.id }}</div>
          <div class="patient-info">{{ formatPhone(patient.phone) }}</div>
          <div class="patient-info record-info">
            <div class="record-text">{{ patient.record || '暂无记录' }}</div>
          </div>
          <div class="patient-actions">
            <button class="btn-view" @click.stop="viewPatientDetails(patient)" title="查看详情">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </button>
            <button class="btn-edit" @click.stop="openPatientModal(patient)" title="编辑">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button class="btn-delete" @click.stop="confirmDeletePatient(patient)" title="删除">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
      <!-- 分页控件 -->
     <div class="pagination">
        <button 
          :disabled="currentPage === 1" 
          @click="currentPage--"
          class="pagination-btn"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
          上一页
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages || 1 }}</span>
        <button 
          :disabled="currentPage === totalPages || totalPages === 0" 
          @click="currentPage++"
          class="pagination-btn"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
          下一页
        </button>
      </div>
    <!-- 患者详情侧边栏 -->
    <div class="patient-details" v-if="selectedPatient" :class="{ 'active': selectedPatient }">
      <div class="details-header">
        <h3>患者详情</h3>
        <button class="btn-close" @click="selectedPatient = null">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="patient-profile">
        <div class="profile-avatar">
          <img :src="getPatientAvatar(selectedPatient)" alt="患者头像" />
        </div>
        <div class="profile-info">
          <h4>{{ selectedPatient.patientName }}</h4>
          <p>{{ selectedPatient.gender }}</p>
        </div>
      </div>

      <div class="details-content">
        <div class="detail-section">
          <h5>基本信息</h5>
          <div class="detail-item">
            <span class="detail-label">出生日期</span>
            <span class="detail-value">{{ formatDate(selectedPatient.birthday) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">联系电话</span>
            <span class="detail-value">{{ formatPhone(selectedPatient.phone) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">患者ID</span>
            <span class="detail-value">{{ selectedPatient.id }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">病情记录</span>
            <span class="detail-value">{{ selectedPatient.record || '暂无记录' }}</span>
          </div>
        </div>

        <div class="detail-section">
          <div class="section-header">
            <h5>病历记录</h5>
            <button class="btn-add-small" @click="openRecordModal">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              添加记录
            </button>
          </div>
          <div v-if="selectedPatient.records && selectedPatient.records.length" class="medical-records">
            <div v-for="(record, index) in selectedPatient.records" :key="index" class="record-item">
              <div class="record-date">{{ formatDate(record.date) }}</div>
              <div class="record-content">
                <p>{{ record.description }}</p>
                <div class="record-doctor">记录医生: {{ getDoctorName(record.doctor_id) }}</div>
              </div>
            </div>
          </div>
          <div v-else class="no-records">
            <p>暂无病历记录</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑患者弹窗 -->
    <div class="modal" v-if="showPatientModal">
      <div class="modal-backdrop" @click="showPatientModal = false"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑患者信息' : '添加新患者' }}</h3>
          <button class="btn-close" @click="showPatientModal = false">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="savePatient">
            <div class="form-group">
              <label for="patientName">患者姓名 <span class="required">*</span></label>
              <input 
                type="text" 
                id="patientName" 
                v-model="patientForm.patientName" 
                required
                placeholder="请输入患者姓名"
              />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="gender">性别 <span class="required">*</span></label>
                <select id="gender" v-model="patientForm.gender" required>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
              </div>
              <div class="form-group">
                <label for="birthday">出生日期 <span class="required">*</span></label>
                <input 
                  type="date" 
                  id="birthday" 
                  v-model="patientForm.birthday" 
                  required
                />
              </div>
            </div>
            <div class="form-group">
              <label for="phone">联系电话 <span class="required">*</span></label>
              <input 
                type="tel" 
                id="phone" 
                v-model="patientForm.phone" 
                required
                placeholder="请输入联系电话"
                pattern="[0-9]{11}"
                title="请输入11位手机号码"
              />
            </div>
            <div class="form-group">
              <label for="record">病情描述</label>
              <textarea 
                id="record" 
                v-model="patientForm.record" 
                placeholder="请输入患者病情描述（可选）"
                rows="4"
              ></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-cancel" @click="showPatientModal = false">取消</button>
              <button type="submit" class="btn-save" :disabled="isSubmitting">
                {{ isSubmitting ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 添加病历记录弹窗 -->
    <div class="modal" v-if="showRecordModal">
      <div class="modal-backdrop" @click="showRecordModal = false"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>添加病历记录</h3>
          <button class="btn-close" @click="showRecordModal = false">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveRecord">
            <div class="form-group">
              <label for="recordDate">记录日期 <span class="required">*</span></label>
              <input 
                type="date" 
                id="recordDate" 
                v-model="recordForm.date" 
                required
              />
            </div>
            <div class="form-group">
              <label for="recordDescription">病情描述 <span class="required">*</span></label>
              <textarea 
                id="recordDescription" 
                v-model="recordForm.description" 
                placeholder="请输入详细的病情描述"
                rows="6"
                required
              ></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-cancel" @click="showRecordModal = false">取消</button>
              <button type="submit" class="btn-save" :disabled="isSubmitting">
                {{ isSubmitting ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 确认删除弹窗 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-backdrop" @click="showDeleteModal = false"></div>
      <div class="modal-content delete-confirm">
        <div class="modal-header">
          <h3>确认删除</h3>
          <button class="btn-close" @click="showDeleteModal = false">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
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
            <p>您确定要删除患者 <strong>{{ patientToDelete ? patientToDelete.patientName : '' }}</strong> 的记录吗？</p>
            <p class="warning-text">此操作不可逆，删除后将无法恢复患者数据。</p>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="showDeleteModal = false">取消</button>
            <button type="button" class="btn-delete-confirm" @click="deletePatient" :disabled="isSubmitting">
              {{ isSubmitting ? '删除中...' : '确认删除' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 消息提示 -->
    <div class="toast" v-if="toast.show">
      <div class="toast-content" :class="toast.type">
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <svg v-else-if="toast.type === 'error'" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </div>

    <!-- 全局加载指示器 -->
    <div class="loading-overlay" v-if="isLoading">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script>
import { getInfo } from '@/utils/storage'; 
const getToken = () => {
  const info = getInfo();
  return info.token || '';
};

export default {
  name: 'PatientManagement',
  data() {
    return {
      // API相关
      apiBaseUrl: 'http://8.155.59.127:34561',
      token: localStorage.getItem('token') || '',
      isLoading: false,
      isSubmitting: false,
      
      // 当前医生信息
      currentDoctor: {
        id: '202301',
        name: '张医生',
        department: '眼科',
        avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
      },
      
      // 医生列表
      doctors: [
        { id: '202301', name: '张医生', department: '眼科', avatar: 'https://randomuser.me/api/portraits/men/32.jpg' },
        { id: '202302', name: '王医生', department: '内科', avatar: 'https://randomuser.me/api/portraits/men/44.jpg' },
        { id: '202303', name: '李医生', department: '外科', avatar: 'https://randomuser.me/api/portraits/women/68.jpg' },
        { id: '202304', name: '赵医生', department: '儿科', avatar: 'https://randomuser.me/api/portraits/women/65.jpg' }
      ],
      
      // 患者列表
      patients: [],
      
      // 搜索结果和筛选
      searchQuery: '',
      filters: {
        gender: '',
        patientId: '',
        phone: ''
      },
      
      // 排序
      sortKey: '',
      sortOrder: 'asc',
      
      // 分页
      currentPage: 1,
      pageSize: 5,
      
      // 选中的患者
      selectedPatient: null,
      
      // 模态框状态
      showPatientModal: false,
      showRecordModal: false,
      showDeleteModal: false,
      
      // 表单数据
      patientForm: {
        patientName: '',
        phone: '',
        gender: '男',
        birthday: '',
        record: ''
      },
      
      recordForm: {
        date: new Date().toISOString().split('T')[0],
        description: '',
        doctor_id: ''
      },
      
      // 要删除的患者
      patientToDelete: null,
      
      // 是否编辑模式
      isEditing: false,
      
      // 消息提示
      toast: {
        show: false,
        message: '',
        type: 'success'
      }
    };
  },
  
  computed: {
    // 过滤后的患者列表
    filteredPatients() {
      let result = [...this.patients];
      
      // 搜索
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(patient => 
          patient.patientName.toLowerCase().includes(query) || 
          patient.phone.includes(query)
        );
      }
      
      // 性别过滤
      if (this.filters.gender) {
        result = result.filter(patient => patient.gender === this.filters.gender);
      }
      
      // 患者ID过滤
      if (this.filters.patientId) {
        result = result.filter(patient => 
          patient.id.toString().includes(this.filters.patientId)
        );
      }
      
      // 手机号过滤
      if (this.filters.phone) {
        result = result.filter(patient => 
          patient.phone.includes(this.filters.phone)
        );
      }
      
      // 排序
      if (this.sortKey) {
        result.sort((a, b) => {
          let valueA = a[this.sortKey];
          let valueB = b[this.sortKey];
          
          if (valueA < valueB) return this.sortOrder === 'asc' ? -1 : 1;
          if (valueA > valueB) return this.sortOrder === 'asc' ? 1 : -1;
          return 0;
        });
      }
      
      return result;
    },
    
    // 分页后的患者列表
    paginatedPatients() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredPatients.slice(start, end);
    },
    
    // 总页数
    totalPages() {
      return Math.ceil(this.filteredPatients.length / this.pageSize);
    },
    
    // 请求头
    headers() {
      return {
        'Content-Type': 'application/json',
        'token': `${getToken()}`
      };
    }
  },
  
  created() {
    // 页面加载时获取患者列表
    this.fetchPatients();
  },
  
  methods: {
    // API请求方法
    async fetchPatients() {
      try {
        this.isLoading = true;
        const response = await fetch(`${this.apiBaseUrl}/user/detail/`, {
          method: 'GET',
          headers: this.headers
        });
        
        if (!response.ok) {
          throw new Error('获取患者列表失败');
        }
        
        const data = await response.json();
        this.patients = data.map(patient => {
          // 转换API返回的数据格式为组件使用的格式
          return {
            id: patient.patient_id.toString(),
            patientName: patient.patientName,
            phone: patient.phone,
            gender: patient.gender,
            birthday: patient.birthday,
            record: patient.record || '',
            lastVisit: patient.lastVisit || '',
            records: patient.records || [],
            visits: patient.visits || []
          };
        });
      } catch (error) {
        console.error('获取患者列表错误:', error);
        this.showToast('获取患者列表失败', 'error');
      } finally {
        this.isLoading = false;
      }
    },
    
    // 计算年龄
    calculateAge(birthday) {
      if (!birthday) return 0;
      const birthDate = new Date(birthday);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      
      return age;
    },
    
    // 格式化电话号码
    formatPhone(phone) {
      if (!phone) return '';
      return phone.replace(/(\d{3})(\d{4})(\d{4})/, '$1 $2 $3');
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
    },
    
    // 获取医生姓名
    getDoctorName(doctorId) {
      const doctor = this.doctors.find(doc => doc.id === doctorId);
      return doctor ? doctor.name : '未分配';
    },
    
    // 获取患者头像
    getPatientAvatar(patient) {
      // 根据患者ID生成固定的头像
      const id = parseInt(patient.id.slice(-2));
      const gender = patient.gender === '男' ? 'men' : 'women';
      return `https://randomuser.me/api/portraits/${gender}/${id % 100}.jpg`;
    },
        handleSearch() {
      this.currentPage = 1;
    },
    
    // 排序处理
    sortBy(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
    },
    
    // 应用筛选
    applyFilters() {
      this.currentPage = 1;
    },
    
    // 重置筛选
    resetFilters() {
      this.filters = {
        gender: '',
        patientId: '',
        phone: ''
      };
      this.searchQuery = '';
      this.currentPage = 1;
    },
    
    // 选择患者
    selectPatient(patient) {
      this.selectedPatient = patient;
    },
    
    // 查看患者详情
    viewPatientDetails(patient) {
      this.selectedPatient = patient;
    },
    
    // 打开患者表单模态框
    openPatientModal(patient = null) {
      this.isEditing = !!patient;
      
      if (patient) {
        // 编辑模式，填充表单
        this.patientForm = { 
          ...patient,
          patient_id: parseInt(patient.id) // 确保API需要的字段名正确
        };
      } else {
        // 添加模式，重置表单
        this.patientForm = {
          patientName: '',
          phone: '',
          gender: '男',
          birthday: '',
          record: ''
        };
      }
      
      this.showPatientModal = true;
    },
    
    // 打开病历记录表单模态框
    openRecordModal() {
      if (!this.selectedPatient) return;
      
      this.recordForm = {
        date: new Date().toISOString().split('T')[0],
        description: '',
        doctor_id: this.currentDoctor.id
      };
      
      this.showRecordModal = true;
    },
    
    // 确认删除患者
    confirmDeletePatient(patient) {
      this.patientToDelete = patient;
      this.showDeleteModal = true;
    },
    
    // 保存患者信息
    async savePatient() {
      try {
        this.isSubmitting = true;
        
        // 准备API请求数据
        const patientData = {
          doctor_id: this.currentDoctor.id,
          patientName: this.patientForm.patientName,
          gender: this.patientForm.gender,
          birthday: this.patientForm.birthday,
          phone: this.patientForm.phone,
          record: this.patientForm.record || ''
        };
        
        let response;
        if (this.isEditing) {
          // 更新现有患者 - PATCH请求
          patientData.patient_id = parseInt(this.patientForm.id);
          response = await fetch(`${this.apiBaseUrl}/user/selectAndUpdate/`, {
            method: 'PATCH',
            headers: this.headers,
            body: JSON.stringify(patientData)
          });
        } else {
          // 添加新患者 - POST请求
          response = await fetch(`${this.apiBaseUrl}/user/detail/`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(patientData)
          });
        }
        
        if (!response.ok) {
          throw new Error(this.isEditing ? '更新患者失败' : '添加患者失败');
        }

        // 关闭模态框
        this.showPatientModal = false;
        
        // 延迟100ms确保模态框关闭动画完成（可选，根据UI过渡时间调整）
        setTimeout(() => {
          // 刷新整个页面（重点：使用完整的页面刷新）
          window.location.href = window.location.href; // 等价于刷新当前页面
        }, 100);

        this.showToast(this.isEditing ? '患者信息更新成功' : '新患者添加成功', 'success');
        window.location.reload();
      } catch (error) {
        console.error('保存失败:', error);
        this.showToast(error.message || '保存操作失败', 'error');
      } finally {
        this.isSubmitting = false;
      }
    },
    
    // 保存病历记录
    async saveRecord() {
      if (!this.selectedPatient) return;
      
      try {
        this.isSubmitting = true;
        
        const newRecord = { ...this.recordForm };
        
        // 确保患者有records数组
        if (!this.selectedPatient.records) {
          this.selectedPatient.records = [];
        }
        
        // 添加新记录
        this.selectedPatient.records.push(newRecord);
        let tt
        if(this.selectedPatient.records[0].description===''){
          tt=this.selectedPatient.record
        }
        else{
          tt=this.selectedPatient.records[0].description 
        }
        // 更新患者信息到API
        const patientData = {
          patient_id: parseInt(this.selectedPatient.id),
          patientName: this.selectedPatient.patientName,
          gender: this.selectedPatient.gender,
          birthday: this.selectedPatient.birthday,
          phone: this.selectedPatient.phone,
          record: tt,
          // records: this.selectedPatient.records
        };
        
        const response = await fetch(`${this.apiBaseUrl}/user/selectAndUpdate/`, {
          method: 'PATCH',
          headers: this.headers,
          body: JSON.stringify(patientData)
        });
        
        if (!response.ok) {
          throw new Error('添加病历记录失败');
        }
        
        this.showToast('病历记录添加成功', 'success');
        this.selectedPatient.records[0].description = '',
        this.selectedPatient.record = tt
        this.showRecordModal = false;
      } catch (error) {
        console.error('保存病历记录错误:', error);
        this.showToast('添加病历记录失败', 'error');
      } finally {
        this.isSubmitting = false;
      }
    },
    
    // 删除患者
    async deletePatient() {
      if (!this.patientToDelete) return;
      
      try {
        this.isSubmitting = true;
        
        // 发送删除请求
        const response = await fetch(`${this.apiBaseUrl}/user/selectAndUpdate/`, {
          method: 'DELETE',
          headers: this.headers,
          body: JSON.stringify({ patient_id: parseInt(this.patientToDelete.id) })
        });
        
        if (!response.ok) {
          throw new Error('删除患者失败');
        }
        
        // 从本地列表中移除
        const index = this.patients.findIndex(p => p.id === this.patientToDelete.id);
        if (index !== -1) {
          this.patients.splice(index, 1);
        }
        
        // 如果删除的是当前选中的患者，清除选中状态
        if (this.selectedPatient && this.selectedPatient.id === this.patientToDelete.id) {
          this.selectedPatient = null;
        }
        
        this.showToast('患者记录已删除', 'success');
        this.showDeleteModal = false;
        this.patientToDelete = null;
      } catch (error) {
        console.error('删除患者错误:', error);
        this.showToast('删除患者失败', 'error');
      } finally {
        this.isSubmitting = false;
      }
    },
    
    // 显示消息提示
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
};
</script>

<style scoped>
/* 全局样式 */
.patient-management {
  display: flex;
  flex-direction: column;
  height: 90vh;
  background-color: #f5f7fa;
  position: relative;
}

/* 页面标题和操作区 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 50px 24px;
  padding-bottom: 0;
}

.header-left h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
}

.subtitle {
  margin: 4px 0 0 0;
  font-size: 14px;
  color: #606266;
}

.header-actions {
  display: flex;
  align-items: center;
}

.search-box {
  position: relative;
  margin-right: 16px;
}

.search-box input {
  width: 240px;
  height: 36px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 32px 0 12px;
  font-size: 14px;
  transition: all 0.3s;
}

.search-box input:focus {
  border-color: #409eff;
  outline: none;
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #909399;
}

.btn-add {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #72b3e3, #4299e1);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0 16px;
  height: 36px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-add svg {
  margin-right: 6px;
}

.btn-add:hover {
  background: linear-gradient(135deg, #63b3ed, #3182ce);
  transform: translateY(-1px);
}

/* 筛选区域 */
.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  border-radius: 4px;
  padding: 16px 24px;
  margin: 16px 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  margin-bottom: 50px;
}

.filter-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-item {
  display: flex;
  align-items: center;
}

.filter-item label {
  margin-right: 8px;
  font-size: 14px;
  color: #606266;
}

.filter-item select,
.filter-item input {
  height: 32px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 8px;
  font-size: 14px;
  color: #606266;
  background-color: #fff;
  min-width: 120px;
}

.filter-item select:focus,
.filter-item input:focus {
  border-color: #409eff;
  outline: none;
}

.btn-reset {
  display: flex;
  align-items: center;
  background-color: transparent;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 12px;
  height: 32px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-reset svg {
  margin-right: 6px;
}

.btn-reset:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

/* 患者列表 */
.patient-list-container {
  background-color: #fff;
  border-radius: 4px;
  margin: 0 24px 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

/* 表头和内容部分居中对齐 */
.patient-list-header {
  display: grid;
  grid-template-columns: 140px 100px 140px 140px 200px 140px;
  background-color: #f5f7fa;
  padding: 12px 16px;
  font-weight: 500;
  color: #606266;
  border-bottom: 1px solid #ebeef5;
  text-align: center; /* 表头居中对齐 */
}

.patient-item {
  display: grid;
  grid-template-columns: 140px 100px 140px 140px 200px 140px;
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
  transition: all 0.3s;
  cursor: pointer;
  text-align: center; /* 内容居中对齐 */
}

.patient-info {
  color: #606266;
  font-size: 14px;
  overflow: hidden;
}

.record-info {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.record-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.patient-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.btn-view, .btn-edit, .btn-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view {
  background-color: #ecf5ff;
  color: #409eff;
}

.btn-view:hover {
  background-color: #d9ecff;
}

.btn-edit {
  background-color: #f0f9eb;
  color: #67c23a;
}

.btn-edit:hover {
  background-color: #e1f3d8;
}

.btn-delete {
  background-color: #fef0f0;
  color: #f56c6c;
}

.btn-delete:hover {
  background-color: #fde2e2;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  color: #909399;
}
.patient-item.selected {
  background-color: #ecf5ff;
}

.patient-item:hover {
  background-color: #f5f7fa;
}

.patient-name {
  display: flex;
  align-items: center;
  justify-content: center;
}

.patient-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 8px;
  margin-bottom: 5px;
}

.patient-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
  border-top: 1px solid #ebeef5;
}

.pagination-btn {
  display: flex;
  align-items: center;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 12px;
  height: 32px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination-btn svg {
  margin-right: 4px;
}

.pagination-btn:hover:not(:disabled) {
  color: #409eff;
  border-color: #c6e2ff;
}

.pagination-btn:disabled {
  color: #c0c4cc;
  cursor: not-allowed;
}

.page-info {
  margin: 0 16px;
  font-size: 14px;
  color: #606266;
}

/* 患者详情侧边栏 */
.patient-details {
  position: fixed;
  top: 0;
  right: 0;
  width: 360px;
  height: 100%;
  background-color: #fff;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.patient-details.active {
  transform: translateX(0);
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.details-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #2c3e50;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #909399;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.3s;
}

.btn-close:hover {
  background-color: #f5f7fa;
  color: #606266;
}

.patient-profile {
  display: flex;
  align-items: center;
  padding: 24px 16px;
  border-bottom: 1px solid #ebeef5;
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 16px;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.profile-info p {
  font-size: 14px;
  color: #606266;
  margin: 0;
}

.details-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h5 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #2c3e50;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h5 {
  margin: 0;
  padding: 0;
  border: none;
}

.btn-add-small {
  display: flex;
  align-items: center;
  background: none;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 8px;
  height: 24px;
  font-size: 12px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-add-small svg {
  margin-right: 4px;
}

.btn-add-small:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.detail-item {
  display: flex;
  margin-bottom: 12px;
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

.medical-records {
  margin-bottom: 16px;
}

.record-item {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px dashed #ebeef5;
}

.record-date {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.record-content {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

.record-content p {
  margin: 0 0 8px 0;
}

.record-doctor {
  font-size: 12px;
  color: #909399;
}

.no-records,
.no-visits {
  display: flex;
  justify-content: center;
  padding: 24px 0;
  color: #909399;
  font-size: 14px;
}

.visit-history {
  margin-top: 16px;
}

.timeline {
  position: relative;
}

.timeline-item {
  position: relative;
  padding-left: 20px;
  margin-bottom: 24px;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-point {
  position: absolute;
  left: 0;
  top: 6px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #409eff;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 4px;
  top: 16px;
  bottom: -24px;
  width: 2px;
  background-color: #ebeef5;
}

.timeline-item:last-child::before {
  display: none;
}

.timeline-date {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.timeline-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.timeline-description {
  font-size: 14px;
  color: #606266;
}

/* 模态框 */
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
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  z-index: 1002;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #2d3748;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: calc(90vh - 70px);
}

.btn-close {
  background: transparent;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #718096;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #f7fafc;
  color: #4a5568;
}

/* 表单样式优化 */
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #2d3748;
  background-color: white;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

.required {
  color: #e53e3e;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-cancel {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #4a5568;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #f7fafc;
}

.btn-save {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #72b3e3, #4299e1);
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: linear-gradient(135deg, #63b3ed, #3182ce);
  transform: translateY(-1px);
}

.btn-save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.delete-confirm {
  width: 400px;
}

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

/* 消息提示 */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1100;
}

.toast-content {
  display: flex;
  align-items: center;
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

.toast-content svg {
  margin-right: 8px;
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

/* 加载指示器 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #72b3e3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .patient-details {
    width: 320px;
  }
}

@media (max-width: 992px) {
  .patient-list-header,
  .patient-item {
    grid-template-columns: 1fr 0.5fr 0.5fr 1fr 1fr 0.8fr;
  }

  .list-header-item:nth-child(6),
  .patient-info:nth-child(6) {
    display: none;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    margin-top: 16px;
    width: 100%;
  }

  .search-box {
    flex: 1;
    margin-right: 8px;
  }

  .search-box input {
    width: 100%;
  }

  .filter-section {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-group {
    width: 100%;
    margin-bottom: 12px;
  }

  .filter-item {
    width: 100%;
    margin-right: 0;
    margin-bottom: 8px;
  }

  .filter-item select,
  .filter-item input {
    width: 100%;
  }

  .btn-reset {
    width: 100%;
  }

  .patient-list-header,
  .patient-item {
    grid-template-columns: 1fr 0.5fr 0.5fr 0.8fr;
  }

  .list-header-item:nth-child(4),
  .patient-info:nth-child(4),
  .list-header-item:nth-child(5),
  .patient-info:nth-child(5),
  .list-header-item:nth-child(6),
  .patient-info:nth-child(6) {
    display: none;
  }

  .patient-details {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .patient-list-header,
  .patient-item {
    grid-template-columns: 1fr 0.5fr 0.8fr;
  }

  .list-header-item:nth-child(3),
  .patient-info:nth-child(3),
  .list-header-item:nth-child(4),
  .patient-info:nth-child(4),
  .list-header-item:nth-child(5),
  .patient-info:nth-child(5),
  .list-header-item:nth-child(6),
  .patient-info:nth-child(6) {
    display: none;
  }

  .modal-content {
    width: 95%;
  }
}
</style>
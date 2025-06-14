<template>
  <div class="doctor-diagnosis-history-container">
    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-group">
        <label>诊断时间:</label>
        <select v-model="filter.dateRange">
          <option value="all">全部时间</option>
          <option value="week">近一周</option>
          <option value="month">近一月</option>
          <option value="quarter">近三月</option>
          <option value="year">近一年</option>
        </select>
      </div>

      <div class="filter-group">
        <label>诊断类型:</label>
        <select v-model="filter.diagnosisType">
          <option value="all">全部类型</option>
          <option value="retina">视网膜检查</option>
          <option value="glaucoma">青光眼检查</option>
          <option value="cataract">白内障检查</option>
          <option value="macula">黄斑检查</option>
        </select>
      </div>

      <div class="filter-group">
        <label>诊断结果:</label>
        <select v-model="filter.result">
          <option value="all">全部结果</option>
          <option value="normal">正常</option>
          <option value="abnormal">异常</option>
          <option value="urgent">紧急</option>
        </select>
      </div>

      <button class="filter-btn" @click="applyFilters">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="16 18 22 12 16 6"></polyline>
          <polyline points="8 6 2 12 8 18"></polyline>
        </svg>
        筛选
      </button>
    </div>

    <!-- 诊断历史列表 -->
    <div class="diagnosis-list">
      <div class="diagnosis-item" v-for="diagnosis in filteredDiagnoses" :key="diagnosis.patient_id">
        <div class="diagnosis-header">
          <div class="patient-info">
            <!-- 使用SVG图标替代头像 -->
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 640 512" fill="currentColor">
              <path d="M352 32C229 32 128 133 128 256S229 480 352 480 576 377 576 256 475 32 352 32z"/>
            </svg>
            <div>
              <div class="patient-name">{{ diagnosis.patientName }}</div>
              <div class="patient-id">ID: {{ diagnosis.patient_id }}</div>
            </div>
          </div>
          <div class="diagnosis-date">{{ diagnosis.date }}</div>
          <div :class="`diagnosis-status ${diagnosis.status}`">{{ diagnosis.statusText }}</div>
        </div>

        <div class="diagnosis-details">
          <div class="diagnosis-type">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            {{ diagnosis.type }}
          </div>

        <div class="diagnosis-result">
    <!-- 增加对无异常状态的判断 -->
    <svg v-if="diagnosis.result === '正常' && diagnosis.resultText === '状态良好，无异常'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#48bb78" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    <!-- 原本的正常状态图标 -->
    <svg v-else-if="diagnosis.result === '正常'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#48bb78" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    <!-- 其他状态的图标逻辑保持不变 -->
    <svg v-else-if="diagnosis.result === 'abnormal'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#edd400" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
    <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f56565" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="15" y1="9" x2="9" y2="15"></line>
        <line x1="9" y1="9" x2="15" y2="15"></line>
    </svg>
    {{ diagnosis.resultText }}
</div>

          <div class="diagnosis-actions">
            <button class="action-btn view" @click="viewDiagnosis(diagnosis)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              查看
            </button>
            <button class="action-btn download" @click="downloadReport(diagnosis)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              下载
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <button class="page-btn" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <button class="page-btn" v-for="page in totalPages" :key="page" :class="{ active: page === currentPage }" @click="changePage(page)">
        {{ page }}
      </button>
      <button class="page-btn" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorDiagnosisHistory',
  data() {
    return {
      // 筛选条件
      filter: {
        dateRange: 'all',
        diagnosisType: 'all',
        result: 'all'
      },
      
      // 分页
      currentPage: 1,
      itemsPerPage: 8,
      totalItems: 0,
      
      // 诊断历史数据
      diagnoses: []
    };
  },
  computed: {
    // 筛选后的诊断历史
    filteredDiagnoses() {
      let result = this.diagnoses;
      
      // 按诊断时间筛选
      if (this.filter.dateRange !== 'all') {
        const now = new Date();
        let startDate;
        
        switch (this.filter.dateRange) {
          case 'week':
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            break;
          case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth(), 1);
            break;
          case 'quarter':
            const month = now.getMonth();
            const quarterStart = Math.floor(month / 3) * 3;
            startDate = new Date(now.getFullYear(), quarterStart, 1);
            break;
          case 'year':
            startDate = new Date(now.getFullYear(), 0, 1);
            break;
        }
        
        result = result.filter(diagnosis => {
          const diagDate = new Date(diagnosis.date);
          return diagDate >= startDate;
        });
      }
      
      // 按诊断类型筛选
      if (this.filter.diagnosisType !== 'all') {
        const typeMap = {
          'retina': '视网膜检查',
          'glaucoma': '青光眼检查',
          'cataract': '白内障检查',
          'macula': '黄斑检查'
        };
        result = result.filter(diagnosis => diagnosis.type === typeMap[this.filter.diagnosisType]);
      }
      
      // 按诊断结果筛选
      if (this.filter.result !== 'all') {
        const resultMap = {
          'normal': '正常',
          'abnormal': '异常',
          'urgent': '紧急'
        };
        result = result.filter(diagnosis => diagnosis.result === resultMap[this.filter.result]);
      }
      
      // 计算总条目数
      this.totalItems = result.length;
      
      // 分页
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return result.slice(start, end);
    },
    
    // 总页数
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    }
  },
  mounted() {
    // 获取患者列表
    this.fetchDiagnosisData();
  },
  methods: {
    // 获取诊断数据
    async fetchDiagnosisData() {
      try {
        const info = localStorage.getItem('info');
        if (!info) {
          console.error('No user info found in localStorage');
          return;
        }

        const parsedInfo = JSON.parse(info);
        if (!parsedInfo || !parsedInfo.token) {
          console.error('No token found in user info');
          return;
        }

        const token = parsedInfo.token;
        
        const response = await fetch('http://8.155.59.127:34561/user/detail/', {
          method: 'GET',
          headers: {
            'token': `${token}`
          }
        });

        if (!response.ok) {
          console.error('Failed to fetch diagnosis data:', response.statusText);
          return;
        }

        const data = await response.json();
        
        // 模拟诊断数据
        this.diagnoses = data.map(patient => {
          const diagnosisTypes = ['视网膜检查', '青光眼检查', '白内障检查', '黄斑检查'];
          const diagnosisResults = ['正常', '异常', '紧急'];
          
          // 根据record字段填充诊断结果
          let result = '';
          let resultText = '';
          if (patient.record === 'null') {
            result = diagnosisResults[Math.floor(Math.random() * diagnosisResults.length)];
            resultText = this.generateRandomDiagnosisText(result);
          } else if (patient.record === '白内障') {
            result = '紧急';
            resultText = '白内障进展迅速，建议尽快手术';
          } else if (patient.record === '青光眼') {
            result = '异常';
            resultText = '眼内压偏高，建议进一步检查';
          } else {
            result = '正常';
            resultText = '状态良好，无异常';
          }
          
          return {
            patient_id: patient.patient_id,
            patientName: patient.patientName,
            date: this.generateRandomDate(),
            type: diagnosisTypes[Math.floor(Math.random() * diagnosisTypes.length)],
            result: result,
            resultText: resultText,
            status: result.toLowerCase(),
            statusText: result
          };
        });
      } catch (error) {
        console.error('Error fetching diagnosis data:', error);
      }
    },
    
    // 生成随机诊断文本
    generateRandomDiagnosisText(result) {
      const normalTexts = ['状态良好，无异常', '一切正常，无需担心'];
      const abnormalTexts = ['发现轻微异常，建议复查', '需要进一步检查确认'];
      const urgentTexts = ['情况紧急，需立即处理', '需要尽快安排治疗'];
      
      switch(result) {
        case '正常':
          return normalTexts[Math.floor(Math.random() * normalTexts.length)];
        case '异常':
          return abnormalTexts[Math.floor(Math.random() * abnormalTexts.length)];
        case '紧急':
          return urgentTexts[Math.floor(Math.random() * urgentTexts.length)];
        default:
          return '状态良好，无异常';
      }
    },
    
    // 生成随机日期（过去一年内的日期）
    generateRandomDate() {
      const now = new Date();
      const pastYear = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
      
      const randomDate = new Date(
        pastYear.getTime() + Math.random() * (now.getTime() - pastYear.getTime())
      );
      
      return randomDate.toISOString().split('T')[0];
    },
    
    // 应用筛选条件
    applyFilters() {
      this.currentPage = 1;
    },
    
    // 查看诊断详情
    viewDiagnosis(diagnosis) {
      console.log('查看诊断详情:', diagnosis);
      // 添加查看诊断详情的逻辑
    },
    
    // 下载诊断报告
    downloadReport(diagnosis) {
      console.log('下载诊断报告:', diagnosis);
      // 添加下载诊断报告的逻辑
    },
    
    // 切换页面
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  },
};
</script>

<style scoped>
/* 全局样式 */
.doctor-diagnosis-history-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #2c3e50;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

/* 筛选区域 */
.filter-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  background-color: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  color: #4a5568;
  font-size: 0.9rem;
}

.filter-group select {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
  color: #2d3748;
}

.filter-btn {
  padding: 0.5rem 1.5rem;
  background-color: #4facfe;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.filter-btn:hover {
  background-color: #3b9eef;
}

/* 诊断历史列表 */
.diagnosis-list {
  background-color: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.diagnosis-item {
  border-bottom: 1px solid #edf2f7;
  padding: 1.25rem 0;
}

.diagnosis-item:last-child {
  border-bottom: none;
}

.diagnosis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.patient-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.diagnosis-patient svg {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #f8fafc;
}

.patient-name {
  font-size: 1rem;
  font-weight: 500;
  color: #2c3e50;
}

.patient-id {
  font-size: 0.85rem;
  color: #718096;
}

.diagnosis-date {
  color: #718096;
  font-size: 0.9rem;
}

.diagnosis-status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  color: white;
}

.diagnosis-status.normal {
  background-color: #c6f6d5;
}

.diagnosis-status.abnormal {
  background-color: #fef9c3;
}

.diagnosis-status.urgent {
  background-color: #fed7d7;
}

.diagnosis-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.diagnosis-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
  font-size: 0.9rem;
}

.diagnosis-result {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.diagnosis-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.action-btn.view {
  background-color: #e6f7ff;
  color: #4facfe;
}

.action-btn.download {
  background-color: #f8fafc;
  color: #718096;
}

.action-btn:hover {
  opacity: 0.9;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.page-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  background-color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn.active {
  background-color: #4facfe;
  color: white;
  border-color: #4facfe;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
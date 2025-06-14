<template>
   <div v-if="activeMenu === 'dashboard'" class="dashboard-content">
          <div class="stats-cards">
            <div class="stat-card">
              <div class="stat-icon bg-blue">
                <i class="icon-patients"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">128</div>
                <div class="stat-label">今日患者</div>
              </div>
              <div class="stat-trend up">
                <i class="icon-trend-up"></i>
                <span>+12.5%</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon bg-green">
                <i class="icon-diagnosis"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">85</div>
                <div class="stat-label">诊断完成</div>
              </div>
              <div class="stat-trend up">
                <i class="icon-trend-up"></i>
                <span>+5.2%</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon bg-purple">
                <i class="icon-accuracy"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">94.8%</div>
                <div class="stat-label">诊断准确率</div>
              </div>
              <div class="stat-trend up">
                <i class="icon-trend-up"></i>
                <span>+1.3%</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon bg-orange">
                <i class="icon-pending"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">43</div>
                <div class="stat-label">待处理</div>
              </div>
              <div class="stat-trend down">
                <i class="icon-trend-down"></i>
                <span>-8.4%</span>
              </div>
            </div>
          </div>
          
          <div class="dashboard-row">
            <div class="chart-container">
              <div class="chart-header">
                <h3>诊断趋势</h3>
                <div class="chart-actions">
                  <button class="btn-outline active">周</button>
                  <button class="btn-outline">月</button>
                  <button class="btn-outline">年</button>
                </div>
              </div>
              <div class="chart-placeholder">
                <!-- 这里放置图表，实际项目中可以使用ECharts等库 -->
                <div class="chart-bars">
                  <div class="chart-bar" style="height: 60%"><span>周一</span></div>
                  <div class="chart-bar" style="height: 80%"><span>周二</span></div>
                  <div class="chart-bar" style="height: 65%"><span>周三</span></div>
                  <div class="chart-bar" style="height: 90%"><span>周四</span></div>
                  <div class="chart-bar" style="height: 75%"><span>周五</span></div>
                  <div class="chart-bar" style="height: 50%"><span>周六</span></div>
                  <div class="chart-bar" style="height: 40%"><span>周日</span></div>
                </div>
              </div>
            </div>
            
            <div class="recent-patients">
              <div class="section-header">
                <h3>最近患者</h3>
                <a href="#" class="view-all">查看全部</a>
              </div>
              <div class="patient-list">
                <div class="patient-item" v-for="(patient, index) in recentPatients" :key="index">
                  <div class="patient-avatar">
                    <img :src="patient.avatar" :alt="patient.name">
                  </div>
                  <div class="patient-info">
                    <div class="patient-name">{{ patient.name }}</div>
                    <div class="patient-diagnosis">{{ patient.diagnosis }}</div>
                  </div>
                  <div class="patient-time">{{ patient.time }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.bg-blue {
  background: linear-gradient(135deg, #0099ff 0%, #0066cc 100%);
}

.bg-green {
  background: linear-gradient(135deg, #00cc66 0%, #009933 100%);
}

.bg-purple {
  background: linear-gradient(135deg, #9966ff 0%, #6633cc 100%);
}

.bg-orange {
  background: linear-gradient(135deg, #ff9933 0%, #ff6600 100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.stat-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 500;
}

.stat-trend.up {
  color: #00cc66;
}

.stat-trend.down {
  color: #ff3860;
}

.icon-trend-up, .icon-trend-down {
  width: 16px;
  height: 16px;
  margin-right: 5px;
}

.icon-trend-up {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%2300cc66"><path d="M7 14l5-5 5 5z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-trend-down {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23ff3860"><path d="M7 10l5 5 5-5z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.dashboard-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.chart-container, .recent-patients {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.chart-header, .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3, .section-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.chart-actions {
  display: flex;
  gap: 10px;
}

.btn-outline {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: transparent;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover, .btn-outline.active {
  border-color: #0099ff;
  color: #0099ff;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 20px 0;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  width: 100%;
  height: 100%;
}

.chart-bar {
  width: 40px;
  background: linear-gradient(180deg, #0099ff 0%, #0066cc 100%);
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: all 0.3s;
}

.chart-bar:hover {
  opacity: 0.8;
}

.chart-bar span {
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: #666;
  white-space: nowrap;
}

.view-all {
  color: #0099ff;
  text-decoration: none;
  font-size: 14px;
}

.view-all:hover {
  text-decoration: underline;
}

.patient-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.patient-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  transition: all 0.2s;
}

.patient-item:hover {
  background: #f5f7fa;
}

.patient-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
}

.patient-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.patient-info {
  flex: 1;
}

.patient-name {
  font-weight: 500;
  color: #333;
}

.patient-diagnosis {
  font-size: 13px;
  color: #666;
}

.patient-time {
  font-size: 12px;
  color: #999;
}
</style>
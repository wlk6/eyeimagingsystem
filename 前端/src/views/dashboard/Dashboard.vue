<template>
  <div class="dashboard">
    
    <div class="dashboard-content">
      <!-- 欢迎卡片 -->
      <div class="welcome-card">
        <div class="welcome-text">
          <h2>欢迎回来，{{ doctorInfo.doctor_name || '医生' }}</h2>
          <p>今天是 {{ currentDate }}，您有 <strong>{{ notifications.messages }}</strong> 条新消息和 <strong>{{ notifications.pending }}</strong> 个待处理的诊断。</p>
          <div class="welcome-stats">
            <div class="welcome-stat">
              <div class="welcome-stat-value">{{ todayStats.completed }}</div>
              <div class="welcome-stat-label">今日已完成</div>
            </div>
            <div class="welcome-stat">
              <div class="welcome-stat-value">{{ todayStats.scheduled }}</div>
              <div class="welcome-stat-label">今日预约</div>
            </div>
            <div class="welcome-stat">
              <div class="welcome-stat-value">{{ todayStats.urgent }}</div>
              <div class="welcome-stat-label">紧急诊断</div>
            </div>
          </div>
        </div>
        <div class="welcome-actions">
          <button class="action-button primary" @click="navigateToDiagnosis">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
            <span>新建诊断</span>
          </button>
          <button class="action-button secondary" @click="navigateToPatients">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span>添加患者</span>
          </button>
        </div>
      </div>
      
      <!-- 眼睛相关SVG装饰 -->
      <div class="eye-decoration">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#72b3e3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
          <path d="M12 14c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"/>
        </svg>
      </div>
      
      <!-- 数据概览卡片 -->
      <div class="stats-overview">
        <div class="stat-card" @mouseenter="showTooltip('patients')" @mouseleave="hideTooltip">
          <div class="stat-icon blue">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </div>
          <div class="stat-details">
            <div class="stat-value">{{ stats.patients }}</div>
            <div class="stat-label">总患者数</div>
            <div class="stat-trend up">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="18 15 12 9 6 15"></polyline>
              </svg>
              <span>↑ {{ stats.patientsTrend }}% 本月</span>
            </div>
          </div>
          <div v-if="activeTooltip === 'patients'" class="stat-tooltip">
            <div class="tooltip-title">患者数据详情</div>
            <div class="tooltip-row">
              <span>新增患者:</span>
              <span>{{ tooltipData.patients.new }} 人</span>
            </div>
            <div class="tooltip-row">
              <span>回访患者:</span>
              <span>{{ tooltipData.patients.returning }} 人</span>
            </div>
            <div class="tooltip-row">
              <span>平均年龄:</span>
              <span>{{ tooltipData.patients.avgAge }} 岁</span>
            </div>
          </div>
        </div>
        
        <div class="stat-card" @mouseenter="showTooltip('diagnoses')" @mouseleave="hideTooltip">
          <div class="stat-icon green">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v12" />
              <path d="M6 12h12" />
            </svg>
          </div>
          <div class="stat-details">
            <div class="stat-value">{{ stats.diagnoses }}</div>
            <div class="stat-label">本月诊断</div>
            <div class="stat-trend up">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="18 15 12 9 6 15"></polyline>
              </svg>
              <span>↑ {{ stats.diagnosesTrend }}% 上月</span>
            </div>
          </div>
          <div v-if="activeTooltip === 'diagnoses'" class="stat-tooltip">
            <div class="tooltip-title">诊断数据详情</div>
            <div class="tooltip-row">
              <span>初诊:</span>
              <span>{{ tooltipData.diagnoses.initial }} 例</span>
            </div>
            <div class="tooltip-row">
              <span>复诊:</span>
              <span>{{ tooltipData.diagnoses.followUp }} 例</span>
            </div>
            <div class="tooltip-row">
              <span>紧急诊断:</span>
              <span>{{ tooltipData.diagnoses.urgent }} 例</span>
            </div>
          </div>
        </div>
        
        <div class="stat-card" @mouseenter="showTooltip('accuracy')" @mouseleave="hideTooltip">
          <div class="stat-icon purple">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </div>
          <div class="stat-details">
            <div class="stat-value">{{ stats.accuracy }}%</div>
            <div class="stat-label">诊断准确率</div>
            <div class="stat-trend up">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="18 15 12 9 6 15"></polyline>
              </svg>
              <span>↑ {{ stats.accuracyTrend }}% 上月</span>
            </div>
          </div>
          <div v-if="activeTooltip === 'accuracy'" class="stat-tooltip">
            <div class="tooltip-title">准确率详情</div>
            <div class="tooltip-row">
              <span>视网膜病变:</span>
              <span>{{ tooltipData.accuracy.retina }}%</span>
            </div>
            <div class="tooltip-row">
              <span>青光眼:</span>
              <span>{{ tooltipData.accuracy.glaucoma }}%</span>
            </div>
            <div class="tooltip-row">
              <span>白内障:</span>
              <span>{{ tooltipData.accuracy.cataract }}%</span>
            </div>
          </div>
        </div>
        
        <div class="stat-card" @mouseenter="showTooltip('response')" @mouseleave="hideTooltip">
          <div class="stat-icon orange">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="16" />
              <line x1="8" y1="12" x2="16" y2="12" />
            </svg>
          </div>
          <div class="stat-details">
            <div class="stat-value">{{ stats.responseTime }}小时</div>
            <div class="stat-label">平均响应时间</div>
            <div class="stat-trend down">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
              <span>↓ {{ stats.responseTimeTrend }}小时 上月</span>
            </div>
          </div>
          <div v-if="activeTooltip === 'response'" class="stat-tooltip">
            <div class="tooltip-title">响应时间详情</div>
            <div class="tooltip-row">
              <span>紧急案例:</span>
              <span>{{ tooltipData.response.urgent }}小时</span>
            </div>
            <div class="tooltip-row">
              <span>常规案例:</span>
              <span>{{ tooltipData.response.regular }}小时</span>
            </div>
            <div class="tooltip-row">
              <span>最快响应:</span>
              <span>{{ tooltipData.response.fastest }}分钟</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 图表区域 -->
      <div class="charts-container">
        <div class="chart-card">
          <div class="chart-header">
            <h3>近期诊断趋势</h3>
            <div class="chart-actions">
              <select class="period-select" v-model="selectedPeriod" @change="updateChartData">
                <option value="week">本周</option>
                <option value="month">本月</option>
                <option value="quarter">本季度</option>
                <option value="year">本年</option>
              </select>
            </div>
          </div>
          <div class="chart-body">
            <div class="chart-placeholder" ref="trendChart">
              <svg width="100%" height="250" viewBox="0 0 600 250" preserveAspectRatio="none">
                <!-- 背景网格 -->
                <line v-for="(line, index) in 5" :key="'hline-'+index" x1="0" :y1="50 + index * 50" x2="600" :y2="50 + index * 50" stroke="#b0d3f1" stroke-width="1" stroke-dasharray="5,5" />
                <line v-for="(line, index) in 5" :key="'vline-'+index" :x1="index * 150" y1="0" :x2="index * 150" y2="250" stroke="#b0d3f1" stroke-width="1" stroke-dasharray="5,5" />
                
                <!-- 填充区域 -->
                <path :d="chartData.areaPath" fill="#e6f7ff" />
                
                <!-- 线条 -->
                <path :d="chartData.linePath" stroke="#72b3e3" stroke-width="3" fill="none" class="chart-line" />
                
                <!-- 数据点 -->
                <g>
                  <circle v-for="(point, index) in chartData.points" :key="index" 
                    :cx="point.x" :cy="point.y" r="5" 
                    fill="#72b3e3" stroke="#ffffff" stroke-width="2"
                    class="data-point"
                    @mouseenter="showDataTooltip(point, $event)" 
                    @mouseleave="hideDataTooltip" />
                </g>
                
                <!-- X轴标签 -->
                <text v-for="(label, index) in chartData.labels" :key="'label-'+index" 
                  :x="index * (600 / (chartData.labels.length - 1))" y="270" 
                  font-size="12" fill="#718096" text-anchor="middle">
                  {{ label }}
                </text>
                
                <!-- Y轴标签 -->
                <text x="-30" y="50" font-size="12" fill="#718096">高</text>
                <text x="-30" y="150" font-size="12" fill="#718096">中</text>
                <text x="-30" y="250" font-size="12" fill="#718096">低</text>
              </svg>
              
              <!-- 数据点悬浮提示 -->
              <div v-if="dataTooltip.visible" class="data-tooltip" :style="dataTooltip.style">
                <div class="data-tooltip-title">{{ dataTooltip.title }}</div>
                <div class="data-tooltip-value">诊断数: {{ dataTooltip.value }}</div>
                <div class="data-tooltip-info">同比: <span :class="dataTooltip.trend >= 0 ? 'trend-up' : 'trend-down'">
                  {{ dataTooltip.trend >= 0 ? '↑' : '↓' }} {{ Math.abs(dataTooltip.trend) }}%
                </span></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chart-card">
          <div class="chart-header">
            <h3>诊断分类统计</h3>
            <div class="chart-actions">
              <select class="period-select" v-model="selectedPieChartPeriod" @change="updatePieChartData">
                <option value="month">本月</option>
                <option value="quarter">本季度</option>
                <option value="year">本年</option>
              </select>
            </div>
          </div>
          <div class="chart-body">
            <div class="chart-placeholder" ref="pieChart">
              <svg width="100%" height="250" viewBox="0 0 600 250" preserveAspectRatio="none">
                <!-- 饼图部分 -->
                <g transform="translate(150, 125)">
                  <path v-for="(slice, index) in pieChartData.slices" :key="'slice-'+index"
                    :d="slice.path" 
                    :fill="activeSlice === index ? slice.highlightColor : slice.color" 
                    :class="['pie-slice', { 'active-slice': activeSlice === index }]"
                    @mouseenter="highlightSlice(index, $event, true)"
                    @mouseleave="resetSlice">
                    <animate attributeName="opacity" from="0" to="1" dur="0.5s" :begin="index * 0.1 + 's'" fill="freeze" />
                  </path>
                  
                  <!-- 饼图悬浮提示 - 直接在SVG中显示 -->
                  <g v-if="pieTooltip.visible && pieTooltip.index === index" 
                     :transform="`translate(${slice.tooltipX}, ${slice.tooltipY})`"
                     class="pie-tooltip-svg">
                    <rect x="-60" y="-40" width="120" height="80" rx="5" fill="white" stroke="#e2e8f0" />
                    <text x="0" y="-20" text-anchor="middle" font-weight="bold" font-size="12">{{ slice.name }}</text>
                    <text x="0" y="0" text-anchor="middle" font-size="11">{{ slice.value }} 例 ({{ slice.percentage }}%)</text>
                    <text x="0" y="20" text-anchor="middle" font-size="11">
                      同比: 
                      <tspan :fill="slice.trend >= 0 ? '#48bb78' : '#f56565'">
                        {{ slice.trend >= 0 ? '↑' : '↓' }} {{ Math.abs(slice.trend) }}%
                      </tspan>
                    </text>
                  </g>
                </g>
                
                <!-- 中心圆 -->
                <circle cx="150" cy="125" r="40" fill="white" />
                <text x="150" y="125" text-anchor="middle" dominant-baseline="middle" font-size="14" font-weight="bold" fill="#4a5568">
                  {{ pieChartData.total }}
                </text>
                <text x="150" y="145" text-anchor="middle" dominant-baseline="middle" font-size="12" fill="#718096">
                  总诊断数
                </text>
                
                <!-- 图例 -->
                <g>
                  <g v-for="(item, index) in pieChartData.legend" :key="'legend-'+index" 
                     :transform="`translate(300, ${50 + index * 30})`"
                     @mouseenter="highlightSlice(index, $event, false)"
                     @mouseleave="resetSlice"
                     class="legend-item">
                    <rect x="0" y="-10" width="15" height="15" :fill="activeSlice === index ? item.highlightColor : item.color" />
                    <text x="25" y="0" font-size="12" :fill="activeSlice === index ? '#2d3748' : '#4a5568'" font-weight="500">
                      {{ item.name }} ({{ item.percentage }}%)
                    </text>
                  </g>
                </g>
              </svg>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 医生工作量统计 -->
      <div class="doctor-workload">
        <div class="section-header">
          <h3>医生工作量统计</h3>
          <div class="chart-actions">
            <button class="view-all-btn">查看详情</button>
          </div>
        </div>
        <div class="workload-bars">
          <div v-for="(doctor, index) in doctorWorkload" :key="index" class="workload-item">
            <div class="doctor-info">
              <div class="doctor-avatar">
                <img :src="doctor.avatar" alt="医生头像" />
              </div>
              <div class="doctor-name">{{ doctor.name }}</div>
            </div>
            <div class="workload-bar-container">
              <div class="workload-bar" :style="{ width: doctor.percentage + '%' }">
                <span class="workload-value">{{ doctor.count }}例</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 近期诊断列表 -->
      <div class="recent-diagnoses">
        <div class="section-header">
          <h3>近期诊断</h3>
          <button class="view-all-btn">查看全部</button>
        </div>
        <div class="diagnoses-list">
          <div class="diagnosis-item" v-for="diagnosis in recentDiagnoses" :key="diagnosis.id" @click="openDiagnosisDetails(diagnosis)">
            <div class="diagnosis-avatar">
              <img :src="diagnosis.avatar" alt="患者头像" />
            </div>
            <div class="diagnosis-details">
              <div class="diagnosis-patient-name">{{ diagnosis.patientName }}</div>
              <div class="diagnosis-time">{{ diagnosis.time }}</div>
              <div class="diagnosis-type">{{ diagnosis.type }}</div>
              <div class="diagnosis-status" :class="diagnosis.status">
                {{ diagnosis.statusText }}
              </div>
            </div>
            <div class="diagnosis-action">
              <button class="view-diagnosis-btn">详情</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 诊断详情弹窗 -->
    <div v-if="showDiagnosisModal" class="diagnosis-modal" @click="closeDiagnosisModal">
      <div class="diagnosis-modal-content" @click.stop>
        <div class="diagnosis-modal-header">
          <h3>诊断详情</h3>
          <button class="close-modal-btn" @click="closeDiagnosisModal">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="diagnosis-modal-body">
          <div class="patient-info-section">
            <div class="patient-header">
              <div class="patient-avatar">
                <img :src="selectedDiagnosis.avatar" alt="患者头像" />
              </div>
              <div class="patient-basic-info">
                <h4>{{ selectedDiagnosis.patientName }}</h4>
                <div class="patient-id">ID: {{ selectedDiagnosis.id + 10000 }}</div>
                <div class="patient-details">
                  <span>{{ selectedDiagnosis.gender }}</span> | 
                  <span>{{ selectedDiagnosis.age }}岁</span> | 
                  <span>{{ selectedDiagnosis.contact }}</span>
                </div>
              </div>
              <div class="patient-status" :class="selectedDiagnosis.status">
                {{ selectedDiagnosis.statusText }}
              </div>
            </div>
            
            <div class="diagnosis-info-grid">
              <div class="info-card">
                <div class="info-card-label">诊断类型</div>
                <div class="info-card-value">{{ selectedDiagnosis.type }}</div>
              </div>
              <div class="info-card">
                <div class="info-card-label">诊断时间</div>
                <div class="info-card-value">{{ selectedDiagnosis.time }}</div>
              </div>
              <div class="info-card">
                <div class="info-card-label">主诊医生</div>
                <div class="info-card-value">{{ selectedDiagnosis.doctor }}</div>
              </div>
              <div class="info-card">
                <div class="info-card-label">检查设备</div>
                <div class="info-card-value">{{ selectedDiagnosis.equipment }}</div>
              </div>
            </div>
          </div>
          
          <div class="diagnosis-tabs">
            <div class="tab-header">
              <div 
                v-for="(tab, index) in diagnosisTabs" 
                :key="index" 
                :class="['tab-item', { active: activeTab === index }]"
                @click="activeTab = index"
              >
                {{ tab.name }}
              </div>
            </div>
            <div class="tab-content">
              <!-- 诊断结果 -->
              <div v-if="activeTab === 0" class="tab-pane">
                <div class="diagnosis-result">
                  <div class="result-header">
                    <h4>诊断结论</h4>
                    <div class="confidence-level" :class="getConfidenceClass(selectedDiagnosis.confidence)">
                      置信度: {{ selectedDiagnosis.confidence }}%
                    </div>
                  </div>
                  
                  <div class="result-content">
                    <p>{{ selectedDiagnosis.conclusion }}</p>
                  </div>
                  
                  <div class="result-images">
                    <div class="result-image-container" v-for="(image, index) in selectedDiagnosis.images" :key="index">
                      <img :src="image.url" :alt="image.description" class="result-image" />
                      <div class="image-description">{{ image.description }}</div>
                    </div>
                  </div>
                  
                  <div class="ai-analysis">
                    <h4>AI辅助分析</h4>
                    <div class="analysis-content">
                      <p>{{ selectedDiagnosis.aiAnalysis }}</p>
                    </div>
                    <div class="analysis-metrics">
                      <div class="metric" v-for="(metric, index) in selectedDiagnosis.metrics" :key="index">
                        <div class="metric-name">{{ metric.name }}</div>
                        <div class="metric-bar-container">
                          <div class="metric-bar" :style="{ width: metric.value + '%', backgroundColor: getMetricColor(metric.value) }"></div>
                        </div>
                        <div class="metric-value">{{ metric.value }}%</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 患者病史 -->
              <div v-if="activeTab === 1" class="tab-pane">
                <div class="patient-history">
                  <div class="history-timeline">
                    <div class="timeline-item" v-for="(record, index) in selectedDiagnosis.history" :key="index">
                      <div class="timeline-date">{{ record.date }}</div>
                      <div class="timeline-content">
                        <div class="timeline-title">{{ record.title }}</div>
                        <div class="timeline-description">{{ record.description }}</div>
                        <div class="timeline-doctor">医生: {{ record.doctor }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 治疗方案 -->
              <div v-if="activeTab === 2" class="tab-pane">
                <div class="treatment-plan">
                  <div class="plan-section">
                    <h4>治疗建议</h4>
                    <p>{{ selectedDiagnosis.treatmentPlan }}</p>
                  </div>
                  
                  <div class="plan-section">
                    <h4>用药方案</h4>
                    <div class="medication-list">
                      <div class="medication-item" v-for="(med, index) in selectedDiagnosis.medications" :key="index">
                        <div class="medication-name">{{ med.name }}</div>
                        <div class="medication-dosage">{{ med.dosage }}</div>
                        <div class="medication-frequency">{{ med.frequency }}</div>
                        <div class="medication-duration">{{ med.duration }}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="plan-section">
                    <h4>后续随访</h4>
                    <p>{{ selectedDiagnosis.followUp }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="diagnosis-actions">
            <button class="action-btn print">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 6 2 18 2 18 9"></polyline>
                <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                <rect x="6" y="14" width="12" height="8"></rect>
              </svg>
              打印报告
            </button>
            <button class="action-btn share">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="18" cy="5" r="3"></circle>
                <circle cx="6" cy="12" r="3"></circle>
                <circle cx="18" cy="19" r="3"></circle>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
              </svg>
              分享
            </button>
            <button class="action-btn edit">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              编辑
            </button>
            <button class="action-btn primary">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              确认并保存
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataOverview',
  data() {
    return {
      doctorInfo: {}, // 存储医生信息
      currentDate: new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }),
      notifications: {
        messages: 5,
        pending: 3
      },
      todayStats: {
        completed: 0,
        scheduled: 0,
        urgent: 0
      },
      stats: {
        patients: 248,
        patientsTrend: 12,
        diagnoses: 156,
        diagnosesTrend: 8,
        accuracy: 94.2,
        accuracyTrend: 2.1,
        responseTime: 1.8,
        responseTimeTrend: 0.5
      },
      tooltipData: {
        patients: {
          new: 32,
          returning: 216,
          avgAge: 48
        },
        diagnoses: {
          initial: 87,
          followUp: 69,
          urgent: 14
        },
        accuracy: {
          retina: 96.5,
          glaucoma: 93.8,
          cataract: 97.2
        },
        response: {
          urgent: 0.8,
          regular: 2.3,
          fastest: 15
        }
      },
      activeTooltip: null,
      selectedPeriod: 'week',
      selectedPieChartPeriod: 'month',
      chartData: {
        linePath: '',
        areaPath: '',
        points: [],
        labels: []
      },
      pieChartData: {
        slices: [],
        legend: [],
        total: 0
      },
      dataTooltip: {
        visible: false,
        style: {},
        title: '',
        value: 0,
        trend: 0
      },
      pieTooltip: {
        visible: false,
        style: {},
        name: '',
        value: 0,
        percentage: 0,
        trend: 0,
        index: null
      },
      activeSlice: null,
      doctorWorkload: [
        {
          name: '张医生',
          avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
          count: 78,
          percentage: 85
        },
        {
          name: '李医生',
          avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
          count: 65,
          percentage: 70
        },
        {
          name: '王医生',
          avatar: 'https://randomuser.me/api/portraits/men/22.jpg',
          count: 52,
          percentage: 56
        },
        {
          name: '赵医生',
          avatar: 'https://randomuser.me/api/portraits/women/28.jpg',
          count: 43,
          percentage: 47
        }
      ],
      // 近期诊断列表
      recentDiagnoses: [
        {
          id: 1,
          patientName: '李明',
          avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
          time: '今天 14:30',
          type: '视网膜检查',
          status: 'normal',
          statusText: '正常',
          gender: '男',
          age: 45,
          contact: '138****5678',
          doctor: '张医生',
          equipment: 'OptiView Pro 3000',
          confidence: 96,
          conclusion: '患者视网膜状态良好，未发现异常。视力稳定，无需特殊治疗。建议定期复查，保持良好用眼习惯。',
          aiAnalysis: '基于深度学习模型分析，患者视网膜图像未显示任何病变迹象。血管分布正常，黄斑区完整，视盘边界清晰。与历史数据对比，无明显变化。',
          metrics: [
            { name: '视网膜完整性', value: 98 },
            { name: '血管健康度', value: 95 },
            { name: '黄斑区状态', value: 97 }
          ],
          images: [
            { 
              url: 'https://via.placeholder.com/150/0000FF/FFFFFF?text=右眼视网膜图像', 
              description: '右眼视网膜图像：显示视网膜结构完整，血管分布正常，未见出血或渗出。' 
            },
            { 
              url: 'https://via.placeholder.com/150/0000FF/FFFFFF?text=左眼视网膜图像', 
              description: '左眼视网膜图像：显示视网膜结构完整，血管分布正常，未见出血或渗出。' 
            }
          ],
          history: [
            { date: '2023-10-15', title: '常规视力检查', description: '视力稳定，无明显变化', doctor: '王医生' },
            { date: '2022-05-22', title: '视网膜检查', description: '视网膜状态良好，无异常', doctor: '张医生' }
          ],
          treatmentPlan: '无需特殊治疗。建议保持良好用眼习惯，避免长时间用眼疲劳，定期复查。',
          medications: [
            { name: '润眼液', dosage: '每次1-2滴', frequency: '每日3次', duration: '视情况使用' }
          ],
          followUp: '建议3个月后复查，如有不适请及时就诊。'
        },
        {
          id: 2,
          patientName: '王芳',
          avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
          time: '今天 09:45',
          type: '青光眼筛查',
          status: 'abnormal',
          statusText: '异常',
          gender: '女',
          age: 62,
          contact: '139****1234',
          doctor: '李医生',
          equipment: 'GlaucoScan 2000',
          confidence: 92,
          conclusion: '患者眼内压偏高，视神经盘凹陷比例增大，疑似开角型青光眼。建议进一步检查确诊并及时治疗。',
          aiAnalysis: '模型检测到视神经盘凹陷比例为0.65，超出正常范围。眼内压测量值为25mmHg，视野检查显示周边视野缺损。综合分析提示青光眼可能性高。',
          metrics: [
            { name: '眼内压水平', value: 78 },
            { name: '视神经状态', value: 65 },
            { name: '视野完整性', value: 72 }
          ],
          images: [
            { 
              url: 'https://via.placeholder.com/150/FF0000/FFFFFF?text=眼底照片', 
              description: '眼底照片：显示视神经盘凹陷比例增大，杯盘比为0.65，超出正常范围。' 
            },
            { 
              url: 'https://via.placeholder.com/150/FFFF00/000000?text=视神经OCT扫描', 
              description: '视神经OCT扫描：显示视神经纤维层厚度减少，RNFL平均厚度为78μm，低于正常范围。' 
            }
          ],
          history: [
            { date: '2023-08-10', title: '眼压检查', description: '眼压轻度升高，建议观察', doctor: '李医生' },
            { date: '2022-12-05', title: '常规检查', description: '视力下降，疑似白内障早期', doctor: '赵医生' }
          ],
          treatmentPlan: '建议使用降眼压药物控制眼内压，定期监测眼压变化。避免剧烈运动和情绪波动。',
          medications: [
            { name: '噻吗洛尔滴眼液', dosage: '每次1滴', frequency: '每日2次', duration: '长期使用' },
            { name: '拉坦前列素滴眼液', dosage: '每次1滴', frequency: '睡前使用', duration: '长期使用' }
          ],
          followUp: '两周后复查眼压，一个月后进行视野检查和OCT扫描。'
        },
        {
          id: 3,
          patientName: '张伟',
          avatar: 'https://randomuser.me/api/portraits/men/22.jpg',
          time: '昨天 16:20',
          type: '白内障评估',
          status: 'normal',
          statusText: '正常',
          gender: '男',
          age: 68,
          contact: '135****9876',
          doctor: '王医生',
          equipment: 'LensScan HD',
          confidence: 94,
          conclusion: '患者晶状体轻度混浊，属于早期白内障，目前视力影响不大。建议定期观察，适当补充叶黄素等营养素。',
          aiAnalysis: '晶状体核部位出现轻度混浊，LOCS III分级为NC2。前囊完整，后囊无明显混浊。视力检查结果为0.8，较上次检查下降0.1。',
          metrics: [
            { name: '晶状体透明度', value: 75 },
            { name: '视力影响程度', value: 25 },
            { name: '手术必要性', value: 15 }
          ],
          images: [
            { 
              url: 'https://via.placeholder.com/150/00FF00/000000?text=裂隙灯检查图像', 
              description: '裂隙灯检查图像：显示晶状体轻度混浊，前囊完整，后囊无明显混浊。' 
            },
            { 
              url: 'https://via.placeholder.com/150/00FFFF/000000?text=晶状体OCT扫描', 
              description: '晶状体OCT扫描：显示晶状体核轻度混浊，皮质透明度良好，中央厚度为4.2mm。' 
            }
          ],
          history: [
            { date: '2023-06-18', title: '视力检查', description: '视力轻度下降，疑似早期白内障', doctor: '王医生' },
            { date: '2022-09-30', title: '常规检查', description: '视力正常，无明显异常', doctor: '张医生' }
          ],
          treatmentPlan: '目前无需手术治疗。建议佩戴防紫外线眼镜，避免强光刺激，补充叶黄素等营养素。',
          medications: [
            { name: '叶黄素软胶囊', dosage: '每次1粒', frequency: '每日1次', duration: '长期服用' }
          ],
          followUp: '建议6个月后复查，评估白内障进展情况。'
        },
        {
          id: 4,
          patientName: '赵丽',
          avatar: 'https://randomuser.me/api/portraits/women/28.jpg',
          time: '昨天 11:15',
          type: '黄斑变性检查',
          status: 'warning',
          statusText: '需关注',
          gender: '女',
          age: 72,
          contact: '136****4567',
          doctor: '赵医生',
          equipment: 'MacuView 4D',
          confidence: 88,
          conclusion: '患者右眼黄斑区出现早期干性黄斑变性迹象，左眼正常。建议密切观察，补充抗氧化营养素，定期复查。',
          aiAnalysis: '右眼黄斑区检测到少量玻璃膜疣，RPE层轻度不规则。OCT显示黄斑中心凹轮廓保持，但厚度略有减少。无明显渗出和出血迹象。',
          metrics: [
            { name: '黄斑完整性', value: 68 },
            { name: '视网膜色素上皮状态', value: 72 },
            { name: '视功能影响', value: 35 }
          ],
          images: [
            { 
              url: 'https://via.placeholder.com/150/FF00FF/000000?text=右眼黄斑OCT', 
              description: '右眼黄斑OCT：显示黄斑中心凹厚度为220μm，检测到少量玻璃膜疣，RPE层轻度不规则。' 
            },
            { 
              url: 'https://via.placeholder.com/150/00FF00/000000?text=眼底自发荧光成像', 
              description: '眼底自发荧光成像：显示右眼黄斑区出现点状高荧光区，提示玻璃膜疣形成。' 
            }
          ],
          history: [
            { date: '2023-07-25', title: '视力检查', description: '右眼视力轻度下降', doctor: '赵医生' },
            { date: '2022-11-12', title: '黄斑检查', description: '未见明显异常', doctor: '李医生' }
          ],
          treatmentPlan: '建议补充AREDS2配方营养素，保持健康饮食，多食用深绿色蔬菜和富含omega-3脂肪酸的食物。避免吸烟。',
          medications: [
            { name: 'AREDS2复合营养素', dosage: '每次1粒', frequency: '每日2次', duration: '长期服用' }
          ],
          followUp: '3个月后复查OCT和眼底检查，评估病情进展。'
        },
        {
          id: 5,
          patientName: '刘强',
          avatar: 'https://randomuser.me/api/portraits/men/42.jpg',
          time: '前天 15:30',
          type: '视力检查',
          status: 'normal',
          statusText: '正常',
          gender: '男',
          age: 35,
          contact: '137****2345',
          doctor: '张医生',
          equipment: 'VisioCheck Pro',
          confidence: 98,
          conclusion: '患者视力正常，双眼屈光度稳定。建议保持良好用眼习惯，避免长时间使用电子设备。',
          aiAnalysis: '视力检查结果为1.0，与上次检查结果一致。角膜地形图显示规则散光，度数稳定。眼压正常范围内。',
          metrics: [
            { name: '视力水平', value: 95 },
            { name: '屈光状态', value: 92 },
            { name: '眼表健康', value: 96 }
          ],
          images: [
            { 
              url: 'https://via.placeholder.com/150/FFFF00/000000?text=角膜地形图', 
              description: '角膜地形图：显示轻度规则散光，陡峭轴为100度，曲率为43.5D。' 
            },
            { 
              url: 'https://via.placeholder.com/150/FFFFFF/000000?text=眼表检查', 
              description: '眼表检查：显示眼表结构正常，泪膜稳定性良好，无干眼迹象。' 
            }
          ],
          history: [
            { date: '2023-02-10', title: '常规检查', description: '视力正常，轻度散光', doctor: '张医生' },
            { date: '2022-03-15', title: '配镜检查', description: '近视+散光，配镜矫正', doctor: '王医生' }
          ],
          treatmentPlan: '无需特殊治疗。建议使用防蓝光眼镜，每用眼1小时休息10分钟，保持充足睡眠。',
          medications: [],
          followUp: '建议一年后进行常规视力检查。'
        }
      ],
      showDiagnosisModal: false,
      selectedDiagnosis: {},
      diagnosisTabs: [
        { name: '诊断结果' },
        { name: '患者病史' },
        { name: '治疗方案' }
      ],
      activeTab: 0
    };
  },
  mounted() {
    this.fetchDoctorInfo();
    this.updateChartData();
    this.updatePieChartData();
  },
  methods: {
    // 获取医生信息
    fetchDoctorInfo() {
      // 从本地存储获取token和userId
      const infoStr = localStorage.getItem('info');
      if (!infoStr) {
        console.error('未找到用户信息');
        return;
      }
      
      try {
        const info = JSON.parse(infoStr);
        const token = info.token;
        const doctorId = info.userId || 1; // 默认使用1
        
        // 发送请求获取医生信息
        fetch('http://8.155.59.127:34561/user/getDoctorInfo/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'token': token
          },
          body: JSON.stringify({
            "doctor_id": doctorId
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.code === 200) {
            this.doctorInfo = data.data;
            console.log('医生信息获取成功:', this.doctorInfo);
            
            // 根据医生ID生成随机的统计数据
            this.generateRandomStats(doctorId);
          } else {
            console.error('获取医生信息失败:', data.msg);
          }
        })
        .catch(error => {
          console.error('请求出错:', error);
        });
      } catch (error) {
        console.error('解析用户信息出错:', error);
      }
    },
    
    // 根据医生ID生成随机统计数据
    generateRandomStats(doctorId) {
      // 使用医生ID作为随机种子，确保同一医生每次生成的数据相对稳定
      const seed = doctorId * 10;
      
      // 生成今日统计数据
      this.todayStats = {
        completed: Math.floor(Math.random() * 10) + seed % 10 + 5, // 5-24之间
        scheduled: Math.floor(Math.random() * 8) + seed % 5 + 3,   // 3-15之间
        urgent: Math.floor(Math.random() * 3) + seed % 2 + 1       // 1-5之间
      };
      
      // 更新其他统计数据
      this.stats = {
        patients: Math.floor(Math.random() * 100) + seed * 10 + 150,  // 150-350之间
        patientsTrend: Math.floor(Math.random() * 15) + 5,            // 5-20之间
        diagnoses: Math.floor(Math.random() * 50) + seed * 5 + 100,   // 100-200之间
        diagnosesTrend: Math.floor(Math.random() * 10) + 3,           // 3-13之间
        accuracy: (90 + Math.random() * 8).toFixed(1),                // 90-98之间
        accuracyTrend: (Math.random() * 3 + 0.5).toFixed(1),          // 0.5-3.5之间
        responseTime: (Math.random() * 2 + 0.5).toFixed(1),           // 0.5-2.5之间
        responseTimeTrend: (Math.random() * 0.8 + 0.2).toFixed(1)     // 0.2-1.0之间
      };
    },
    
    // 导航到诊断页面
    navigateToDiagnosis() {
      this.$router.push('/diagnosis');
    },
    
    // 导航到患者管理页面
    navigateToPatients() {
      this.$router.push('/patients');
    },
    
    // 显示统计卡片的提示框
    showTooltip(type) {
      this.activeTooltip = type;
    },
    hideTooltip() {
      this.activeTooltip = null;
    },
    
    // 更新趋势图数据
    updateChartData() {
      // 根据选择的时间段生成不同的随机数据
      let points = [];
      let labels = [];
      
      if (this.selectedPeriod === 'week') {
        // 周数据 - 7天
        points = this.generateRandomPoints(7);
        labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
      } else if (this.selectedPeriod === 'month') {
        // 月数据 - 4周
        points = this.generateRandomPoints(4);
        labels = ['第一周', '第二周', '第三周', '第四周'];
      } else if (this.selectedPeriod === 'quarter') {
        // 季度数据 - 3个月
        points = this.generateRandomPoints(3);
        labels = ['一月', '二月', '三月'];
      } else if (this.selectedPeriod === 'year') {
        // 年数据 - 12个月
        points = this.generateRandomPoints(12);
        labels = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
      }
      
      // 生成SVG路径
      const width = 600;
      const height = 250;
      const xStep = width / (points.length - 1);
      
      // 转换数据点为坐标
      const coordinates = points.map((value, index) => {
        // 将值映射到图表高度 (值越高，y坐标越小)
        const y = height - (value / 100 * height);
        return { x: index * xStep, y, value };
      });
      
      // 生成线条路径
      let linePath = `M${coordinates[0].x},${coordinates[0].y}`;
      for (let i = 1; i < coordinates.length; i++) {
        linePath += ` L${coordinates[i].x},${coordinates[i].y}`;
      }
      
      // 生成填充区域路径
      let areaPath = linePath + ` L${coordinates[coordinates.length-1].x},${height} L${coordinates[0].x},${height} Z`;
      
      // 更新图表数据
      this.chartData = {
        linePath,
        areaPath,
        points: coordinates,
        labels
      };
      
      // 添加动画效果
      this.$nextTick(() => {
        const lineElement = this.$refs.trendChart.querySelector('.chart-line');
        if (lineElement) {
          const length = lineElement.getTotalLength();
          lineElement.style.strokeDasharray = length;
          lineElement.style.strokeDashoffset = length;
          lineElement.style.animation = 'dash 1.5s ease-in-out forwards';
        }
      });
    },
    
    // 生成随机数据点
    generateRandomPoints(count) {
      const points = [];
      for (let i = 0; i < count; i++) {
        points.push(Math.floor(Math.random() * 60) + 20); // 20-80之间的随机值
      }
      return points;
    },
    
    // 显示数据点提示
    showDataTooltip(point, event) {
      const rect = event.target.getBoundingClientRect();
      this.dataTooltip = {
        visible: true,
        style: {
          left: `${rect.left}px`,
          top: `${rect.top - 80}px`
        },
        title: this.chartData.labels[this.chartData.points.indexOf(point)],
        value: point.value,
        trend: Math.floor(Math.random() * 20) - 5 // -5到15之间的随机值
      };
    },
    
    hideDataTooltip() {
      this.dataTooltip.visible = false;
    },
    
    // 更新饼图数据
    updatePieChartData() {
      // 根据选择的时间段生成不同的随机数据
      const categories = [
        { name: '视网膜病变', color: '#72b3e3', highlightColor: '#4299e1' },
        { name: '青光眼', color: '#48bb78', highlightColor: '#38a169' },
        { name: '白内障', color: '#ed8936', highlightColor: '#dd6b20' },
        { name: '黄斑变性', color: '#9f7aea', highlightColor: '#805ad5' },
        { name: '其他', color: '#68d391', highlightColor: '#48bb78' }
      ];
      
      // 生成随机数据
      let total = 0;
      const data = categories.map(category => {
        const value = Math.floor(Math.random() * 50) + 10; // 10-60之间的随机值
        total += value;
        return { ...category, value };
      });
      
      // 计算百分比
      data.forEach(item => {
        item.percentage = Math.round((item.value / total) * 100);
      });
      
      // 生成饼图切片
      const slices = [];
      let startAngle = 0;
      
      data.forEach(item => {
        const angle = (item.percentage / 100) * Math.PI * 2;
        const endAngle = startAngle + angle;
        
        // 计算路径
        const x1 = Math.cos(startAngle) * 100;
        const y1 = Math.sin(startAngle) * 100;
        const x2 = Math.cos(endAngle) * 100;
        const y2 = Math.sin(endAngle) * 100;
        
        // 大弧标志
        const largeArcFlag = angle > Math.PI ? 1 : 0;
        
        // 生成路径
        const path = `M0,0 L${x1},${y1} A100,100 0 ${largeArcFlag},1 ${x2},${y2} Z`;
        
        // 计算提示框位置 - 在切片中间位置
        const midAngle = startAngle + (angle / 2);
        // 提示框位置稍微偏离圆心，但不会太远
        const tooltipX = Math.cos(midAngle) * 60;
        const tooltipY = Math.sin(midAngle) * 60;
        
        slices.push({
          path,
          color: item.color,
          highlightColor: item.highlightColor,
          name: item.name,
          value: item.value,
          percentage: item.percentage,
          trend: Math.floor(Math.random() * 20) - 5, // -5到15之间的随机值
          tooltipX,
          tooltipY
        });
        
        startAngle = endAngle;
      });
      
      // 更新饼图数据
      this.pieChartData = {
        slices,
        legend: data,
        total: total
      };
    },
    
    // 高亮饼图切片
    highlightSlice(index, event, isFromPie) {
      this.activeSlice = index;
      
      // 显示提示框
      this.pieTooltip = {
        visible: true,
        index: index,
        name: this.pieChartData.slices[index].name,
        value: this.pieChartData.slices[index].value,
        percentage: this.pieChartData.slices[index].percentage,
        trend: this.pieChartData.slices[index].trend
      };
    },
    
    resetSlice() {
      this.activeSlice = null;
      this.pieTooltip.visible = false;
    },
    
    // 打开诊断详情弹窗
    openDiagnosisDetails(diagnosis) {
      this.selectedDiagnosis = diagnosis;
      this.showDiagnosisModal = true;
      this.activeTab = 0; // 默认显示第一个标签页
      
      // 防止页面滚动
      document.body.style.overflow = 'hidden';
    },
    
    // 关闭诊断详情弹窗
    closeDiagnosisModal() {
      this.showDiagnosisModal = false;
      
      // 恢复页面滚动
      document.body.style.overflow = 'auto';
    },
    
    // 获取置信度样式类
    getConfidenceClass(confidence) {
      if (confidence >= 90) return 'high';
      if (confidence >= 70) return 'medium';
      return 'low';
    },
    
    // 获取指标颜色
    getMetricColor(value) {
      if (value >= 90) return '#48bb78';
      if (value >= 70) return '#ecc94b';
      return '#f56565';
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 24px;
  background-color: #f8fafc;
  position: relative;
}


.breadcrumb {
  display: flex;
  align-items: center;
  margin-top: 8px;
}

.breadcrumb svg {
  margin: 0 8px;
}

.breadcrumb span {
  font-size: 14px;
  color: #718096;
}

/* 欢迎卡片 */
.welcome-card {
  background: linear-gradient(135deg, #72b3e3, #b0d3f1);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 10px 15px -3px rgba(114, 179, 227, 0.2);
  position: relative;
  overflow: hidden;
}

.welcome-card::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.welcome-text h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.welcome-text p {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 20px;
}

.welcome-stats {
  display: flex;
  gap: 20px;
  margin-top: 16px;
}

.welcome-stat {
  background: rgba(255, 255, 255, 0.2);
  padding: 10px 16px;
  border-radius: 8px;
  text-align: center;
}

.welcome-stat-value {
  font-size: 20px;
  font-weight: 600;
}

.welcome-stat-label {
  font-size: 12px;
  opacity: 0.8;
}

.welcome-actions {
  display: flex;
  gap: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.action-button.primary {
  background: white;
  color: #72b3e3;
}

.action-button.primary:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

.action-button.secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.action-button.secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* 眼睛装饰 */
.eye-decoration {
  position: absolute;
  right: 5%;
  top: 20%;
  opacity: 0.1;
  width: 100px;
  height: 100px;
}

/* 数据概览卡片 */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  position: relative;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: white;
}

.stat-icon.blue {
  background: linear-gradient(135deg, #63b3ed, #4299e1);
}

.stat-icon.green {
  background: linear-gradient(135deg, #68d391, #48bb78);
}

.stat-icon.purple {
  background: linear-gradient(135deg, #b794f4, #805ad5);
}

.stat-icon.orange {
  background: linear-gradient(135deg, #fbd38d, #ed8936);
}

.stat-details {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #718096;
  margin-bottom: 8px;
}

.stat-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 500;
}

.stat-trend.up {
  color: #48bb78;
}

.stat-trend.down {
  color: #f56565;
}

.stat-trend svg {
  margin-right: 4px;
}

/* 统计卡片提示框 */
.stat-tooltip {
  position: absolute;
  top: -120px;
  left: 0;
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 200px;
  z-index: 10;
  animation: fadeIn 0.2s ease-in-out;
}

.stat-tooltip::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 20px;
  width: 16px;
  height: 16px;
  background: white;
  transform: rotate(45deg);
  box-shadow: 4px 4px 5px -2px rgba(0, 0, 0, 0.1);
}

.tooltip-title {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #4a5568;
  margin-bottom: 4px;
}

/* 图表区域 */
.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: relative;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
}

.chart-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.period-select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: white;
  font-size: 14px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s;
}

.period-select:focus {
  outline: none;
  border-color: #72b3e3;
  box-shadow: 0 0 0 3px rgba(114, 179, 227, 0.2);
}

.chart-body {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  position: relative;
}

/* 数据点提示框 */
.data-tooltip {
  position: absolute;
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 150px;
  z-index: 10;
  animation: fadeIn 0.2s ease-in-out;
}

.data-tooltip-title {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
}

.data-tooltip-value {
  font-size: 12px;
  color: #4a5568;
  margin-bottom: 4px;
}

.data-tooltip-info {
  font-size: 12px;
  color: #4a5568;
}

/* 饼图提示框 */
.pie-tooltip {
  position: absolute;
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 150px;
  z-index: 10;
  animation: fadeIn 0.2s ease-in-out;
}

.pie-tooltip-title {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
}

.pie-tooltip-value {
  font-size: 12px;
  color: #4a5568;
  margin-bottom: 4px;
}

.pie-tooltip-info {
  font-size: 12px;
  color: #4a5568;
}

.trend-up {
  color: #48bb78;
}

.trend-down {
  color: #f56565;
}

/* 医生工作量统计 */
.doctor-workload {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.workload-bars {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.workload-item {
  display: flex;
  align-items: center;
}

.doctor-info {
  display: flex;
  align-items: center;
  width: 120px;
  margin-right: 16px;
}

.doctor-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 8px;
}

.doctor-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.doctor-name {
  font-size: 14px;
  color: #4a5568;
}

.workload-bar-container {
  flex: 1;
  height: 24px;
  background: #edf2f7;
  border-radius: 12px;
  overflow: hidden;
}

.workload-bar {
  height: 100%;
  background: linear-gradient(90deg, #72b3e3, #b0d3f1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 12px;
  transition: width 1s ease-in-out;
}

.workload-value {
  font-size: 12px;
  color: white;
  font-weight: 500;
}

/* 近期诊断列表 */
.recent-diagnoses {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
}

.view-all-btn {
  padding: 6px 12px;
  border-radius: 6px;
  background: rgba(114, 179, 227, 0.1);
  color: #72b3e3;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background: rgba(114, 179, 227, 0.2);
}

.diagnoses-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.diagnosis-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  background: #f8fafc;
  transition: all 0.2s;
  cursor: pointer;
}

.diagnosis-item:hover {
  background: #edf2f7;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.diagnosis-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 12px;
}

.diagnosis-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.diagnosis-details {
  flex: 1;
}

.diagnosis-patient-name {
  font-size: 14px;
  font-weight: 500;
  color: #2d3748;
}

.diagnosis-time {
  font-size: 12px;
  color: #718096;
  margin-bottom: 4px;
}

.diagnosis-type {
  font-size: 12px;
  color: #4a5568;
  margin-bottom: 4px;
}

.diagnosis-status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.diagnosis-status.normal {
  background: rgba(72, 187, 120, 0.1);
  color: #48bb78;
}

.diagnosis-status.abnormal {
  background: rgba(245, 101, 101, 0.1);
  color: #f56565;
}

.diagnosis-status.warning {
  background: rgba(237, 137, 54, 0.1);
  color: #ed8936;
}

.diagnosis-action {
  margin-left: 12px;
}

.view-diagnosis-btn {
  padding: 6px 12px;
  border-radius: 6px;
  background: linear-gradient(135deg, #72b3e3, #b0d3f1);
  color: white;
  font-size: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.view-diagnosis-btn:hover {
  background: linear-gradient(135deg, #63b3ed, #90c5f0);
}

/* 饼图交互效果 */
.pie-tooltip-svg {
  filter: drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.1));
  pointer-events: none;
  animation: fadeIn 0.2s ease-in-out;
}

/* 饼图交互效果 */
.pie-slice {
  cursor: pointer;
  transition: all 0.3s ease;
}

.pie-slice.active-slice {
  filter: drop-shadow(0px 0px 8px rgba(0, 0, 0, 0.3));
}

.legend-item {
  cursor: pointer;
  transition: all 0.2s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 诊断详情弹窗 */
.diagnosis-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  animation: fadeIn 0.3s ease;
}

.diagnosis-modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s ease;
}

.diagnosis-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.diagnosis-modal-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
}

.close-modal-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #718096;
  transition: all 0.2s;
}

.close-modal-btn:hover {
  color: #2d3748;
}

.diagnosis-modal-body {
  padding: 20px;
}

.patient-info-section {
  margin-bottom: 24px;
}

.patient-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.patient-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 16px;
}

.patient-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.patient-basic-info {
  flex: 1;
}

.patient-basic-info h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 4px;
}

.patient-id {
  font-size: 14px;
  color: #718096;
  margin-bottom: 4px;
}

.patient-details {
  font-size: 14px;
  color: #4a5568;
}

.patient-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.diagnosis-info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 20px;
}

.info-card {
  background: #f8fafc;
  border-radius: 8px;
  padding: 12px;
}

.info-card-label {
  font-size: 12px;
  color: #718096;
  margin-bottom: 4px;
}

.info-card-value {
  font-size: 14px;
  font-weight: 500;
  color: #2d3748;
}

.diagnosis-tabs {
  margin-top: 24px;
}

.tab-header {
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 20px;
}

.tab-item {
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 500;
  color: #718096;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
}

.tab-item.active {
  color: #72b3e3;
  border-bottom: 2px solid #72b3e3;
}

.tab-content {
  min-height: 300px;
}

.diagnosis-result {
  padding: 16px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.result-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
}

.confidence-level {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.confidence-level.high {
  background: rgba(72, 187, 120, 0.1);
  color: #48bb78;
}

.confidence-level.medium {
  background: rgba(237, 137, 54, 0.1);
  color: #ed8936;
}

.confidence-level.low {
  background: rgba(245, 101, 101, 0.1);
  color: #f56565;
}

.result-content {
  margin-bottom: 20px;
}

.result-content p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
}

.result-images {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.result-image-container {
  width: calc(50% - 8px);
}

.result-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 8px;
}

.image-description {
  font-size: 12px;
  color: #718096;
  text-align: center;
}

.ai-analysis {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  margin-top: 20px;
}

.ai-analysis h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 12px;
}

.analysis-content p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 16px;
}

.analysis-metrics {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.metric {
  display: flex;
  align-items: center;
  gap: 12px;
}

.metric-name {
  width: 120px;
  font-size: 14px;
  color: #4a5568;
}

.metric-bar-container {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.metric-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease-in-out;
}

.metric-value {
  width: 40px;
  font-size: 14px;
  font-weight: 500;
  color: #2d3748;
  text-align: right;
}

.patient-history {
  padding: 16px;
}

.history-timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.timeline-item {
  display: flex;
  position: relative;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 80px;
  top: 24px;
  bottom: -24px;
  width: 2px;
  background: #e2e8f0;
}

.timeline-item:last-child::before {
  display: none;
}

.timeline-date {
  width: 80px;
  font-size: 14px;
  color: #718096;
  padding-right: 20px;
}

.timeline-content {
  flex: 1;
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  position: relative;
}

.timeline-content::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 16px;
  width: 16px;
  height: 16px;
  background: #f8fafc;
  transform: rotate(45deg);
  border-radius: 2px;
}

.timeline-title {
  font-size: 14px;
  font-weight: 500;
  color: #2d3748;
  margin-bottom: 8px;
}

.timeline-description {
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 8px;
}

.timeline-doctor {
  font-size: 12px;
  color: #718096;
}

.treatment-plan {
  padding: 16px;
}

.plan-section {
  margin-bottom: 24px;
}

.plan-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 12px;
}

.plan-section p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
}

.medication-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.medication-item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 12px;
  background: #f8fafc;
  border-radius: 8px;
  padding: 12px;
}

.medication-name {
  font-size: 14px;
  font-weight: 500;
  color: #2d3748;
}

.medication-dosage, .medication-frequency, .medication-duration {
  font-size: 14px;
  color: #4a5568;
}

.diagnosis-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.action-btn.print {
  background: #f8fafc;
  color: #4a5568;
}

.action-btn.share {
  background: #f8fafc;
  color: #4a5568;
}

.action-btn.edit {
  background: #f8fafc;
  color: #4a5568;
}

.action-btn.primary {
  background: linear-gradient(135deg, #72b3e3, #b0d3f1);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
}

/* 动画 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes dash {
  to { stroke-dashoffset: 0; }
}

.data-point {
  cursor: pointer;
  transition: r 0.2s;
}

.data-point:hover {
  r: 8;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .diagnosis-info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .welcome-card {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .welcome-actions {
    margin-top: 16px;
  }
  
  .result-image-container {
    width: 100%;
  }
  
  .medication-item {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}

@media (max-width: 576px) {
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .diagnosis-info-grid {
    grid-template-columns: 1fr;
  }
  
  .diagnosis-actions {
    flex-wrap: wrap;
  }
  
  .action-btn {
    flex: 1;
    justify-content: center;
  }
}
</style>
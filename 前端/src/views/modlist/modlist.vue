<template>
  <div class="diagnostic-page">
    <div class="section">
      <div class="section-header">
        <h2>模型诊断效果分析</h2>
        <div class="date-filter">
          <span>时间范围：</span>
          <select v-model="timeRange" @change="updateChartData" class="select-control">
            <option value="7">最近7天</option>
            <option value="14">最近14天</option>
            <option value="30">最近30天</option>
            <option value="90">最近90天</option>
          </select>
        </div>
      </div>

      <!-- 性能指标卡片 -->
      <div class="metrics-cards">
        <div class="metric-card">
          <div class="metric-icon accuracy">
            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <div class="metric-details">
            <h3>准确率 (Accuracy)</h3>
            <div class="metric-value">{{ currentMetrics.accuracy }}</div>
            <div class="metric-trend" :class="getTrendClass(accuracyTrend)">
              <svg v-if="accuracyTrend > 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="18 15 12 9 6 15"></polyline>
              </svg>
              <svg v-else-if="accuracyTrend < 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
              <span>{{ Math.abs(accuracyTrend).toFixed(2) }}%</span>
            </div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon recall">
            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </div>
          <div class="metric-details">
            <h3>召回率 (Recall)</h3>
            <div class="metric-value">{{ currentMetrics.recall }}</div>
            <div class="metric-trend" :class="getTrendClass(recallTrend)">
              <svg v-if="recallTrend > 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="18 15 12 9 6 15"></polyline>
              </svg>
              <svg v-else-if="recallTrend < 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
              <span>{{ Math.abs(recallTrend).toFixed(2) }}%</span>
            </div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon f1-score">
            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9"></path>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
          </div>
          <div class="metric-details">
            <h3>F1 值 (F1 Score)</h3>
            <div class="metric-value">{{ currentMetrics.f1Score }}</div>
            <div class="metric-trend" :class="getTrendClass(f1Trend)">
              <svg v-if="f1Trend > 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="18 15 12 9 6 15"></polyline>
              </svg>
              <svg v-else-if="f1Trend < 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
              <span>{{ Math.abs(f1Trend).toFixed(2) }}%</span>
            </div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon anomaly">
            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </div>
          <div class="metric-details">
            <h3>异常值 (Anomaly)</h3>
            <div class="metric-value">{{ currentMetrics.anomaly }}</div>
            <div class="metric-trend" :class="getTrendClass(-anomalyTrend)">
              <svg v-if="anomalyTrend < 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="18 15 12 9 6 15"></polyline>
              </svg>
              <svg v-else-if="anomalyTrend > 0" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
              <span>{{ Math.abs(anomalyTrend).toFixed(2) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 性能指标趋势图 -->
      <div class="chart-container">
        <div class="chart-header">
          <h3>模型性能趋势</h3>
          <div class="chart-legend">
            <div class="legend-item">
              <span class="legend-color accuracy"></span>
              <span>准确率 (Accuracy)</span>
            </div>
            <div class="legend-item">
              <span class="legend-color recall"></span>
              <span>召回率 (Recall)</span>
            </div>
            <div class="legend-item">
              <span class="legend-color f1-score"></span>
              <span>F1 值 (F1 Score)</span>
            </div>
            <div class="legend-item">
              <span class="legend-color anomaly"></span>
              <span>异常值 (Anomaly)</span>
            </div>
          </div>
        </div>
        <div class="chart" ref="performanceChart"></div>
        <!-- 添加图表提示框 -->
        <div class="chart-tooltip" ref="chartTooltip" v-show="showTooltip">
          <div class="tooltip-date">{{ tooltipData.date }}</div>
          <div class="tooltip-item" v-for="(value, key) in tooltipData.values" :key="key">
            <span class="tooltip-color" :class="key"></span>
            <span class="tooltip-label">{{ getMetricLabel(key) }}:</span>
            <span class="tooltip-value">{{ (value * 100).toFixed(2) }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 疾病诊断混淆矩阵 -->
    <div class="section">
      <div class="section-header">
        <h2>疾病诊断混淆矩阵</h2>
        <div class="filter-container">
          <div class="disease-filter">
            <select v-model="selectedDisease" class="select-control">
              <option value="all">所有疾病</option>
              <option v-for="disease in diseases" :key="disease.id" :value="disease.id">
                {{ disease.name }}
              </option>
            </select>
          </div>
          <div class="date-range-filter">
            <span>时间范围：</span>
            <select v-model="matrixTimeRange" @change="updateMatrixData" class="select-control">
              <option value="7">最近7天</option>
              <option value="14">最近14天</option>
              <option value="30">最近30天</option>
              <option value="90">最近90天</option>
            </select>
          </div>
        </div>
      </div>

      <div class="table-wrapper">
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>疾病类型</th>
                <th>真阳性 (TP)</th>
                <th>假阳性 (FP)</th>
                <th>真阴性 (TN)</th>
                <th>假阴性 (FN)</th>
                <th>准确率</th>
                <th>召回率</th>
                <th>F1 值</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="disease in filteredDiseases" :key="disease.id">
                <td>{{ disease.name }}</td>
                <td>{{ disease.tp }}</td>
                <td>{{ disease.fp }}</td>
                <td>{{ disease.tn }}</td>
                <td>{{ disease.fn }}</td>
                <td :class="getAccuracyClass(disease.accuracy)">{{ (disease.accuracy * 100).toFixed(2) }}%</td>
                <td :class="getRecallClass(disease.recall)">{{ (disease.recall * 100).toFixed(2) }}%</td>
                <td :class="getF1Class(disease.f1Score)">{{ (disease.f1Score * 100).toFixed(2) }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 混淆矩阵可视化 -->
      <div class="confusion-matrix-container" v-if="selectedDisease !== 'all'">
        <h3>{{ getSelectedDiseaseName() }} 混淆矩阵可视化</h3>
        <div class="confusion-matrix">
          <div class="matrix-row">
            <div class="matrix-cell header"></div>
            <div class="matrix-cell header">预测阳性</div>
            <div class="matrix-cell header">预测阴性</div>
          </div>
          <div class="matrix-row">
            <div class="matrix-cell header">实际阳性</div>
            <div class="matrix-cell tp">
              <div class="cell-value">{{ getSelectedDiseaseData().tp }}</div>
              <div class="cell-label">真阳性 (TP)</div>
            </div>
            <div class="matrix-cell fn">
              <div class="cell-value">{{ getSelectedDiseaseData().fn }}</div>
              <div class="cell-label">假阴性 (FN)</div>
            </div>
          </div>
          <div class="matrix-row">
            <div class="matrix-cell header">实际阴性</div>
            <div class="matrix-cell fp">
              <div class="cell-value">{{ getSelectedDiseaseData().fp }}</div>
              <div class="cell-label">假阳性 (FP)</div>
            </div>
            <div class="matrix-cell tn">
              <div class="cell-value">{{ getSelectedDiseaseData().tn }}</div>
              <div class="cell-label">真阴性 (TN)</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 新增：疾病诊断历史趋势 -->
      <div class="disease-trend-container" v-if="selectedDisease !== 'all'">
        <h3>{{ getSelectedDiseaseName() }} 诊断准确率历史趋势</h3>
        <div class="disease-trend-chart" ref="diseaseTrendChart"></div>
      </div>
    </div>
    
    <!-- 新增：模型诊断建议 -->
    <div class="section">
      <div class="section-header">
        <h2>模型诊断建议</h2>
      </div>
      <div class="recommendations">
        <div class="recommendation-card" v-for="(rec, index) in recommendations" :key="index">
          <div class="recommendation-icon" :class="rec.type">
            <svg v-if="rec.type === 'warning'" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <svg v-else-if="rec.type === 'info'" viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <svg v-else viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <div class="recommendation-content">
            <h4>{{ rec.title }}</h4>
            <p>{{ rec.description }}</p>
            <div class="recommendation-actions" v-if="rec.actions && rec.actions.length">
              <button v-for="(action, actionIndex) in rec.actions" :key="actionIndex" class="action-button">
                {{ action }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelDiagnosticPage',
  data() {
    return {
      timeRange: '7',
      matrixTimeRange: '7',
      selectedDate: new Date(),
      selectedDisease: 'all',
      chart: null,
      diseaseTrendChart: null,
      currentMetrics: {
        accuracy: '0.92',
        recall: '0.87',
        f1Score: '0.89',
        anomaly: '0.03'
      },
      accuracyTrend: 2.5,
      recallTrend: -1.2,
      f1Trend: 0.8,
      anomalyTrend: -0.5,
      // 扩展数据集以支持不同的时间范围
      allPerformanceData: [
        { date: '2025-01-01', accuracy: 0.88, recall: 0.83, f1Score: 0.85, anomaly: 0.04 },
        { date: '2025-01-15', accuracy: 0.89, recall: 0.84, f1Score: 0.86, anomaly: 0.04 },
        { date: '2025-01-30', accuracy: 0.90, recall: 0.85, f1Score: 0.87, anomaly: 0.03 },
        { date: '2025-02-15', accuracy: 0.89, recall: 0.84, f1Score: 0.86, anomaly: 0.04 },
        { date: '2025-02-28', accuracy: 0.91, recall: 0.86, f1Score: 0.88, anomaly: 0.03 },
        { date: '2025-03-10', accuracy: 0.90, recall: 0.85, f1Score: 0.87, anomaly: 0.03 },
        { date: '2025-03-20', accuracy: 0.91, recall: 0.86, f1Score: 0.88, anomaly: 0.03 },
        { date: '2025-03-28', accuracy: 0.91, recall: 0.88, f1Score: 0.90, anomaly: 0.02 },
        { date: '2025-03-29', accuracy: 0.92, recall: 0.89, f1Score: 0.91, anomaly: 0.02 },
        { date: '2025-03-30', accuracy: 0.90, recall: 0.87, f1Score: 0.89, anomaly: 0.03 },
        { date: '2025-03-31', accuracy: 0.93, recall: 0.90, f1Score: 0.91, anomaly: 0.02 },
        { date: '2025-04-01', accuracy: 0.89, recall: 0.82, f1Score: 0.85, anomaly: 0.04 },
        { date: '2025-04-02', accuracy: 0.92, recall: 0.87, f1Score: 0.89, anomaly: 0.03 },
        { date: '2025-04-03', accuracy: 0.93, recall: 0.89, f1Score: 0.91, anomaly: 0.02 },
        { date: '2025-04-04', accuracy: 0.94, recall: 0.90, f1Score: 0.92, anomaly: 0.02 }
      ],
      performanceData: [], // 将根据时间范围筛选
      // 疾病数据集，按时间范围存储
      allDiseaseData: {
        '7': [
          {
            id: 1,
            name: '青光眼',
            tp: 124,
            fp: 8,
            tn: 452,
            fn: 6,
            accuracy: 0.97,
            recall: 0.95,
            f1Score: 0.96
          },
          {
            id: 2,
            name: '白内障',
            tp: 98,
            fp: 5,
            tn: 478,
            fn: 9,
            accuracy: 0.96,
            recall: 0.92,
            f1Score: 0.94
          },
          {
            id: 3,
            name: '糖尿病视网膜病变',
            tp: 87,
            fp: 12,
            tn: 465,
            fn: 16,
            accuracy: 0.94,
            recall: 0.84,
            f1Score: 0.89
          },
          {
            id: 4,
            name: '黄斑变性',
            tp: 76,
            fp: 10,
            tn: 470,
            fn: 14,
            accuracy: 0.95,
            recall: 0.84,
            f1Score: 0.89
          },
          {
            id: 5,
            name: '视网膜脱离',
            tp: 45,
            fp: 7,
            tn: 510,
            fn: 8,
            accuracy: 0.97,
            recall: 0.85,
            f1Score: 0.90
          }
        ],
        '14': [
          {
            id: 1,
            name: '青光眼',
            tp: 235,
            fp: 18,
            tn: 892,
            fn: 15,
            accuracy: 0.96,
            recall: 0.94,
            f1Score: 0.95
          },
          {
            id: 2,
            name: '白内障',
            tp: 187,
            fp: 12,
            tn: 945,
            fn: 16,
            accuracy: 0.97,
            recall: 0.92,
            f1Score: 0.94
          },
          {
            id: 3,
            name: '糖尿病视网膜病变',
            tp: 165,
            fp: 25,
            tn: 920,
            fn: 30,
            accuracy: 0.95,
            recall: 0.85,
            f1Score: 0.90
          },
          {
            id: 4,
            name: '黄斑变性',
            tp: 142,
            fp: 18,
            tn: 940,
            fn: 30,
            accuracy: 0.96,
            recall: 0.83,
            f1Score: 0.89
          },
          {
            id: 5,
            name: '视网膜脱离',
            tp: 85,
            fp: 14,
            tn: 1020,
            fn: 21,
            accuracy: 0.97,
            recall: 0.80,
            f1Score: 0.88
          }
        ],
        '30': [
          {
            id: 1,
            name: '青光眼',
            tp: 485,
            fp: 42,
            tn: 1820,
            fn: 33,
            accuracy: 0.96,
            recall: 0.94,
            f1Score: 0.95
          },
          {
            id: 2,
            name: '白内障',
            tp: 392,
            fp: 28,
            tn: 1950,
            fn: 30,
            accuracy: 0.97,
            recall: 0.93,
            f1Score: 0.95
          },
          {
            id: 3,
            name: '糖尿病视网膜病变',
            tp: 345,
            fp: 58,
            tn: 1880,
            fn: 67,
            accuracy: 0.94,
            recall: 0.84,
            f1Score: 0.89
          },
          {
            id: 4,
            name: '黄斑变性',
            tp: 298,
            fp: 45,
            tn: 1920,
            fn: 57,
            accuracy: 0.95,
            recall: 0.84,
            f1Score: 0.89
          },
          {
            id: 5,
            name: '视网膜脱离',
            tp: 175,
            fp: 32,
            tn: 2080,
            fn: 43,
            accuracy: 0.96,
            recall: 0.80,
            f1Score: 0.87
          }
        ],
        '90': [
          {
            id: 1,
            name: '青光眼',
            tp: 1250,
            fp: 120,
            tn: 5430,
            fn: 100,
            accuracy: 0.96,
            recall: 0.93,
            f1Score: 0.94
          },
          {
            id: 2,
            name: '白内障',
            tp: 1080,
            fp: 85,
            tn: 5820,
            fn: 95,
            accuracy: 0.97,
            recall: 0.92,
            f1Score: 0.94
          },
          {
            id: 3,
            name: '糖尿病视网膜病变',
            tp: 950,
            fp: 175,
            tn: 5600,
            fn: 195,
            accuracy: 0.94,
            recall: 0.83,
            f1Score: 0.88
          },
          {
            id: 4,
            name: '黄斑变性',
            tp: 820,
            fp: 140,
            tn: 5750,
            fn: 170,
            accuracy: 0.95,
            recall: 0.83,
            f1Score: 0.88
          },
          {
            id: 5,
            name: '视网膜脱离',
            tp: 480,
            fp: 95,
            tn: 6200,
            fn: 125,
            accuracy: 0.97,
            recall: 0.79,
            f1Score: 0.87
          }
        ]
      },
      diseases: [], // 将根据时间范围筛选
      // 添加Canvas绘图相关变量
      canvas: null,
      ctx: null,
      chartWidth: 0,
      chartHeight: 0,
      chartPadding: { top: 20, right: 30, bottom: 40, left: 50 },
      // 添加图表提示框相关变量
      showTooltip: false,
      tooltipData: {
        date: '',
        values: {}
      },
      mousePosition: { x: 0, y: 0 },
      // 添加疾病趋势数据
      diseaseTrendData: {
        1: [
          { date: '2025-03-01', accuracy: 0.95, recall: 0.92, f1Score: 0.93 },
          { date: '2025-03-15', accuracy: 0.96, recall: 0.93, f1Score: 0.94 },
          { date: '2025-03-29', accuracy: 0.97, recall: 0.95, f1Score: 0.96 },
          { date: '2025-04-01', accuracy: 0.96, recall: 0.94, f1Score: 0.95 },
          { date: '2025-04-04', accuracy: 0.97, recall: 0.95, f1Score: 0.96 }
        ],
        2: [
          { date: '2025-03-01', accuracy: 0.94, recall: 0.90, f1Score: 0.92 },
          { date: '2025-03-15', accuracy: 0.95, recall: 0.91, f1Score: 0.93 },
          { date: '2025-03-29', accuracy: 0.96, recall: 0.92, f1Score: 0.94 },
          { date: '2025-04-01', accuracy: 0.95, recall: 0.91, f1Score: 0.93 },
          { date: '2025-04-04', accuracy: 0.96, recall: 0.92, f1Score: 0.94 }
        ],
        3: [
          { date: '2025-03-01', accuracy: 0.92, recall: 0.82, f1Score: 0.87 },
          { date: '2025-03-15', accuracy: 0.93, recall: 0.83, f1Score: 0.88 },
          { date: '2025-03-29', accuracy: 0.94, recall: 0.84, f1Score: 0.89 },
          { date: '2025-04-01', accuracy: 0.93, recall: 0.83, f1Score: 0.88 },
          { date: '2025-04-04', accuracy: 0.94, recall: 0.84, f1Score: 0.89 }
        ],
        4: [
          { date: '2025-03-01', accuracy: 0.93, recall: 0.82, f1Score: 0.87 },
          { date: '2025-03-15', accuracy: 0.94, recall: 0.83, f1Score: 0.88 },
          { date: '2025-03-29', accuracy: 0.95, recall: 0.84, f1Score: 0.89 },
          { date: '2025-04-01', accuracy: 0.94, recall: 0.83, f1Score: 0.88 },
          { date: '2025-04-04', accuracy: 0.95, recall: 0.84, f1Score: 0.89 }
        ],
        5: [
          { date: '2025-03-01', accuracy: 0.95, recall: 0.78, f1Score: 0.86 },
          { date: '2025-03-15', accuracy: 0.96, recall: 0.79, f1Score: 0.87 },
          { date: '2025-03-29', accuracy: 0.97, recall: 0.80, f1Score: 0.88 },
          { date: '2025-04-01', accuracy: 0.96, recall: 0.79, f1Score: 0.87 },
          { date: '2025-04-04', accuracy: 0.97, recall: 0.80, f1Score: 0.88 }
        ]
      },
      // 添加模型诊断建议
      recommendations: [
        {
          type: 'warning',
          title: '糖尿病视网膜病变召回率偏低',
          description: '当前模型对糖尿病视网膜病变的召回率为84%，低于其他疾病。建议增加此类疾病的训练样本，特别是假阴性案例。',
          actions: ['查看详情', '调整模型']
        },
        {
          type: 'info',
          title: '视网膜脱离样本数量不足',
          description: '视网膜脱离的样本数量明显少于其他疾病类型，可能影响模型对该疾病的诊断能力。建议增加此类样本的收集。',
          actions: ['查看样本统计']
        },
        {
          type: 'success',
          title: '青光眼诊断效果优异',
          description: '模型对青光眼的诊断准确率和召回率均达到95%以上，表现优异。可以考虑将此部分模型架构应用到其他疾病诊断中。',
          actions: ['查看模型结构']
        }
      ]
    };
  },
  computed: {
    isToday() {
      const today = new Date();
      return (
        this.selectedDate.getDate() === today.getDate() &&
        this.selectedDate.getMonth() === today.getMonth() &&
        this.selectedDate.getFullYear() === today.getFullYear()
      );
    },
    filteredDiseases() {
      if (this.selectedDisease === 'all') {
        return this.diseases;
      } else {
        return this.diseases.filter(disease => disease.id === parseInt(this.selectedDisease));
      }
    }
  },
  mounted() {
    this.updateChartData();
    this.updateMatrixData();
    window.addEventListener('resize', this.handleResize);
    
    // 添加鼠标移动监听，用于图表提示框
    if (this.$refs.performanceChart) {
      this.$refs.performanceChart.addEventListener('mousemove', this.handleChartMouseMove);
      this.$refs.performanceChart.addEventListener('mouseout', this.handleChartMouseOut);
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    
    // 移除鼠标事件监听
    if (this.$refs.performanceChart) {
      this.$refs.performanceChart.removeEventListener('mousemove', this.handleChartMouseMove);
      this.$refs.performanceChart.removeEventListener('mouseout', this.handleChartMouseOut);
    }
  },
  watch: {
    selectedDisease(newValue) {
      if (newValue !== 'all') {
        this.$nextTick(() => {
          this.initDiseaseTrendChart();
        });
      }
    }
  },
  methods: {
    updateChartData() {
      // 根据选择的时间范围筛选数据
      const days = parseInt(this.timeRange);
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(endDate.getDate() - days);
      
      // 筛选数据
      this.performanceData = this.allPerformanceData.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate >= startDate && itemDate <= endDate;
      });
      
      // 如果数据点不足，生成一些模拟数据
      if (this.performanceData.length < days) {
        const existingDates = this.performanceData.map(item => item.date);
        for (let i = 0; i < days; i++) {
          const date = new Date(endDate);
          date.setDate(endDate.getDate() - i);
          const dateStr = this.formatDate(date);
          
          if (!existingDates.includes(dateStr)) {
            // 生成随机数据，但保持在合理范围内
            this.performanceData.push({
              date: dateStr,
              accuracy: 0.85 + Math.random() * 0.1,
              recall: 0.8 + Math.random() * 0.15,
              f1Score: 0.82 + Math.random() * 0.13,
              anomaly: 0.01 + Math.random() * 0.04
            });
          }
        }
        
        // 按日期排序
        this.performanceData.sort((a, b) => new Date(a.date) - new Date(b.date));
      }
      
      // 更新当前指标为最新数据
      if (this.performanceData.length > 0) {
        const latestData = this.performanceData[this.performanceData.length - 1];
        this.currentMetrics = {
          accuracy: latestData.accuracy.toFixed(2),
          recall: latestData.recall.toFixed(2),
          f1Score: latestData.f1Score.toFixed(2),
          anomaly: latestData.anomaly.toFixed(2)
        };
        
        // 计算趋势（与前一天相比）
        if (this.performanceData.length > 1) {
          const previousData = this.performanceData[this.performanceData.length - 2];
          this.accuracyTrend = (latestData.accuracy - previousData.accuracy) * 100;
          this.recallTrend = (latestData.recall - previousData.recall) * 100;
          this.f1Trend = (latestData.f1Score - previousData.f1Score) * 100;
          this.anomalyTrend = (latestData.anomaly - previousData.anomaly) * 100;
        }
      }
      
      // 初始化或更新图表
      this.$nextTick(() => {
        this.initChart();
      });
    },
    
    updateMatrixData() {
      // 根据选择的时间范围更新疾病数据
      this.diseases = this.allDiseaseData[this.matrixTimeRange] || [];
      
      // 如果当前选择了特定疾病，更新疾病趋势图
      if (this.selectedDisease !== 'all') {
        this.$nextTick(() => {
          this.initDiseaseTrendChart();
        });
      }
    },
    
    initChart() {
      const chartElement = this.$refs.performanceChart;
      if (!chartElement) return;
      
      // 清除旧的canvas元素
      while (chartElement.firstChild) {
        chartElement.removeChild(chartElement.firstChild);
      }
      
      // 创建新的canvas元素
      this.canvas = document.createElement('canvas');
      chartElement.appendChild(this.canvas);
      this.ctx = this.canvas.getContext('2d');
      
      // 设置canvas尺寸
      this.handleResize();
      
      // 绘制图表
      this.drawChart();
    },
    
    initDiseaseTrendChart() {
      const chartElement = this.$refs.diseaseTrendChart;
      if (!chartElement) return;
      
      // 清除旧的canvas元素
      while (chartElement.firstChild) {
        chartElement.removeChild(chartElement.firstChild);
      }
      
      // 创建新的canvas元素
      const canvas = document.createElement('canvas');
      chartElement.appendChild(canvas);
      const ctx = canvas.getContext('2d');
      
      // 设置canvas尺寸
      const rect = chartElement.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = 250;
      
      // 获取选中疾病的趋势数据
      const diseaseId = parseInt(this.selectedDisease);
      const data = this.diseaseTrendData[diseaseId] || [];
      
      if (data.length === 0) return;
      
      // 绘制图表
      const width = canvas.width;
      const height = canvas.height;
      const padding = { top: 20, right: 30, bottom: 40, left: 50 };
      
      // 清除画布
      ctx.clearRect(0, 0, width, height);
      
      // 设置绘图区域
      const chartWidth = width - padding.left - padding.right;
      const chartHeight = height - padding.top - padding.bottom;
      
      // 找出数据范围
      let minValue = 0.7; // 设置最小值为0.7，以便更好地显示差异
      let maxValue = 1.0;
      
      // 绘制网格和坐标轴
      ctx.strokeStyle = '#e0e0e0';
      ctx.lineWidth = 1;
      
      // 绘制水平网格线和Y轴标签
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.font = '10px Arial';
      ctx.fillStyle = '#666';
      
      const yStep = (maxValue - minValue) / 5;
      for (let i = 0; i <= 5; i++) {
        const y = padding.top + chartHeight - (i / 5) * chartHeight;
        const value = minValue + i * yStep;
        
        // 绘制网格线
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(padding.left + chartWidth, y);
        ctx.stroke();
        
        // 绘制Y轴标签
        ctx.fillText((value * 100).toFixed(0) + '%', padding.left - 10, y);
      }
      
      // 绘制X轴和标签
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      
      const xStep = chartWidth / (data.length - 1);
      data.forEach((item, index) => {
        const x = padding.left + index * xStep;
        
        // 绘制垂直网格线
        ctx.beginPath();
        ctx.moveTo(x, padding.top);
        ctx.lineTo(x, padding.top + chartHeight);
        ctx.stroke();
        
        // 绘制X轴标签
        const date = new Date(item.date);
        const label = `${date.getMonth() + 1}/${date.getDate()}`;
        ctx.fillText(label, x, padding.top + chartHeight + 10);
      });
      
      // 定义指标颜色
      const colors = {
        accuracy: '#4caf50',
        recall: '#2196f3',
        f1Score: '#673ab7'
      };
      
      // 绘制数据线和点
      const metrics = ['accuracy', 'recall', 'f1Score'];
      metrics.forEach(metric => {
        ctx.strokeStyle = colors[metric];
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        data.forEach((item, index) => {
          const x = padding.left + index * xStep;
          const value = item[metric];
          const y = padding.top + chartHeight - ((value - minValue) / (maxValue - minValue)) * chartHeight;
          
          if (index === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        });
        
        ctx.stroke();
        
        // 绘制数据点
        data.forEach((item, index) => {
          const x = padding.left + index * xStep;
          const value = item[metric];
          const y = padding.top + chartHeight - ((value - minValue) / (maxValue - minValue)) * chartHeight;
          
          ctx.fillStyle = colors[metric];
          ctx.beginPath();
          ctx.arc(x, y, 4, 0, Math.PI * 2);
          ctx.fill();
          
          // 为最后一个点添加标签
          if (index === data.length - 1) {
            ctx.fillStyle = colors[metric];
            ctx.textAlign = 'left';
            ctx.textBaseline = 'middle';
            ctx.font = 'bold 10px Arial';
            
            const displayValue = (item[metric] * 100).toFixed(0) + '%';
            ctx.fillText(displayValue, x + 8, y);
          }
        });
      });
      
      // 添加图例
      const legendY = padding.top;
      const legendX = padding.left + chartWidth - 150;
      const legendItems = [
        { label: '准确率', color: colors.accuracy },
        { label: '召回率', color: colors.recall },
        { label: 'F1值', color: colors.f1Score }
      ];
      
      legendItems.forEach((item, index) => {
        const y = legendY + index * 20;
        
        // 绘制颜色标记
        ctx.fillStyle = item.color;
        ctx.beginPath();
        ctx.rect(legendX, y, 12, 12);
        ctx.fill();
        
        // 绘制标签
        ctx.fillStyle = '#333';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.font = '12px Arial';
        ctx.fillText(item.label, legendX + 20, y + 6);
      });
    },
    
    handleResize() {
      if (!this.canvas || !this.ctx) return;
      
      const chartElement = this.$refs.performanceChart;
      if (!chartElement) return;
      
      // 获取容器尺寸
      const rect = chartElement.getBoundingClientRect();
      this.chartWidth = rect.width;
      this.chartHeight = rect.height || 300; // 设置默认高度
      
      // 设置canvas尺寸
      this.canvas.width = this.chartWidth;
      this.canvas.height = this.chartHeight;
      
      // 重新绘制图表
      this.drawChart();
      
      // 如果选择了特定疾病，更新疾病趋势图
      if (this.selectedDisease !== 'all' && this.$refs.diseaseTrendChart) {
        this.initDiseaseTrendChart();
      }
    },
    
    drawChart() {
      if (!this.ctx || !this.canvas || this.performanceData.length === 0) return;
      
      const ctx = this.ctx;
      const width = this.chartWidth;
      const height = this.chartHeight;
      const padding = this.chartPadding;
      const data = this.performanceData;
      
      // 清除画布
      ctx.clearRect(0, 0, width, height);
      
      // 设置绘图区域
      const chartWidth = width - padding.left - padding.right;
      const chartHeight = height - padding.top - padding.bottom;
      
      // 找出数据范围
      let minValue = 0.7; // 设置最小值为0.7，以便更好地显示差异
      let maxValue = 1.0;
      
      // 计算异常值的缩放因子，使其在图表上可见
      const anomalyScale = 5;
      
      // 绘制网格和坐标轴
      ctx.strokeStyle = '#e0e0e0';
      ctx.lineWidth = 1;
      
      // 绘制水平网格线和Y轴标签
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.font = '10px Arial';
      ctx.fillStyle = '#666';
      
      const yStep = (maxValue - minValue) / 5;
      for (let i = 0; i <= 5; i++) {
        const y = padding.top + chartHeight - (i / 5) * chartHeight;
        const value = minValue + i * yStep;
        
        // 绘制网格线
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(padding.left + chartWidth, y);
        ctx.stroke();
        
        // 绘制Y轴标签
        ctx.fillText((value * 100).toFixed(0) + '%', padding.left - 10, y);
      }
      
      // 绘制X轴和标签
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      
      const xStep = chartWidth / (data.length - 1);
      data.forEach((item, index) => {
        const x = padding.left + index * xStep;
        
        // 每隔一定间隔绘制垂直网格线
        if (index % Math.ceil(data.length / 7) === 0 || index === data.length - 1) {
          ctx.beginPath();
          ctx.moveTo(x, padding.top);
          ctx.lineTo(x, padding.top + chartHeight);
          ctx.stroke();
          
          // 绘制X轴标签
          const date = new Date(item.date);
          const label = `${date.getMonth() + 1}/${date.getDate()}`;
          ctx.fillText(label, x, padding.top + chartHeight + 10);
        }
      });
      
      // 定义指标颜色
      const colors = {
        accuracy: '#4caf50',
        recall: '#2196f3',
        f1Score: '#673ab7',
        anomaly: '#f44336'
      };
      
      // 存储数据点位置，用于提示框
      this.dataPoints = [];
      
      // 绘制数据线和点
      const metrics = ['accuracy', 'recall', 'f1Score', 'anomaly'];
      metrics.forEach(metric => {
        ctx.strokeStyle = colors[metric];
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        data.forEach((item, index) => {
          const x = padding.left + index * xStep;
          let value = item[metric];
          
          // 对异常值进行缩放，使其在图表上可见
          if (metric === 'anomaly') {
            value = minValue + (value * anomalyScale);
          }
          
          const y = padding.top + chartHeight - ((value - minValue) / (maxValue - minValue)) * chartHeight;
          
          if (index === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
          
          // 存储数据点位置
          if (!this.dataPoints[index]) {
            this.dataPoints[index] = {
              x,
              y: {},
              date: item.date,
              values: {}
            };
          }
          this.dataPoints[index].y[metric] = y;
          this.dataPoints[index].values[metric] = item[metric];
        });
        
        ctx.stroke();
        
        // 绘制数据点
        data.forEach((item, index) => {
          const x = padding.left + index * xStep;
          let value = item[metric];
          
          // 对异常值进行缩放
          if (metric === 'anomaly') {
            value = minValue + (value * anomalyScale);
          }
          
          const y = padding.top + chartHeight - ((value - minValue) / (maxValue - minValue)) * chartHeight;
          
          ctx.fillStyle = colors[metric];
          ctx.beginPath();
          ctx.arc(x, y, 4, 0, Math.PI * 2);
          ctx.fill();
          
          // 为最后一个点添加标签
          if (index === data.length - 1) {
            ctx.fillStyle = colors[metric];
            ctx.textAlign = 'left';
            ctx.textBaseline = 'middle';
            ctx.font = 'bold 10px Arial';
            
            // 显示原始值，而不是缩放后的值
            const displayValue = (item[metric] * 100).toFixed(0) + '%';
            ctx.fillText(displayValue, x + 8, y);
          }
        });
      });
    },
    
    handleChartMouseMove(event) {
      if (!this.dataPoints || this.dataPoints.length === 0) return;
      
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = event.clientX - rect.left;
      
      // 查找最近的数据点
      let closestPoint = null;
      let minDistance = Infinity;
      
      this.dataPoints.forEach(point => {
        const distance = Math.abs(point.x - mouseX);
        if (distance < minDistance) {
          minDistance = distance;
          closestPoint = point;
        }
      });
      
      // 如果鼠标足够接近数据点，显示提示框
      if (closestPoint && minDistance < 30) {
        this.showTooltip = true;
        this.tooltipData = {
          date: this.formatDateForDisplay(closestPoint.date),
          values: closestPoint.values
        };
        
        // 更新提示框位置
        const tooltipElement = this.$refs.chartTooltip;
        if (tooltipElement) {
          // 计算提示框位置，避免超出边界
          const tooltipWidth = 150;
          const tooltipHeight = 120;
          
          let tooltipX = closestPoint.x - tooltipWidth / 2;
          let tooltipY = Math.min(...Object.values(closestPoint.y)) - tooltipHeight - 10;
          
          // 确保提示框不超出左右边界
          if (tooltipX < 0) tooltipX = 0;
          if (tooltipX + tooltipWidth > rect.width) tooltipX = rect.width - tooltipWidth;
          
          // 如果提示框会超出顶部，则显示在数据点下方
          if (tooltipY < 0) tooltipY = Math.max(...Object.values(closestPoint.y)) + 10;
          
          tooltipElement.style.left = `${tooltipX}px`;
          tooltipElement.style.top = `${tooltipY}px`;
        }
      } else {
        this.showTooltip = false;
      }
    },
    
    handleChartMouseOut() {
      this.showTooltip = false;
    },
    
    navigateDate(direction) {
      const newDate = new Date(this.selectedDate);
      newDate.setDate(newDate.getDate() + direction);
      
      // 不允许选择未来日期
      const today = new Date();
      if (newDate <= today) {
        this.selectedDate = newDate;
        this.updateMetricsForDate();
      }
    },
    
    updateMetricsForDate() {
      // 根据选择的日期更新指标
      const dateStr = this.formatDate(this.selectedDate);
      const dataPoint = this.performanceData.find(d => d.date === dateStr);
      
      if (dataPoint) {
        this.currentMetrics = {
          accuracy: dataPoint.accuracy.toFixed(2),
          recall: dataPoint.recall.toFixed(2),
          f1Score: dataPoint.f1Score.toFixed(2),
          anomaly: dataPoint.anomaly.toFixed(2)
        };
      }
    },
    
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    
    formatDateForDisplay(dateStr) {
      const date = new Date(dateStr);
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
    },
    
    getTrendClass(trend) {
      if (trend > 0) return 'positive';
      if (trend < 0) return 'negative';
      return '';
    },
    
    getAccuracyClass(value) {
      if (value >= 0.95) return 'excellent';
      if (value >= 0.90) return 'good';
      if (value >= 0.85) return 'average';
      return 'poor';
    },
    
    getRecallClass(value) {
      if (value >= 0.90) return 'excellent';
      if (value >= 0.85) return 'good';
      if (value >= 0.80) return 'average';
      return 'poor';
    },
    
    getF1Class(value) {
      if (value >= 0.90) return 'excellent';
      if (value >= 0.85) return 'good';
      if (value >= 0.80) return 'average';
      return 'poor';
    },
    
    getSelectedDiseaseName() {
      if (this.selectedDisease === 'all') return '';
      const disease = this.diseases.find(d => d.id === parseInt(this.selectedDisease));
      return disease ? disease.name : '';
    },
    
    getSelectedDiseaseData() {
      if (this.selectedDisease === 'all') return null;
      return this.diseases.find(d => d.id === parseInt(this.selectedDisease)) || {};
    },
    
    getMetricLabel(key) {
      const labels = {
        accuracy: '准确率',
        recall: '召回率',
        f1Score: 'F1值',
        anomaly: '异常值'
      };
      return labels[key] || key;
    }
  }
}
</script>

<style scoped>
.diagnostic-page {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
}

.section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 24px;
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.section:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.section-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 指标卡片样式 */
.metrics-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 12px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  transition: all 0.3s ease;
}

.metric-icon.accuracy {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.metric-icon.recall {
  background-color: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.metric-icon.f1-score {
  background-color: rgba(103, 58, 183, 0.1);
  color: #673ab7;
}

.metric-icon.anomaly {
  background-color: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.metric-card:hover .metric-icon {
  transform: scale(1.1);
}

.metric-details {
  flex: 1;
}

.metric-details h3 {
  font-size: 14px;
  font-weight: 500;
  color: #666;
  margin: 0 0 8px 0;
}

.metric-value {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.metric-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 12px;
  width: fit-content;
}

.metric-trend.positive {
  color: #4caf50;
  background-color: rgba(76, 175, 80, 0.1);
}

.metric-trend.negative {
  color: #f44336;
  background-color: rgba(244, 67, 54, 0.1);
}

.metric-trend svg {
  margin-right: 4px;
}

/* 图表样式 */
.chart-container {
  margin-bottom: 30px;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 20px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  position: relative;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #666;
  padding: 4px 8px;
  border-radius: 12px;
  background-color: #f9f9f9;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 6px;
}

.legend-color.accuracy {
  background-color: #4caf50;
}

.legend-color.recall {
  background-color: #2196f3;
}

.legend-color.f1-score {
  background-color: #673ab7;
}

.legend-color.anomaly {
  background-color: #f44336;
}

.chart {
  height: 300px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
}

/* 图表提示框样式 */
.chart-tooltip {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  pointer-events: none;
  z-index: 10;
  min-width: 150px;
  border: 1px solid #f0f0f0;
}

.tooltip-date {
  font-weight: 600;
  font-size: 12px;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
  color: #333;
}

.tooltip-item {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
  font-size: 12px;
}

.tooltip-color {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  margin-right: 6px;
}

.tooltip-color.accuracy {
  background-color: #4caf50;
}

.tooltip-color.recall {
  background-color: #2196f3;
}

.tooltip-color.f1Score {
  background-color: #673ab7;
}

.tooltip-color.anomaly {
  background-color: #f44336;
}

.tooltip-label {
  margin-right: 6px;
  color: #666;
}

.tooltip-value {
  font-weight: 600;
  color: #333;
}

/* 日期选择器样式 */
.date-selector {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.date-nav {
  display: flex;
  align-items: center;
  gap: 16px;
  background-color: #f9f9f9;
  padding: 8px 16px;
  border-radius: 24px;
}

.date-nav-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: white;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.date-nav-btn:hover:not(:disabled) {
  background-color: #f0f0f0;
  transform: translateY(-1px);
}

.date-nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.current-date {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  padding: 8px 16px;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-container {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.date-filter, .disease-filter, .date-range-filter {
  display: flex;
  align-items: center;
}

.date-filter span, .disease-filter span, .date-range-filter span {
  margin-right: 8px;
  font-size: 14px;
  color: #666;
}

.select-control {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: white;
  font-size: 14px;
  color: #333;
  outline: none;
  transition: all 0.2s;
  cursor: pointer;
}

.select-control:hover {
  border-color: #d0d0d0;
}

.select-control:focus {
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

/* 表格样式 */
.table-wrapper {
  margin-bottom: 30px;
}

.table-container {
  overflow-x: auto;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.data-table th {
  background-color: #f9f9f9;
  font-weight: 500;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 1;
}

.data-table tbody tr {
  transition: background-color 0.2s;
}

.data-table tbody tr:hover {
  background-color: #f5f7fa;
}

.data-table td.excellent {
  color: #4caf50;
  font-weight: 500;
}

.data-table td.good {
  color: #2196f3;
  font-weight: 500;
}

.data-table td.average {
  color: #ff9800;
  font-weight: 500;
}

.data-table td.poor {
  color: #f44336;
  font-weight: 500;
}

/* 混淆矩阵样式 */
.confusion-matrix-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
}

.confusion-matrix-container h3 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.confusion-matrix {
  display: table;
  border-collapse: collapse;
  margin: 0 auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  overflow: hidden;
}

.matrix-row {
  display: table-row;
}

.matrix-cell {
  display: table-cell;
  width: 120px;
  height: 120px;
  text-align: center;
  vertical-align: middle;
  border: 1px solid #f0f0f0;
  padding: 10px;
  transition: all 0.2s;
}

.matrix-cell:hover {
  transform: scale(1.02);
  z-index: 2;
}

.matrix-cell.header {
  background-color: #f9f9f9;
  font-weight: 500;
  color: #333;
  width: 100px;
  height: 50px;
}

.matrix-cell.tp {
  background-color: rgba(76, 175, 80, 0.1);
}

.matrix-cell.fp {
  background-color: rgba(244, 67, 54, 0.1);
}

.matrix-cell.fn {
  background-color: rgba(255, 152, 0, 0.1);
}

.matrix-cell.tn {
  background-color: rgba(33, 150, 243, 0.1);
}

.cell-value {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.cell-label {
  font-size: 12px;
  color: #666;
}

/* 疾病趋势图样式 */
.disease-trend-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
}

.disease-trend-container h3 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.disease-trend-chart {
  height: 250px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 模型诊断建议样式 */
.recommendations {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.recommendation-card {
  display: flex;
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.recommendation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.recommendation-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.recommendation-icon.warning {
  background-color: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.recommendation-icon.info {
  background-color: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.recommendation-icon.success {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.recommendation-content {
  flex: 1;
}

.recommendation-content h4 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0 0 8px 0;
}

.recommendation-content p {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.recommendation-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.action-button {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background-color: #f5f7fa;
  color: #333;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:hover {
  background-color: #e0e0e0;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .metrics-cards {
    grid-template-columns: 1fr;
  }
  
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .chart-legend {
    margin-top: 10px;
    flex-wrap: wrap;
  }
  
  .confusion-matrix-container {
    overflow-x: auto;
  }
  
  .matrix-cell {
    width: 100px;
    height: 100px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-container {
    margin-top: 12px;
    width: 100%;
  }
  
  .recommendations {
    grid-template-columns: 1fr;
  }
}

/* 添加一些动画效果 */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.metric-card:hover .metric-value {
  animation: pulse 1s infinite;
}
</style>
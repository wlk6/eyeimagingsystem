<template>
  <div class="eye-diagnosis-container">
    <div class="main-content">
      <!-- 患者选择部分 -->
      <div class="upload-section" v-if="!diagnosisResult">
        <div class="form-container">
          <h2>选择患者</h2>
          
          <div v-if="isLoadingPatients" class="loading-patients">
            <div class="loading-spinner-small"></div>
            <p>正在加载患者列表...</p>
          </div>
          
          <div v-else-if="patientsList.length === 0" class="no-patients">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
              <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
            <p>未找到患者记录</p>
            <button class="btn-refresh" @click="fetchPatients">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path>
              </svg>
              刷新
            </button>
          </div>
          
          <div v-else class="patients-list">
            <div class="search-bar">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="搜索患者姓名或电话" 
                class="search-input"
              />
              <button class="btn-refresh" @click="fetchPatients">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path>
                </svg>
                刷新
              </button>
            </div>
            
            <div class="patients-grid">
              <div 
                v-for="patient in filteredPatients" 
                :key="patient.patient_id" 
                class="patient-card"
                :class="{ 'selected': selectedPatient && selectedPatient.patient_id === patient.patient_id }"
                @click="selectPatient(patient)"
              >
                <div class="patient-avatar">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <div class="patient-info">
                  <h3 class="patient-name">{{ patient.patientName }}</h3>
                  <div class="patient-details">
                    <span class="patient-gender">{{ patient.gender === 'male' ? '男' : '女' }}</span>
                    <span class="patient-phone">{{ patient.phone }}</span>
                  </div>
                  <div class="patient-record" v-if="patient.record && patient.record !== 'null'">
                    <span class="record-label">既往病史:</span>
                    <span class="record-value">{{ patient.record }}</span>
                  </div>
                </div>
                <div class="patient-select-indicator">
                  <svg v-if="selectedPatient && selectedPatient.patient_id === patient.patient_id" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                </div>
              </div>
            </div>
            
            <div class="error-message" v-if="errors.patient">{{ errors.patient }}</div>
          </div>

          <h2 class="mt-6">眼部图像上传</h2>
          <div class="eye-upload-container">
            <div class="eye-upload left-eye">
              <h3>左眼图像</h3>
              <div 
                class="upload-area" 
                :class="{ 'has-image': leftEyePreview }"
                @click="triggerFileInput('leftEye')"
                @dragover.prevent
                @drop.prevent="handleFileDrop($event, 'leftEye')"
              >
                <div v-if="!leftEyePreview" class="upload-placeholder">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7"></path>
                    <line x1="16" y1="5" x2="22" y2="5"></line>
                    <line x1="19" y1="2" x2="19" y2="8"></line>
                    <circle cx="9" cy="9" r="2"></circle>
                    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
                  </svg>
                  <p>点击或拖拽上传左眼图像</p>
                </div>
                <img v-else :src="leftEyePreview" alt="左眼预览" class="eye-preview" />
                <button 
                  v-if="leftEyePreview" 
                  type="button" 
                  class="remove-image" 
                  @click.stop="removeImage('leftEye')"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              <input 
                type="file" 
                ref="leftEyeInput" 
                @change="handleFileChange($event, 'leftEye')" 
                accept="image/*" 
                class="file-input"
              />
            </div>
            
            <div class="eye-upload right-eye">
              <h3>右眼图像</h3>
              <div 
                class="upload-area"
                :class="{ 'has-image': rightEyePreview }"
                @click="triggerFileInput('rightEye')"
                @dragover.prevent
                @drop.prevent="handleFileDrop($event, 'rightEye')"
              >
                <div v-if="!rightEyePreview" class="upload-placeholder">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7"></path>
                    <line x1="16" y1="5" x2="22" y2="5"></line>
                    <line x1="19" y1="2" x2="19" y2="8"></line>
                    <circle cx="9" cy="9" r="2"></circle>
                    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
                  </svg>
                  <p>点击或拖拽上传右眼图像</p>
                </div>
                <img v-else :src="rightEyePreview" alt="右眼预览" class="eye-preview" />
                <button 
                  v-if="rightEyePreview" 
                  type="button" 
                  class="remove-image" 
                  @click.stop="removeImage('rightEye')"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              <input 
                type="file" 
                ref="rightEyeInput" 
                @change="handleFileChange($event, 'rightEye')" 
                accept="image/*" 
                class="file-input"
              />
            </div>
          </div>
          
          <div class="form-note">
            <p>注意：至少需要上传一张眼部图像（左眼或右眼）</p>
            <p v-if="errors.images" class="error-message">{{ errors.images }}</p>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn-submit" :disabled="isSubmitting" @click="submitDiagnosis">
              {{ isSubmitting ? '诊断中...' : '开始诊断' }}
              <span v-if="isSubmitting" class="spinner"></span>
            </button>
          </div>
        </div>
      </div>

      <!-- 诊断结果部分 -->
      <div class="diagnosis-results" v-if="diagnosisResult" ref="reportContent">
        <div class="results-header">
          <div class="report-title">
            <h2>眼部健康诊断报告</h2>
            <div class="report-id">报告编号: {{ generateReportId() }}</div>
          </div>
          
          <div class="patient-summary">
            <div class="patient-info-item">
              <span class="label">患者姓名:</span>
              <span class="value">{{ selectedPatient.patientName }}</span>
            </div>
            <div class="patient-info-item">
              <span class="label">性别:</span>
              <span class="value">{{ selectedPatient.gender === 'male' ? '男' : '女' }}</span>
            </div>
            <div class="patient-info-item">
              <span class="label">联系电话:</span>
              <span class="value">{{ selectedPatient.phone }}</span>
            </div>
            <div class="patient-info-item">
              <span class="label">诊断时间:</span>
              <span class="value">{{ currentDateTime }}</span>
            </div>
          </div>
          
          <div class="report-actions-top">
            <button class="btn-back" @click="resetDiagnosis">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
              返回重新诊断
            </button>
            
            <div class="action-buttons">
              <button class="btn-save" @click="saveReport">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                  <polyline points="17 21 17 13 7 13 7 21"></polyline>
                  <polyline points="7 3 7 8 15 8"></polyline>
                </svg>
                保存报告
              </button>
            </div>
          </div>
        </div>

        <!-- 综合诊断结果 -->
        <div class="result-section combined-result" v-if="hasCombinedResult">
          <h3>综合诊断结果</h3>
          <div class="result-card">
            <div class="result-overview">
              <div class="risk-indicator" :class="getDiagnosisRiskLevel()">
                <div class="risk-level">{{ getDiagnosisRiskText() }}</div>
                <div class="risk-description">{{ getDiagnosisRiskDescription() }}</div>
              </div>
            </div>
            
            <div class="result-summary">
              <div class="result-item" v-for="(value, key) in diagnosisResult.combined_result" :key="`combined-${key}`">
                <div class="disease-name">{{ getDiseaseLabel(key) }}</div>
                <div class="probability-bar">
                  <div class="probability-fill" :style="{ width: `${value * 100}%`, backgroundColor: getProbabilityColor(value) }"></div>
                </div>
                <div class="probability-value">{{ (value * 100).toFixed(1) }}%</div>
              </div>
            </div>
            
            <div class="disease-types" v-if="diagnosisResult.combined_disease_types && diagnosisResult.combined_disease_types.length">
              <h4>检测到的疾病类型:</h4>
              <div class="disease-tags">
                <span class="disease-tag" v-for="(disease, index) in diagnosisResult.combined_disease_types" :key="`combined-disease-${index}`">
                  {{ disease }}
                </span>
              </div>
            </div>
            <div class="no-disease" v-else-if="diagnosisResult.combined_disease_types && !diagnosisResult.combined_disease_types.length">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
              未检测到明显疾病
            </div>
          </div>
        </div>

        <div class="eyes-results">
          <!-- 左眼诊断结果 -->
          <div class="result-section left-eye-result" v-if="diagnosisResult.left_result">
            <h3>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              左眼诊断结果
            </h3>
            <div class="result-card">
              <div class="eye-images">
                <div class="original-image">
                  <h4>原始图像</h4>
                  <img :src="leftEyePreview" alt="左眼图像" class="eye-image" />
                </div>
                <div class="heatmap-image">
                  <h4>热力图分析</h4>
                  <div class="heatmap-container">
                    <img :src="leftEyeHeatmap" alt="左眼热力图" class="eye-image" />
                    <div class="heatmap-legend">
                      <div class="legend-item">
                        <div class="legend-color high"></div>
                        <span>高风险区域</span>
                      </div>
                      <div class="legend-item">
                        <div class="legend-color medium"></div>
                        <span>中风险区域</span>
                      </div>
                      <div class="legend-item">
                        <div class="legend-color low"></div>
                        <span>低风险区域</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="result-summary">
                <div class="result-item" v-for="(value, key) in diagnosisResult.left_result" :key="`left-${key}`">
                  <div class="disease-name">{{ getDiseaseLabel(key) }}</div>
                  <div class="probability-bar">
                    <div class="probability-fill" :style="{ width: `${value * 100}%`, backgroundColor: getProbabilityColor(value) }"></div>
                  </div>
                  <div class="probability-value">{{ (value * 100).toFixed(1) }}%</div>
                </div>
              </div>
              
              <div class="disease-types" v-if="diagnosisResult.left_disease_types && diagnosisResult.left_disease_types.length">
                <h4>检测到的疾病类型:</h4>
                <div class="disease-tags">
                  <span class="disease-tag" v-for="(disease, index) in diagnosisResult.left_disease_types" :key="`left-disease-${index}`">
                    {{ disease }}
                  </span>
                </div>
                <div class="disease-description" v-if="getHighestDisease('left')">
                  <h5>{{ getHighestDisease('left') }}:</h5>
                  <p>{{ getDiseaseDescription(getHighestDisease('left')) }}</p>
                </div>
              </div>
              <div class="no-disease" v-else-if="diagnosisResult.left_disease_types && diagnosisResult.left_disease_types.length === 0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                未检测到明显疾病
              </div>
            </div>
          </div>

          <!-- 右眼诊断结果 -->
          <div class="result-section right-eye-result" v-if="diagnosisResult.right_result">
            <h3>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              右眼诊断结果
            </h3>
            <div class="result-card">
              <div class="eye-images">
                <div class="original-image">
                  <h4>原始图像</h4>
                  <img :src="rightEyePreview" alt="右眼图像" class="eye-image" />
                </div>
                <div class="heatmap-image">
                  <h4>热力图分析</h4>
                  <div class="heatmap-container">
                    <img :src="rightEyeHeatmap" alt="右眼热力图" class="eye-image" style="width: 200px;"/>
                    <div class="heatmap-legend">
                      <div class="legend-item">
                        <div class="legend-color high"></div>
                        <span>高风险区域</span>
                      </div>
                      <div class="legend-item">
                        <div class="legend-color medium"></div>
                        <span>中风险区域</span>
                      </div>
                      <div class="legend-item">
                        <div class="legend-color low"></div>
                        <span>低风险区域</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="result-summary">
                <div class="result-item" v-for="(value, key) in diagnosisResult.right_result" :key="`right-${key}`">
                  <div class="disease-name">{{ getDiseaseLabel(key) }}</div>
                  <div class="probability-bar">
                    <div class="probability-fill" :style="{ width: `${value * 100}%`, backgroundColor: getProbabilityColor(value) }"></div>
                  </div>
                  <div class="probability-value">{{ (value * 100).toFixed(1) }}%</div>
                </div>
              </div>
              
              <div class="disease-types" v-if="diagnosisResult.right_disease_types && diagnosisResult.right_disease_types.length">
                <h4>检测到的疾病类型:</h4>
                <div class="disease-tags">
                  <span class="disease-tag" v-for="(disease, index) in diagnosisResult.right_disease_types" :key="`right-disease-${index}`">
                    {{ disease }}
                  </span>
                </div>
                <div class="disease-description" v-if="getHighestDisease('right')">
                  <h5>{{ getHighestDisease('right') }}:</h5>
                  <p>{{ getDiseaseDescription(getHighestDisease('right')) }}</p>
                </div>
              </div>
              <div class="no-disease" v-else-if="diagnosisResult.right_disease_types && diagnosisResult.right_disease_types.length === 0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                未检测到明显疾病
              </div>
            </div>
          </div>
        </div>

        <div class="diagnosis-summary">
          <h3>诊断总结与建议</h3>
          <div class="summary-card">
            <div class="summary-content">
              <div class="summary-icon" :class="getDiagnosisRiskLevel()">
                <svg v-if="hasDiseases()" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
              </div>
              
              <div class="summary-text">
                <p v-if="hasCombinedResult && diagnosisResult.combined_disease_types && diagnosisResult.combined_disease_types.length">
                  根据AI分析，患者眼部可能存在 <strong>{{ diagnosisResult.combined_disease_types.join('、') }}</strong> 问题。
                  {{ getRecommendationText() }}
                </p>
                <p v-else-if="(diagnosisResult.left_disease_types && diagnosisResult.left_disease_types.length > 0) || 
                             (diagnosisResult.right_disease_types && diagnosisResult.right_disease_types.length > 0)">
                  根据AI分析，患者眼部可能存在异常。
                  {{ getRecommendationText() }}
                </p>
                <p v-else>
                  根据AI分析，患者眼部未检测到明显异常，建议定期进行眼部检查，保持良好用眼习惯。
                </p>
              </div>
            </div>
            
            <div class="recommendations">
              <h4>健康建议</h4>
              <ul>
                <li v-for="(recommendation, index) in getHealthRecommendations()" :key="`rec-${index}`">
                  {{ recommendation }}
                </li>
              </ul>
            </div>
            
            <div class="follow-up">
              <h4>后续跟进</h4>
              <p>{{ getFollowUpText() }}</p>
            </div>
            
            <div class="disclaimer">
              <p><strong>免责声明：</strong>本诊断结果仅供参考，不能替代专业医生的诊断和建议。如有任何疑问或不适，请及时就医。</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载指示器 -->
    <div class="loading-overlay" v-if="isSubmitting || isExporting">
      <div class="loading-spinner"></div>
      <p>{{ isExporting ? '正在生成PDF报告，请稍候...' : '正在分析眼部图像，请稍候...' }}</p>
    </div>

    <!-- 消息提示 -->
    <div class="toast" v-if="toast.show">
      <div class="toast-content" :class="toast.type">
        <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import html2pdf from 'html2pdf.js';

export default {
  name: 'EyeDiagnosis',
  data() {
    return {
      token: '',
      // 患者列表
      patientsList: [],
      selectedPatient: null,
      searchQuery: '',
      isLoadingPatients: false,
      
      // 眼部图像
      leftEyeFile: null,
      rightEyeFile: null,
      leftEyePreview: null,
      rightEyePreview: null,
      
      // 热力图
      leftEyeHeatmap: '/imgpro/left.png',
      rightEyeHeatmap: '/imgpro/right.png',
      
      // 表单验证
      errors: {
        patient: '',
        images: ''
      },
      
      // 提交状态
      isSubmitting: false,
      isExporting: false,
      
      // 诊断结果
      diagnosisResult: null,
      
      // 消息提示
      toast: {
        show: false,
        message: '',
        type: 'success'
      },
      
      // 疾病映射
      diseaseMapping: {
        'N': '正常',
        'D': '糖尿病视网膜病变',
        'G': '青光眼',
        'C': '白内障',
        'A': '年龄相关性黄斑变性',
        'H': '高血压视网膜病变',
        'M': '病理性近视',
        'O': '其他眼部异常'
      },
      
      // 疾病描述
      diseaseDescriptions: {
        '糖尿病视网膜病变': '糖尿病视网膜病变是由糖尿病引起的视网膜血管损伤，可能导致视力下降甚至失明。早期干预和血糖控制对预防视力损失至关重要。',
        '青光眼': '青光眼是一组导致视神经损伤的眼病，通常与眼内压升高有关。如不及时治疗，可能导致视野缺损和不可逆的视力丧失。',
        '白内障': '白内障是指眼睛晶状体变得混浊，导致视力模糊、色彩感知下降等症状。是全球主要的可治疗性致盲眼病之一。',
        '年龄相关性黄斑变性': '年龄相关性黄斑变性是影响视网膜中央区域（黄斑）的疾病，导致中央视力下降，影响阅读和面部识别等精细视觉活动。',
        '高血压视网膜病变': '高血压视网膜病变是长期高血压导致的视网膜血管改变，可能导致视网膜出血、水肿和视力下降。',
        '病理性近视': '病理性近视是一种严重的近视形式，伴随眼轴过度延长和视网膜变性，增加视网膜脱离和黄斑变性的风险。',
        '其他眼部异常': '包括多种可能影响眼部健康的疾病或异常状况，需要进一步专业检查确定具体病因。'
      },
      
      // 当前日期时间
      currentDateTime: '',
      
      // PDF导出配置
      pdfOptions: {
        margin: 10,
        filename: '眼部健康诊断报告.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { 
          scale: 2,
          useCORS: true,
          letterRendering: true,
          logging: false
        },
        jsPDF: { 
          unit: 'mm', 
          format: 'a4', 
          orientation: 'portrait',
          compress: true
        },
        fontFaces: [
          {
            family: 'SimSun',
            style: 'normal'
          }
        ]
      }
    };
  },
  
  computed: {
    hasCombinedResult() {
      return this.diagnosisResult && 
             (this.diagnosisResult.combined_result !== null || 
              this.diagnosisResult.combined_disease_types !== null);
    },
    
    filteredPatients() {
      if (!this.searchQuery) {
        return this.patientsList;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.patientsList.filter(patient => {
        return patient.patientName.toLowerCase().includes(query) || 
               patient.phone.toLowerCase().includes(query);
      });
    }
  },
  
  mounted() {
    // 从本地存储中获取 info 对象
    const info = localStorage.getItem('info');

    if (info) {
      // 将 JSON 字符串解析为对象
      const parsedInfo = JSON.parse(info);

      // 检查解析后的对象是否包含 token 属性
      if (parsedInfo && parsedInfo.token) {
        this.token = parsedInfo.token;
      } else {
        console.log('info 对象中不包含 token 属性');
      }
    } else {
      console.log('本地存储中未找到 info 对象');
    }    
    
    this.updateDateTime();
    this.fetchPatients();
    
    // 动态加载html2pdf.js库
    this.loadHtml2PdfScript();
  },
  
  methods: {
    // 加载html2pdf.js库
    loadHtml2PdfScript() {
      if (typeof html2pdf === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
        script.async = true;
        script.onload = () => {
          console.log('html2pdf.js 加载成功');
        };
        script.onerror = () => {
          console.error('html2pdf.js 加载失败');
          this.showToast('PDF导出组件加载失败，请刷新页面重试', 'error');
        };
        document.head.appendChild(script);
      }
    },
    
    // 获取患者列表
    async fetchPatients() {
      this.isLoadingPatients = true;
      
      try {
        const response = await fetch('http://8.155.59.127:34561/user/detail/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'token': this.token
          }
        });
        
        if (!response.ok) {
          throw new Error('获取患者列表失败');
        }
        
        const data = await response.json();
        this.patientsList = data;
        
        // 处理性别格式
        this.patientsList = this.patientsList.map(patient => {
          if (patient.gender === '男') {
            patient.gender = 'male';
          } else if (patient.gender === '女') {
            patient.gender = 'female';
          }
          return patient;
        });
        
      } catch (error) {
        console.error('获取患者列表错误:', error);
        this.showToast('获取患者列表失败，请稍后重试', 'error');
      } finally {
        this.isLoadingPatients = false;
      }
    },
    
    // 选择患者
    selectPatient(patient) {
      this.selectedPatient = patient;
      this.errors.patient = '';
    },
    
    // 更新当前日期时间
    updateDateTime() {
      const now = new Date();
      const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      this.currentDateTime = now.toLocaleDateString('zh-CN', options);
    },
    
    // 生成报告ID
    generateReportId() {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
      return `EYE-${year}${month}${day}-${random}`;
    },
    
    // 触发文件选择
    triggerFileInput(eye) {
      this.$refs[`${eye}Input`].click();
    },
    
    // 处理文件选择
    handleFileChange(event, eye) {
      const file = event.target.files[0];
      if (!file) return;
      
      if (!file.type.startsWith('image/')) {
        this.showToast('请上传有效的图像文件', 'error');
        return;
      }
      
      this[`${eye}File`] = file;
      this.createImagePreview(file, eye);
      this.errors.images = '';
    },
    
    // 处理文件拖放
    handleFileDrop(event, eye) {
      const file = event.dataTransfer.files[0];
      if (!file) return;
      
      if (!file.type.startsWith('image/')) {
        this.showToast('请上传有效的图像文件', 'error');
        return;
      }
      
      this[`${eye}File`] = file;
      this.createImagePreview(file, eye);
      this.errors.images = '';
    },
    
    // 创建图像预览
    createImagePreview(file, eye) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this[`${eye}Preview`] = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    // 移除图像
    removeImage(eye) {
      this[`${eye}File`] = null;
      this[`${eye}Preview`] = null;
      this.$refs[`${eye}Input`].value = '';
    },
    
    // 验证表单
    validateForm() {
      let isValid = true;
      this.errors = {
        patient: '',
        images: ''
      };
      
      // 验证患者选择
      if (!this.selectedPatient) {
        this.errors.patient = '请选择一位患者';
        isValid = false;
      }
      
      // 验证图像
      if (!this.leftEyeFile && !this.rightEyeFile) {
        this.errors.images = '请至少上传一张眼部图像（左眼或右眼）';
        isValid = false;
      }
      
      return isValid;
    },
    
    // 提交诊断
    async submitDiagnosis() {
      if (!this.validateForm()) {
        return;
      }
      
      this.isSubmitting = true;
      
      try {
        // 创建表单数据
        const formData = new FormData();
        
        // 添加眼部图像
        if (this.leftEyeFile) {
          formData.append('left_eye', this.leftEyeFile);
        }
        
        if (this.rightEyeFile) {
          formData.append('right_eye', this.rightEyeFile);
        }
        
        // 发送请求
        const response = await fetch('http://127.0.0.1:4523/m2/5776644-5460725-default/283867121', {
          method: 'POST',    
          headers: {
            'token': this.token,
          },
          body: formData
        });
        
        if (!response.ok) {
          throw new Error('诊断请求失败');
        }
        
        // 解析响应数据
        const data = await response.json();
        
        // 模拟随机诊断结果，左右眼有差异
        this.simulateDifferentEyeDiagnosisResults();
        
        // 更新日期时间
        this.updateDateTime();
        
        this.showToast('诊断完成', 'success');
      } catch (error) {
        console.error('诊断错误:', error);
        this.showToast('诊断请求失败，请稍后重试', 'error');
        
        // 模拟随机诊断结果（仅用于演示）
        this.simulateDifferentEyeDiagnosisResults();
      } finally {
        this.isSubmitting = false;
      }
    },

    // 模拟左右眼不同的诊断结果
    simulateDifferentEyeDiagnosisResults() {
      // 生成基础随机结果
      const baseResult = {
        "N": Math.random() * 0.5 + 0.3, // 正常概率在30%-80%之间
        "D": Math.random() * 0.3,       // 其他疾病概率较低
        "G": Math.random() * 0.3,
        "C": Math.random() * 0.3,
        "A": Math.random() * 0.3,
        "H": Math.random() * 0.3,
        "M": Math.random() * 0.3,
        "O": Math.random() * 0.2
      };
      
      // 为左眼和右眼创建不同的结果
      const leftResult = { ...baseResult };
      const rightResult = {};
      
      // 右眼结果基于左眼，但有细微差异
      for (const key in leftResult) {
        // 为右眼添加-15%到+15%的随机变化
        const variation = 1 + (Math.random() * 0.3 - 0.15);
        rightResult[key] = Math.min(Math.max(leftResult[key] * variation, 0), 1);
      }
      
      // 随机选择一种疾病在一只眼睛中更明显
      const diseaseKeys = ["D", "G", "C", "A", "H", "M", "O"];
      const randomDiseaseKey = diseaseKeys[Math.floor(Math.random() * diseaseKeys.length)];
      
      // 随机决定哪只眼睛有更明显的症状
      if (Math.random() > 0.5) {
        leftResult[randomDiseaseKey] = Math.min(leftResult[randomDiseaseKey] * 1.5, 0.9);
        leftResult["N"] = Math.max(leftResult["N"] * 0.7, 0.1);
      } else {
        rightResult[randomDiseaseKey] = Math.min(rightResult[randomDiseaseKey] * 1.5, 0.9);
        rightResult["N"] = Math.max(rightResult["N"] * 0.7, 0.1);
      }
      
      // 归一化概率值
      this.normalizeResults(leftResult);
      this.normalizeResults(rightResult);
      
      // 确定疾病类型
      const leftDiseaseTypes = this.determineDiseaseTypes(leftResult);
      const rightDiseaseTypes = this.determineDiseaseTypes(rightResult);
      
      // 创建综合结果 - 取左右眼的平均值
      const combinedResult = {};
      for (const key in leftResult) {
        if (rightResult[key]) {
          combinedResult[key] = (leftResult[key] + rightResult[key]) / 2;
        } else {
          combinedResult[key] = leftResult[key];
        }
      }
      
      // 归一化综合结果
      this.normalizeResults(combinedResult);
      
      // 确定综合疾病类型
      const combinedDiseaseTypes = this.determineDiseaseTypes(combinedResult);
      
      // 构建诊断结果对象
      const result = {
        combined_result: combinedResult,
        combined_disease_types: combinedDiseaseTypes,
        left_result: null,
        left_disease_types: null,
        right_result: null,
        right_disease_types: null
      };
      
      // 如果有左眼图像，添加左眼结果
      if (this.leftEyeFile) {
        result.left_result = leftResult;
        result.left_disease_types = leftDiseaseTypes;
      }
      
      // 如果有右眼图像，添加右眼结果
      if (this.rightEyeFile) {
        result.right_result = rightResult;
        result.right_disease_types = rightDiseaseTypes;
      }
      
      this.diagnosisResult = result;
    },
    
    // 归一化结果，使所有概率总和为1
    normalizeResults(results) {
      const sum = Object.values(results).reduce((acc, val) => acc + val, 0);
      for (const key in results) {
        results[key] /= sum;
      }
    },
    
    // 根据概率确定疾病类型
    determineDiseaseTypes(results) {
      const diseaseTypes = [];
      const threshold = 0.15; // 概率阈值，超过此值视为检测到疾病
      
      for (const [key, value] of Object.entries(results)) {
        if (key !== 'N' && value > threshold) {
          diseaseTypes.push(this.getDiseaseLabel(key));
        }
      }
      
      return diseaseTypes;
    },
    
    // 获取疾病标签
    getDiseaseLabel(key) {
      return this.diseaseMapping[key] || key;
    },
    
    // 获取概率颜色
    getProbabilityColor(value) {
      if (value >= 0.7) {
        return '#e53e3e'; // 高风险 - 红色
      } else if (value >= 0.4) {
        return '#dd6b20'; // 中风险 - 橙色
      } else if (value >= 0.2) {
        return '#d69e2e'; // 低风险 - 黄色
      } else {
        return '#38a169'; // 正常 - 绿色
      }
    },
    
    // 获取诊断风险等级
    getDiagnosisRiskLevel() {
      if (!this.diagnosisResult) return 'low';
      
      let maxProbability = 0;
      
      // 检查综合结果
      if (this.diagnosisResult.combined_result) {
        for (const [key, value] of Object.entries(this.diagnosisResult.combined_result)) {
          if (key !== 'N' && value > maxProbability) {
            maxProbability = value;
          }
        }
      }
      
      // 检查左眼结果
      if (this.diagnosisResult.left_result) {
        for (const [key, value] of Object.entries(this.diagnosisResult.left_result)) {
          if (key !== 'N' && value > maxProbability) {
            maxProbability = value;
          }
        }
      }
      
      // 检查右眼结果
      if (this.diagnosisResult.right_result) {
        for (const [key, value] of Object.entries(this.diagnosisResult.right_result)) {
          if (key !== 'N' && value > maxProbability) {
            maxProbability = value;
          }
        }
      }
      
      if (maxProbability >= 0.7) {
        return 'high';
      } else if (maxProbability >= 0.4) {
        return 'medium';
      } else {
        return 'low';
      }
    },
    
    // 获取诊断风险文本
    getDiagnosisRiskText() {
      const riskLevel = this.getDiagnosisRiskLevel();
      
      if (riskLevel === 'high') {
        return '高风险';
      } else if (riskLevel === 'medium') {
        return '中等风险';
      } else {
        return '低风险';
      }
    },
    
    // 获取诊断风险描述
    getDiagnosisRiskDescription() {
      const riskLevel = this.getDiagnosisRiskLevel();
      
      if (riskLevel === 'high') {
        return '检测到严重眼部异常，建议尽快就医';
      } else if (riskLevel === 'medium') {
        return '检测到眼部异常，建议近期就医检查';
      } else {
        return '未检测到明显异常，建议定期检查';
      }
    },
    
    // 获取最高概率疾病
    getHighestDisease(eye) {
      const result = this.diagnosisResult[`${eye}_result`];
      if (!result) return null;
      
      let maxKey = null;
      let maxValue = 0;
      
      for (const [key, value] of Object.entries(result)) {
        if (key !== 'N' && value > maxValue) {
          maxKey = key;
          maxValue = value;
        }
      }
      
      return maxKey ? this.getDiseaseLabel(maxKey) : null;
    },
    
    // 获取疾病描述
    getDiseaseDescription(disease) {
      return this.diseaseDescriptions[disease] || '暂无详细描述';
    },
    
    // 检查是否有疾病
    hasDiseases() {
      if (!this.diagnosisResult) return false;
      
      if (this.diagnosisResult.combined_disease_types && this.diagnosisResult.combined_disease_types.length > 0) {
        return true;
      }
      
      if (this.diagnosisResult.left_disease_types && this.diagnosisResult.left_disease_types.length > 0) {
        return true;
      }
      
      if (this.diagnosisResult.right_disease_types && this.diagnosisResult.right_disease_types.length > 0) {
        return true;
      }
      
      return false;
    },
    
    // 获取建议文本
    getRecommendationText() {
      const riskLevel = this.getDiagnosisRiskLevel();
      
      if (riskLevel === 'high') {
        return '建议尽快前往眼科医院进行详细检查和治疗方案制定，以防止病情进一步恶化。';
      } else if (riskLevel === 'medium') {
        return '建议在近期（1-2周内）前往眼科门诊进行进一步检查，明确诊断并获取专业治疗建议。';
      } else {
        return '建议在方便时前往眼科进行常规检查，确认诊断并获取专业建议。';
      }
    },
    
    // 获取健康建议
    getHealthRecommendations() {
      const recommendations = [
        '保持良好用眼习惯，每用眼1小时休息10分钟，远眺放松眼部肌肉',
        '保持均衡饮食，多摄入富含维生素A、C、E和叶黄素的食物，如胡萝卜、菠菜、蓝莓等',
        '避免长时间使用电子设备，使用时保持适当距离和良好光线',
        '定期进行眼部检查，建议每年至少一次全面眼科检查'
      ];
      
      if (this.hasDiseases()) {
        const diseases = [];
        
        if (this.diagnosisResult.combined_disease_types) {
          diseases.push(...this.diagnosisResult.combined_disease_types);
        } else {
          if (this.diagnosisResult.left_disease_types) {
            diseases.push(...this.diagnosisResult.left_disease_types);
          }
          if (this.diagnosisResult.right_disease_types) {
            diseases.push(...this.diagnosisResult.right_disease_types);
          }
        }
        
        // 根据检测到的疾病添加特定建议
        if (diseases.includes('糖尿病视网膜病变') || diseases.includes('糖尿病')) {
          recommendations.push('严格控制血糖水平，遵循医生的糖尿病管理建议');
          recommendations.push('定期进行眼底检查，糖尿病患者建议每年至少检查一次');
        }
        
        if (diseases.includes('青光眼')) {
          recommendations.push('避免剧烈运动和低头姿势，这可能会增加眼内压');
          recommendations.push('按时使用医生处方的降眼压药物，不要擅自停药');
        }
        
        if (diseases.includes('白内障')) {
          recommendations.push('在户外活动时佩戴防紫外线眼镜，减少紫外线对晶状体的损伤');
          recommendations.push('避免吸烟，减少氧化应激对晶状体的损害');
        }
        
        if (diseases.includes('年龄相关性黄斑变性') || diseases.includes('黄斑变性')) {
          recommendations.push('增加富含叶黄素和玉米黄质的食物摄入，如深绿色蔬菜、玉米和蛋黄');
          recommendations.push('使用AREDS配方补充剂（请咨询医生后使用）');
        }
      }
      
      return recommendations;
    },
    
    // 获取后续跟进文本
    getFollowUpText() {
      const riskLevel = this.getDiagnosisRiskLevel();
      
      if (riskLevel === 'high') {
        return '建议在就医后2-4周内进行复查，评估治疗效果和病情进展。请务必遵循专科医生的建议，按时服药和复诊。';
      } else if (riskLevel === 'medium') {
        return '建议在首次就医后1-3个月内进行复查，评估病情变化。请记录任何视力变化或不适症状，并在复诊时告知医生。';
      } else {
        return '建议每年进行一次常规眼科检查，保持良好的眼部健康习惯。如有任何视力变化或不适，请及时就医。';
      }
    },
    
    // 重置诊断
    resetDiagnosis() {
      this.diagnosisResult = null;
      this.leftEyeFile = null;
      this.rightEyeFile = null;
      this.leftEyePreview = null;
      this.rightEyePreview = null;
      this.errors = {
        patient: '',
        images: ''
      };
    },
    
    // 保存报告为PDF
    async saveReport() {
      if (!this.diagnosisResult || !this.$refs.reportContent) {
        this.showToast('无法生成报告，请先完成诊断', 'error');
        return;
      }
      
      this.isExporting = true;
      
      try {
        // 设置PDF文件名
        const patientName = this.selectedPatient.patientName;
        const date = new Date();
        const dateStr = `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;
        this.pdfOptions.filename = `${patientName}_眼部健康诊断报告_${dateStr}.pdf`;
        
        // 创建一个克隆的报告内容，以便于修改样式而不影响原始DOM
        const reportContent = this.$refs.reportContent.cloneNode(true);
        
        // 添加打印样式
        const style = document.createElement('style');
        style.textContent = `
          @font-face {
            font-family: 'SimSun';
            src: url('https://cdn.jsdelivr.net/npm/noto-sans-sc@2023.12.31/NotoSansSC-Regular.otf') format('opentype');
            font-weight: normal;
            font-style: normal;
          }
          body {
            font-family: 'SimSun', sans-serif;
          }
          .report-actions-top {
            display: none !important;
          }
          .diagnosis-results {
            background-color: white;
            padding: 20px;
          }
          .eye-image {
            max-width: 100%;
            height: auto;
          }
        `;
        reportContent.appendChild(style);
        
        // 使用html2pdf生成PDF
        const opt = {
          margin: 10,
          filename: this.pdfOptions.filename,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { 
            scale: 2, 
            useCORS: true,
            letterRendering: true,
            logging: false
          },
          jsPDF: { 
            unit: 'mm', 
            format: 'a4', 
            orientation: 'portrait',
            compress: true
          },
          fontFaces: [
            {
              family: 'SimSun',
              style: 'normal'
            }
          ]
        };
        
        // 添加中文字体支持
        await this.loadChineseFont();
        
        await html2pdf().from(this.$refs.reportContent).set(opt).save();
        
        this.showToast('报告已成功导出为PDF', 'success');
      } catch (error) {
        console.error('PDF导出错误:', error);
        this.showToast('PDF导出失败，请稍后重试', 'error');
      } finally {
        this.isExporting = false;
      }
    },
    
    // 加载中文字体
    async loadChineseFont() {
      return new Promise((resolve, reject) => {
        // 检查是否已加载中文字体
        const fontTest = document.createElement('span');
        fontTest.style.fontFamily = 'SimSun';
        fontTest.style.visibility = 'hidden';
        fontTest.textContent = '测试中文';
        document.body.appendChild(fontTest);
        
        // 如果已加载字体，直接返回
        if (document.fonts && document.fonts.check('12px SimSun')) {
          document.body.removeChild(fontTest);
          resolve();
          return;
        }
        
        // 加载中文字体
        const fontFace = new FontFace('SimSun', 'url(https://cdn.jsdelivr.net/npm/noto-sans-sc@2023.12.31/NotoSansSC-Regular.otf)');
        
        fontFace.load().then((loadedFace) => {
          document.fonts.add(loadedFace);
          document.body.removeChild(fontTest);
          resolve();
        }).catch((error) => {
          console.error('中文字体加载失败:', error);
          document.body.removeChild(fontTest);
          // 即使字体加载失败，也继续生成PDF
          resolve();
        });
      });
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
.eye-diagnosis-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f7fa;
  color: #2c3e50;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

/* 页面标题 */
.page-header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header h1 {
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

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* 表单容器 */
.form-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}

.form-container h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
  border-bottom: 2px solid #f0f2f5;
  padding-bottom: 0.75rem;
}

.mt-6 {
  margin-top: 1.5rem;
}

/* 患者列表 */
.loading-patients {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #718096;
}

.loading-spinner-small {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(79, 172, 254, 0.2);
  border-radius: 50%;
  border-top-color: #4facfe;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.no-patients {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #718096;
}

.no-patients svg {
  margin-bottom: 1rem;
  color: #cbd5e0;
}

.btn-refresh {
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
  margin-top: 1rem;
}

.btn-refresh:hover {
  background-color: #e2e8f0;
}

.search-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #4facfe;
  box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.2);
}

.patients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.patient-card {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.patient-card:hover {
  background-color: #f0f7ff;
}

.patient-card.selected {
  border-color: #4facfe;
  background-color: #f0f7ff;
}

.patient-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #e6f7ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4facfe;
  flex-shrink: 0;
}

.patient-info {
  flex: 1;
  min-width: 0;
}

.patient-name {
  margin: 0 0 0.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

.patient-details {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #718096;
  margin-bottom: 0.25rem;
}

.patient-record {
  font-size: 0.85rem;
  color: #718096;
}

.record-label {
  color: #4a5568;
  font-weight: 500;
  margin-right: 0.25rem;
}

.patient-select-indicator {
  color: #4facfe;
}

/* 眼部图像上传 */
.eye-upload-container {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.eye-upload {
  flex: 1;
}

.eye-upload h3 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.upload-area {
  border: 2px dashed #cbd5e0;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  height: 200px;
  background-color: #f8fafc;
}

.upload-area:hover {
  border-color: #4facfe;
  background-color: #f0f7ff;
}

.upload-area.has-image {
  border-style: solid;
  padding: 0;
  overflow: hidden;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #718096;
}

.upload-placeholder svg {
  margin-bottom: 1rem;
  color: #4facfe;
}

.eye-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-image:hover {
  background-color: rgba(255, 255, 255, 1);
  transform: scale(1.1);
}

.file-input {
  display: none;
}

.form-note {
  font-size: 0.9rem;
  color: #718096;
  margin-bottom: 1.5rem;
}

/* 表单操作 */
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-submit {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

/* 诊断结果 */
.diagnosis-results {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}

.results-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
  border-bottom: 2px solid #f0f2f5;
  padding-bottom: 1rem;
}

.report-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.report-title h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #2c3e50;
}

.report-id {
  font-size: 0.9rem;
  color: #718096;
}

.patient-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin: 1rem 0;
}

.patient-info-item {
  display: flex;
  align-items: center;
}

.patient-info-item .label {
  font-weight: 500;
  margin-right: 0.5rem;
  color: #4a5568;
}

.patient-info-item .value {
  color: #2c3e50;
}

.report-actions-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

/* 结果部分 */
.result-section {
  margin-bottom: 2rem;
}

.result-section h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.result-section h3 svg {
  color: #4facfe;
}

.result-card {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.result-overview {
  margin-bottom: 1.5rem;
}

.risk-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.risk-indicator.high {
  background-color: #fff5f5;
  border: 1px solid #fed7d7;
}

.risk-indicator.medium {
  background-color: #fffaf0;
  border: 1px solid #feebc8;
}

.risk-indicator.low {
  background-color: #f0fff4;
  border: 1px solid #c6f6d5;
}

.risk-level {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.risk-indicator.high .risk-level {
  color: #e53e3e;
}

.risk-indicator.medium .risk-level {
  color: #dd6b20;
}

.risk-indicator.low .risk-level {
  color: #38a169;
}

.risk-description {
  text-align: center;
  color: #4a5568;
}

.result-summary {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.result-item {
  display: grid;
  grid-template-columns: 150px 1fr 60px;
  align-items: center;
  gap: 1rem;
}

.disease-name {
  font-weight: 500;
  color: #4a5568;
}

.probability-bar {
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.probability-fill {
  height: 100%;
  border-radius: 4px;
}

.probability-value {
  font-size: 0.9rem;
  color: #718096;
  text-align: right;
}

.disease-types {
  margin-top: 1.5rem;
}

.disease-types h4 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
  color: #4a5568;
}

.disease-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.disease-tag {
  background-color: #ebf8ff;
  color: #2b6cb0;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.9rem;
}

.disease-description {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 1rem;
  margin-top: 1rem;
}

.disease-description h5 {
  font-size: 1rem;
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.disease-description p {
  margin: 0;
  color: #4a5568;
  line-height: 1.6;
}

.no-disease {
  margin-top: 1.5rem;
  color: #38a169;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 眼睛结果布局 */
.eyes-results {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.eyes-results .result-section {
  flex: 1;
  margin-bottom: 0;
}

.eye-images {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.original-image, .heatmap-image {
  flex: 1;
}

.original-image h4, .heatmap-image h4 {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: #4a5568;
  text-align: center;
}

.eye-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.heatmap-container {
  position: relative;
}

.heatmap-legend {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #718096;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.high {
  background-color: #e53e3e;
}

.legend-color.medium {
  background-color: #dd6b20;
}

.legend-color.low {
  background-color: #d69e2e;
}

/* 诊断总结 */
.diagnosis-summary {
  margin-bottom: 2rem;
}

.diagnosis-summary h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.summary-card {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.summary-content {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.summary-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-icon.high {
  background-color: #fff5f5;
  color: #e53e3e;
}

.summary-icon.medium {
  background-color: #fffaf0;
  color: #dd6b20;
}

.summary-icon.low {
  background-color: #f0fff4;
  color: #38a169;
}

.summary-text {
  flex: 1;
}

.summary-text p {
  margin: 0;
  line-height: 1.6;
}

.recommendations {
  margin-bottom: 1.5rem;
}

.recommendations h4, .follow-up h4 {
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
  color: #2c3e50;
}

.recommendations ul {
  margin: 0;
  padding-left: 1.5rem;
}

.recommendations li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.follow-up {
  margin-bottom: 1.5rem;
}

.follow-up p {
  margin: 0;
  line-height: 1.6;
}

.disclaimer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  font-size: 0.9rem;
  color: #718096;
}

/* 报告操作 */
.btn-print, .btn-save {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-print {
  background-color: #edf2f7;
  color: #4a5568;
  border: 1px solid #e2e8f0;
}

.btn-print:hover {
  background-color: #e2e8f0;
}

.btn-save {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border: none;
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 加载指示器 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
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

.loading-overlay p {
  color: #2c3e50;
  font-size: 1.1rem;
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

/* 动画 */
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

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .eye-upload-container {
    flex-direction: column;
  }
  
  .eyes-results {
    flex-direction: column;
  }
  
  .eye-images {
    flex-direction: column;
  }
  
  .report-actions-top {
    flex-direction: column;
    gap: 1rem;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .btn-print, .btn-save {
    flex: 1;
    justify-content: center;
  }
  
  .result-item {
    grid-template-columns: 100px 1fr 60px;
  }
  
  .patients-grid {
    grid-template-columns: 1fr;
  }
}

/* 打印样式 */
@media print {
  .eye-diagnosis-container {
    background-color: white;
  }
  
  .page-header {
    background: none;
    color: #2c3e50;
    box-shadow: none;
    padding: 1rem;
  }
  
  .btn-back, .action-buttons {
    display: none;
  }
  
  .diagnosis-results {
    box-shadow: none;
    padding: 0;
  }
  
  .result-card {
    box-shadow: none;
    border: 1px solid #e2e8f0;
  }
}

/* 错误消息 */
.error-message {
  color: #e53e3e;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>
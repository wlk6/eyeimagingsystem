<template>
  <div class="help-center-container">
    <div class="header">
      <div class="header-content">
        <h1>医疗问答中心</h1>
        <p class="subtitle">找到您需要的专业解答</p>
      </div>
    </div>

    <div class="search-container">
      <div class="search-box">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="search-icon">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input 
          type="text" 
          v-model="filter.search" 
          placeholder="搜索问题或关键词..." 
          @input="handleSearch"
          class="search-input"
        >
        <button v-if="filter.search" @click="clearSearch" class="clear-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <div class="filter-section">
      <div class="category-tabs">
        <button 
          class="category-tab" 
          :class="{ active: filter.category === 'all' }" 
          @click="filter.category = 'all'"
        >
          全部问题
        </button>
        <button 
          class="category-tab" 
          :class="{ active: filter.category === 'functionality' }" 
          @click="filter.category = 'functionality'"
        >
          功能使用
        </button>
        <button 
          class="category-tab" 
          :class="{ active: filter.category === 'disease' }" 
          @click="filter.category = 'disease'"
        >
          疾病预防与治疗
        </button>
        <button 
          class="category-tab" 
          :class="{ active: filter.category === 'system' }" 
          @click="filter.category = 'system'"
        >
          系统问题
        </button>
      </div>
    </div>

    <div class="results-info" v-if="filter.search">
      <p>
        <span class="results-count">{{ filteredFAQs.length }}</span> 条结果匹配 
        <span class="search-term">"{{ filter.search }}"</span>
      </p>
    </div>

    <div class="faq-list" v-if="filteredFAQs.length > 0">
      <div 
        class="faq-item" 
        v-for="faq in filteredFAQs" 
        :key="faq.id"
        :class="{ 'expanded': faq.isExpanded }"
      >
        <div class="faq-question" @click="toggleAnswer(faq.id)">
          <div class="question-icon" :class="getCategoryClass(faq.category)">
            <svg v-if="faq.category === 'functionality'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
            <svg v-else-if="faq.category === 'disease'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
            </svg>
            <svg v-else-if="faq.category === 'system'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </div>
          <h3 v-html="highlightKeywords(faq.question)"></h3>
          <button class="toggle-btn" :class="{ 'expanded': faq.isExpanded }">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
        </div>
        <transition name="fade">
          <div class="faq-answer" v-if="faq.isExpanded">
            <div class="answer-content" v-html="highlightKeywords(faq.answer)"></div>
            <div class="answer-footer" v-if="faq.relatedLinks && faq.relatedLinks.length">
              <div class="related-links">
                <h4>相关链接:</h4>
                <ul>
                  <li v-for="(link, index) in faq.relatedLinks" :key="index">
                    <a :href="link.url" target="_blank">{{ link.text }}</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="feedback-section">
              <p>这个回答对您有帮助吗？</p>
              <div class="feedback-buttons">
                <button class="feedback-btn" @click="provideFeedback(faq.id, true)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
                  </svg>
                  有帮助
                </button>
                <button class="feedback-btn" @click="provideFeedback(faq.id, false)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path>
                  </svg>
                  没帮助
                </button>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>

    <div class="no-results" v-else>
      <div class="no-results-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          <line x1="8" y1="11" x2="14" y2="11"></line>
        </svg>
      </div>
      <h3>未找到匹配的结果</h3>
      <p>尝试使用不同的关键词或浏览其他类别</p>
      <button class="reset-btn" @click="resetFilters">重置筛选条件</button>
    </div>

    <div class="help-footer">
      <p>没有找到您需要的答案？</p>
      <button class="contact-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
        </svg>
        联系客服
      </button>
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
  name: 'HelpCenter',
  data() {
    return {
      filter: {
        category: 'all',
        search: ''
      },
      toast: {
        show: false,
        message: '',
        type: 'success'
      },
      FAQs: [
        {
          id: 1,
          question: '如何查看诊断历史？',
          answer: '您可以在系统首页找到"诊断历史"选项，点击进入后可以查看所有历史诊断记录。您还可以使用筛选功能，按时间、类型和结果进行筛选。<br><br>在诊断历史页面，您可以：<ul><li>查看详细的诊断报告</li><li>比较不同时间的诊断结果</li><li>追踪眼部健康变化趋势</li><li>将报告分享给其他医生</li></ul>',
          category: 'functionality',
          isExpanded: false,
          relatedLinks: [
            { text: '诊断历史使用指南', url: '#' },
            { text: '如何解读诊断报告', url: '#' }
          ]
        },
        {
          id: 2,
          question: '如何下载诊断报告？',
          answer: '在诊断历史页面，每个诊断记录右侧都有"下载"按钮，点击即可下载对应的诊断报告。报告将以PDF格式保存到您的设备。<br><br>下载的报告包含完整的诊断信息，包括眼部图像、AI分析结果、风险评估和医生建议。您可以将报告打印出来或通过电子邮件分享给其他医疗专业人士。',
          category: 'functionality',
          isExpanded: false
        },
        {
          id: 3,
          question: '如何预约新的诊断？',
          answer: '您可以在系统首页点击"预约诊断"按钮，选择需要的诊断类型和时间，填写相关信息后提交预约请求。系统会尽快处理您的预约并通知您。<br><br>预约流程：<ol><li>登录系统并点击"预约诊断"</li><li>选择诊断类型（常规检查、专项检查等）</li><li>选择合适的日期和时间段</li><li>填写患者信息和症状描述</li><li>提交预约申请</li></ol>',
          category: 'functionality',
          isExpanded: false
        },
        {
          id: 4,
          question: '如何修改个人信息？',
          answer: '您可以在个人中心页面查看和修改个人信息，包括姓名、联系方式、地址等。修改后点击保存按钮即可更新信息。<br><br>请确保您的联系信息始终保持最新，这样系统可以及时向您发送重要通知，如预约确认、检查结果和随访提醒。',
          category: 'functionality',
          isExpanded: false
        },
        {
          id: 5,
          question: '如何添加家庭成员信息？',
          answer: '在个人中心页面，点击"家庭成员管理"选项，然后点击"添加成员"按钮，填写家庭成员的信息并保存。<br><br>添加家庭成员后，您可以为他们预约诊断、查看他们的诊断历史，并管理他们的健康记录。这对于需要照顾老人和孩子的用户特别有用。',
          category: 'functionality',
          isExpanded: false
        },
        {
          id: 6,
          question: '白内障的常见症状是什么？',
          answer: '白内障的常见症状包括视力模糊、对光线敏感、夜间视力下降、颜色感知减弱、重影、光晕和眩光等。如果您出现这些症状，建议尽快就医检查。<br><br>白内障是一种常见的眼部疾病，主要是由于晶状体变得混浊，导致光线无法正常通过晶状体到达视网膜。早期发现和治疗可以有效防止视力进一步下降。',
          category: 'disease',
          isExpanded: false,
          relatedLinks: [
            { text: '白内障预防指南', url: '#' },
            { text: '白内障手术常见问题', url: '#' }
          ]
        },
        {
          id: 7,
          question: '如何预防青光眼？',
          answer: '预防青光眼的方法包括定期进行眼压检查、保持健康的生活方式、避免长时间用眼、控制血压和血糖等。如果有青光眼家族史，应更加关注眼部健康。<br><br>青光眼是一组导致视神经损伤的眼病，通常与眼内压升高有关。早期青光眼通常没有明显症状，因此定期检查对于早期发现和治疗至关重要。',
          category: 'disease',
          isExpanded: false
        },
        {
          id: 8,
          question: '糖尿病视网膜病变的早期症状有哪些？',
          answer: '糖尿病视网膜病变的早期可能没有明显症状，随着病情发展可能出现视力模糊、眼前黑影、视物变形等。糖尿病患者应定期进行眼底检查，以便早期发现和治疗。<br><br>糖尿病视网膜病变是糖尿病的常见并发症，由于长期高血糖导致视网膜血管损伤。定期的眼底检查对于糖尿病患者至关重要，即使没有任何视力问题。',
          category: 'disease',
          isExpanded: false,
          relatedLinks: [
            { text: '糖尿病患者眼部护理指南', url: '#' }
          ]
        },
        {
          id: 9,
          question: '黄斑变性的治疗方法有哪些？',
          answer: '黄斑变性的治疗方法包括药物治疗（如抗血管内皮生长因子注射）、激光治疗、光动力疗法和手术治疗等。具体治疗方案应根据病情的严重程度和类型由医生决定。<br><br>黄斑变性是一种影响视网膜中央区域（黄斑）的疾病，是老年人视力丧失的主要原因之一。早期诊断和治疗对于保存视力至关重要。',
          category: 'disease',
          isExpanded: false
        },
        {
          id: 10,
          question: '如何缓解眼睛疲劳？',
          answer: '缓解眼睛疲劳的方法包括：<ul><li>定期休息：遵循20-20-20原则，每20分钟看远处20英尺（约6米）外的物体20秒</li><li>保持正确的用眼距离和姿势</li><li>使用人工泪液缓解干眼</li><li>保持室内适当湿度</li><li>调整屏幕亮度和对比度</li><li>考虑使用防蓝光眼镜</li><li>定期进行眼部按摩和热敷</li></ul>',
          category: 'disease',
          isExpanded: false
        },
        {
          id: 11,
          question: '系统支持哪些浏览器？',
          answer: '我们的系统支持所有主流现代浏览器，包括：<ul><li>Google Chrome（推荐，版本88及以上）</li><li>Mozilla Firefox（版本85及以上）</li><li>Microsoft Edge（基于Chromium的版本，79及以上）</li><li>Apple Safari（版本14及以上）</li></ul>为了获得最佳体验，我们建议使用最新版本的浏览器，并确保您的浏览器已启用JavaScript和Cookie。',
          category: 'system',
          isExpanded: false
        },
        {
          id: 12,
          question: '如何重置密码？',
          answer: '重置密码的步骤如下：<ol><li>在登录页面点击"忘记密码"链接</li><li>输入您注册时使用的电子邮件地址</li><li>系统将向您的邮箱发送一封包含重置链接的邮件</li><li>点击邮件中的链接，设置新密码</li><li>使用新密码登录系统</li></ol>如果您没有收到重置邮件，请检查垃圾邮件文件夹，或联系客服获取帮助。',
          category: 'system',
          isExpanded: false
        },
        {
          id: 13,
          question: '系统数据安全性如何保障？',
          answer: '我们采取多层次的安全措施保护您的数据：<ul><li>所有数据传输使用SSL/TLS加密</li><li>患者数据存储在符合医疗行业标准的安全服务器中</li><li>定期进行安全审计和漏洞扫描</li><li>严格的访问控制和权限管理</li><li>定期数据备份和灾难恢复计划</li><li>符合相关医疗数据保护法规和标准</li></ul>我们将患者隐私和数据安全视为最高优先级。',
          category: 'system',
          isExpanded: false,
          relatedLinks: [
            { text: '隐私政策', url: '#' },
            { text: '数据安全白皮书', url: '#' }
          ]
        },
        {
          id: 14,
          question: '系统是否支持移动设备访问？',
          answer: '是的，我们的系统采用响应式设计，可以在各种设备上使用，包括台式电脑、笔记本电脑、平板电脑和智能手机。<br><br>此外，我们还提供iOS和Android平台的移动应用，您可以从App Store或Google Play商店下载安装。移动应用提供了更加便捷的访问方式和一些专为移动设备优化的功能。',
          category: 'system',
          isExpanded: false
        },
        {
          id: 15,
          question: '干眼症的日常护理方法有哪些？',
          answer: '干眼症的日常护理方法包括：<ul><li>定期使用人工泪液</li><li>避免长时间使用电子设备</li><li>保持室内适当湿度</li><li>佩戴防风眼镜，减少眼部暴露在风、灰尘中</li><li>注意眨眼，特别是在使用电脑时</li><li>热敷眼睛，促进睑板腺分泌</li><li>保持充分休息和睡眠</li><li>增加富含omega-3脂肪酸的食物摄入</li><li>避免烟草和酒精</li></ul>如果症状持续或加重，请咨询眼科医生。',
          category: 'disease',
          isExpanded: false
        }
      ]
    };
  },
  computed: {
    filteredFAQs() {
      let result = this.FAQs;

      // 按类别筛选
      if (this.filter.category !== 'all') {
        result = result.filter(faq => faq.category === this.filter.category);
      }

      // 按关键词搜索
      if (this.filter.search) {
        const searchTerm = this.filter.search.toLowerCase();
        result = result.filter(faq => 
          faq.question.toLowerCase().includes(searchTerm) || 
          faq.answer.toLowerCase().includes(searchTerm)
        );
      }

      return result;
    }
  },
  methods: {
    toggleAnswer(id) {
      this.FAQs.forEach(faq => {
        if (faq.id === id) {
          faq.isExpanded = !faq.isExpanded;
        }
      });
    },
    handleSearch() {
      // 实时筛选，不需要额外操作
    },
    highlightKeywords(text) {
      if (!this.filter.search || this.filter.search.trim() === '') return text;
      
      // 转义正则表达式中的特殊字符
      const escapeRegExp = (string) => {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      };
      
      const searchTerms = this.filter.search.trim().split(/\s+/);
      let highlightedText = text;
      
      searchTerms.forEach(term => {
        if (term) {
          const regex = new RegExp(`(${escapeRegExp(term)})`, 'gi');
          highlightedText = highlightedText.replace(regex, '<span class="highlight">$1</span>');
        }
      });
      
      return highlightedText;
    },
    clearSearch() {
      this.filter.search = '';
    },
    resetFilters() {
      this.filter.category = 'all';
      this.filter.search = '';
    },
    getCategoryClass(category) {
      const categoryClasses = {
        'functionality': 'category-functionality',
        'disease': 'category-disease',
        'system': 'category-system'
      };
      return categoryClasses[category] || '';
    },
    provideFeedback(id, isHelpful) {
      // 在实际应用中，这里可以发送反馈到服务器
      this.showToast(isHelpful ? '感谢您的反馈！' : '感谢您的反馈，我们会继续改进', 'success');
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
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  color: #2c3e50;
  background-color: #f5f7fa;
}

.help-center-container {
  max-width: 900px;
  margin: 40px auto;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 0;
  transition: all 0.3s ease;
  overflow: hidden;
}

/* 页面标题 */
.header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  padding: 2.5rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.3;
}

.header-content {
  position: relative;
  z-index: 1;
}

.header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  font-weight: 300;
}

/* 搜索框 */
.search-container {
  padding: 0 2rem;
  margin-top: -25px;
  position: relative;
  z-index: 10;
}

.search-box {
  background-color: white;
  border-radius: 50px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.search-box:focus-within {
  border-color: #4facfe;
  box-shadow: 0 5px 25px rgba(79, 172, 254, 0.2);
}

.search-icon {
  color: #4facfe;
  margin-right: 0.75rem;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1.1rem;
  color: #2c3e50;
}

.search-input::placeholder {
  color: #a0aec0;
}

.clear-btn {
  background: none;
  border: none;
  color: #cbd5e0;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.clear-btn:hover {
  color: #718096;
}

/* 筛选部分 */
.filter-section {
  padding: 2rem;
  padding-top: 1.5rem;
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.category-tab {
  padding: 0.6rem 1.2rem;
  background-color: #f1f5f9;
  border: none;
  border-radius: 50px;
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.category-tab:hover {
  background-color: #e2e8f0;
  color: #334155;
}

.category-tab.active {
  background-color: #4facfe;
  color: white;
  box-shadow: 0 4px 10px rgba(79, 172, 254, 0.3);
}

/* 结果信息 */
.results-info {
  padding: 0 2rem;
  margin-bottom: 1rem;
}

.results-info p {
  color: #64748b;
  font-size: 0.95rem;
}

.results-count {
  font-weight: 600;
  color: #334155;
}

.search-term {
  background-color: #e6f7ff;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
  color: #0284c7;
}

/* FAQ列表 */
.faq-list {
  padding: 0 2rem 2rem;
}

.faq-item {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.faq-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.faq-item.expanded {
  border-color: #4facfe;
  box-shadow: 0 4px 15px rgba(79, 172, 254, 0.15);
}

.faq-question {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  cursor: pointer;
  position: relative;
  gap: 1rem;
}

.question-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.category-functionality {
  background-color: #e6f7ff;
  color: #0284c7;
}

.category-disease {
  background-color: #fef3c7;
  color: #d97706;
}

.category-system {
  background-color: #e0e7ff;
  color: #4f46e5;
}

.faq-question h3 {
  flex: 1;
  color: #334155;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
  line-height: 1.5;
}

.toggle-btn {
  background: none;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.toggle-btn:hover {
  background-color: #f1f5f9;
  color: #64748b;
}

.toggle-btn.expanded {
  transform: rotate(45deg);
  color: #4facfe;
}

.faq-answer {
  padding: 0 1.25rem 1.25rem 1.25rem;
  margin-left: 3.5rem;
  color: #475569;
  line-height: 1.7;
  font-size: 1rem;
}

.answer-content {
  margin-bottom: 1.5rem;
}

.answer-content ul, 
.answer-content ol {
  padding-left: 1.5rem;
  margin: 1rem 0;
}

.answer-content li {
  margin-bottom: 0.5rem;
}

.answer-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.related-links h4 {
  font-size: 0.95rem;
  color: #334155;
  margin-bottom: 0.75rem;
}

.related-links ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.related-links li {
  margin-bottom: 0.5rem;
}

.related-links a {
  color: #4facfe;
  text-decoration: none;
  font-size: 0.95rem;
  display: inline-flex;
  align-items: center;
}

.related-links a:hover {
  text-decoration: underline;
}

.feedback-section {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.feedback-section p {
  font-size: 0.95rem;
  color: #64748b;
  margin-bottom: 0.75rem;
}

.feedback-buttons {
  display: flex;
  gap: 1rem;
}

.feedback-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: #f8fafc;
  color: #64748b;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.feedback-btn:hover {
  background-color: #f1f5f9;
  color: #334155;
  border-color: #cbd5e0;
}

/* 无结果状态 */
.no-results {
  padding: 3rem 2rem;
  text-align: center;
}

.no-results-icon {
  margin-bottom: 1.5rem;
  color: #94a3b8;
}

.no-results h3 {
  font-size: 1.3rem;
  color: #334155;
  margin-bottom: 0.75rem;
}

.no-results p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.reset-btn {
  padding: 0.75rem 1.5rem;
  background-color: #4facfe;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.reset-btn:hover {
  background-color: #3b9eef;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(79, 172, 254, 0.2);
}

/* 页脚 */
.help-footer {
  background-color: #f8fafc;
  padding: 2rem;
  text-align: center;
  border-top: 1px solid #e2e8f0;
}

.help-footer p {
  color: #64748b;
  margin-bottom: 1rem;
}

.contact-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.contact-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(79, 172, 254, 0.2);
}

/* 高亮样式 */
.highlight {
  background-color: rgba(255, 245, 157, 0.7);
  font-weight: 500;
  border-radius: 3px;
  padding: 0 2px;
  box-shadow: 0 0 0 1px rgba(255, 220, 0, 0.3);
}

/* 动画 */
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
  max-height: 1000px;
  opacity: 1;
  overflow: hidden;
}

.fade-enter, .fade-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}

/* 消息提示 */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1100;
}

.toast-content {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease;
}

.toast-content.success {
  background-color: #dcfce7;
  color: #166534;
}

.toast-content.error {
  background-color: #fee2e2;
  color: #b91c1c;
}

.toast-content svg {
  margin-right: 0.75rem;
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
  .header {
    padding: 2rem 1.5rem;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .search-container {
    padding: 0 1.5rem;
  }
  
  .filter-section,
  .faq-list,
  .help-footer {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  
  .category-tabs {
    overflow-x: auto;
    padding-bottom: 0.5rem;
    flex-wrap: nowrap;
  }
  
  .category-tab {
    white-space: nowrap;
  }
  
  .faq-question {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .faq-answer {
    margin-left: 0;
  }
  
  .toggle-btn {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
  }
  
  .feedback-buttons {
    flex-direction: column;
  }
}
</style>
<template>
  <div class="container">
    <div>
      <vxe-grid ref="xGrid" 
                :columns="isCreating ? createColumns : fullColumns"
                :data="tableData"
                @toolbar-button-click="handleToolbar"
                   :proxy-config="gridOptions.proxyConfig"
                :border="gridOptions.border" 
                :showHeaderOverflow="gridOptions.showHeaderOverflow"
                :showOverflow="gridOptions.showOverflow" 
                :keepSource="gridOptions.keepSource"
                :id="gridOptions.id" 
                :height="gridOptions.height"
                :rowConfig="gridOptions.rowConfig" 
                :columnConfig="gridOptions.columnConfig"
                :customConfig="gridOptions.customConfig" 
                :printConfig="gridOptions.printConfig"
                :sortConfig="gridOptions.sortConfig" 
                :filterConfig="gridOptions.filterConfig"
                :pagerConfig="gridOptions.pagerConfig" 
                :form-config="formConfig"
                :toolbarConfig="gridOptions.toolbarConfig" 
                :importConfig="gridOptions.importConfig"
                :exportConfig="gridOptions.exportConfig" 
                :checkboxConfig="gridOptions.checkboxConfig"
                :editRules="gridOptions.editRules" 
                :editConfig="gridOptions.editConfig"
                 @proxy-query="handleProxyQuery">
        <template #avatarSlot="{ row }">
          <img :src="baseUrl + row.avatar" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />
        </template>
      </vxe-grid>
    </div>
  </div>
</template>

<script>
import XEUtils from 'xe-utils';
import VXETable from 'vxe-table';
import { MessageBox } from 'element-ui';
import 'vxe-table/lib/index.css';
import 'element-ui/lib/theme-chalk/index.css';
import { getInfo } from '../utils/storage'; 

const INFO_KEY = 'info';
const POSITION_MAP = {
  chief_physician: '主任医师',
  associate_physician: '副主任医师',
  attending_doctor: '主治医师'
};

const getToken = () => {
  const info = getInfo();
  return info.token || '';
};

export default {
  data() {
    return {
       allData: [],
      form: {
        doctor_id: '',
        doctor_name: '',
        gender: '',
        position: ''
      },
      formConfig: {
        titleWidth: 100,
        titleAlign: 'right',
        data: this.form, // 确保 data 绑定到 this.form
        items: [
          {
      field: 'doctor_id',
      title: '工号',
      span: 6,
      itemRender: { 
        name: '$input',
        model: { prop: 'doctor_id', event: 'input' }, // ✅ 正确绑定方式
        props: { placeholder: '请输入工号' }
      }
    },
    {
      field: 'doctor_name',
      title: '医生姓名',
      span: 6,
      itemRender: { 
        name: '$input',
        model: { prop: 'doctor_name', event: 'input' }, // ✅ 正确绑定方式
        props: { placeholder: '请输入医生姓名' }
      }
    },
          {
      field: 'gender',
      title: '性别',
      span: 5,
      itemRender: { 
        name: '$select',
        model: { prop: 'gender', event: 'input' }, // ✅ 使用 model 绑定
        options: [
          { label: '男', value: '男' },
          { label: '女', value: '女' }
        ],
        props: { placeholder: '请选择性别' }
      }
    },
    {
      field: 'position',
      title: '职位',
      span: 5,
      itemRender: { 
        name: '$select',
        model: { prop: 'position', event: 'input' }, // ✅ 使用 model 绑定
        options: [
          { label: '主任医师', value: 'chief_physician' },
          { label: '副主任医师', value: 'associate_physician' },
          { label: '主治医师', value: 'attending_doctor' }
        ],
        props: { placeholder: '请选择职位' }
      }
    }
        ]
      },
      baseUrl: 'http://121.196.228.176:9002/user',
      isCreating: false,
      tableData: [],
      serveApiUrl: 'http://121.196.228.176:9002/user/adminAddDoctorAccount',
      createColumns: [
        { type: 'checkbox', width: 60 },
        { field: 'doctor_name', title: '医生姓名', editRender: { name: 'input' } },
        { field: 'password', title: '密码', editRender: { name: 'input', props: { type: 'password' } }},
        { field: 'password_confirm', title: '确认密码', editRender: { name: 'input', props: { type: 'password' } } },
        { 
          field: 'gender', 
          title: '性别', 
          editRender: {
            name: '$select',
            options: [
              { label: '男', value: '男' },
              { label: '女', value: '女' }
            ]
          }
        },
        { 
          field: 'position',
          title: '职位',
          editRender: {
            name: '$select',
            options: [
              { label: '主任医师', value: 'chief_physician' },
              { label: '副主任医师', value: 'associate_physician' },
              { label: '主治医师', value: 'attending_doctor' }
            ]
          }
        }
      ],
      fullColumns: [
        { type: 'checkbox', width: 60 },
        { field: 'doctor_id', title: '医生ID' },
        { field: 'doctor_name', title: '医生姓名' },
        { field: 'phone', title: '电话' },
        { field: 'email', title: '邮箱' },
        { field: 'gender', title: '性别' },
        { 
          field: 'position', 
          title: '职位',
          formatter: ({ cellValue }) => POSITION_MAP[cellValue] || cellValue
        },
        { 
          field: 'avatar', 
          title: '头像',
          align: 'center',
          slots: {
            default: 'avatarSlot'
          }
        },
        { field: 'introduce', title: '个人简介', showOverflow: true }
      ],
      gridOptions: {
        border: true,
        showHeaderOverflow: true,
        showOverflow: true,
        keepSource: true,
        id: 'full_edit_1',
        height: 600,
        rowConfig: {
          keyField: 'id',
          isHover: true
        },
        proxyConfig: {
  autoLoad: true,
  form: true,
   props: {
              result: 'result',
              total: 'page.total'
            },
  ajax: {
    query: ({ page, form }) => {
      // 处理分页参数（与图片中的50条/页匹配）
      const params = {
        pageNum: page.currentPage,
        pageSize: 50, // 固定每页50条
        ...form
      }
      return fetch('http://121.196.228.176:9002/user/selectDoctor/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'token': getToken()
        },
        body: JSON.stringify(params)
      }).then(res => res.json())
       .then(data => {
                  this.allData = data.data; 
                  return {
                    page: {
                      total: data.data.length
                    },
                    result: data.data
                  };
                });
    }
  }
},
        columnConfig: {
          resizable: true,
          align: 'center',
          headerAlign: 'center'
        },
        customConfig: {
          storage: true,
          checkMethod(column) {
            if (['nickname', 'role'].includes(column.field)) {
              return false;
            }
            return true;
          }
        },
        printConfig: {
          columns: [
            { field: 'name' },
            { field: 'email' },
            { field: 'nickname' },
            { field: 'age' },
            { field: 'amount' }
          ]
        },
        sortConfig: {
          trigger: 'cell',
          remote: false
        },
        filterConfig: {
          remote: false
        },
        pagerConfig: {
          pageSize: 50,  
          pageSizes: [50, 100, 200, 500, 1000],  
          remote: false,  
          layout: 'total, sizes, prev, pager, next, jumper'  
        },
        toolbarConfig: {
          buttons: [
            { code: 'insert_actived', name: '新增' },
            { code: 'custom_delete', name: '直接删除' }, 
            { code: 'custom_quit', name: '取消' },
            { code: 'save', name: '保存', status: 'success' },
            { code: 'query', name: '查询', status: 'success' }
          ],
          refresh: true,
          import: true,
          export: true,
          print: true,
          zoom: true,
          custom: true
        },
        importConfig: {
          remote: true,
          types: ['xlsx'],
          modes: ['insert'],
          importMethod(file) {
            const $grid = this.$refs.xGrid;
            const formBody = new FormData();
            formBody.append('file', file);
            return fetch(`${this.serveApiUrl}/import`, {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${getToken()}` 
              },
              body: formBody
            })
              .then(response => response.json())
              .then(data => {
                VXETable.modal.message({
                  content: `成功导入 ${data.result.insertRows} 条记录！`,
                  status: 'success'
                });
                if ($grid) {
                  $grid.commitProxy('query');
                }
              })
              .catch(() => {
                VXETable.modal.message({
                  content: '导入失败，请检查数据是否正确！',
                  status: 'error'
                });
              });
          }
        },
   exportConfig: {
  remote: false, // 使用本地导出
  types: ['xlsx', 'csv'], // 显示支持的文件类型
  modes: ['current', 'selected', 'all'],
  beforeExportMethod({ options }) {
    const $grid = this.$refs.xGrid
    // 获取完整数据（包含分页信息）
    const { fullData } = $grid.getTableData()
    
    // 数据转换（保持与图片中的列顺序一致）
    const exportData = fullData.map(item => ({
      '医生ID': item.doctor_id,
      '医生姓名': item.doctor_name,
      '电话': item.phone || '无', // 处理空值
      '邮箱': item.email || '未填写',
      '性别': item.gender,
      '职位': POSITION_MAP[item.position] || item.position,
      '个人简介': item.introduce || '暂无简介'
    }))

    // 执行导出（生成与图片一致的表格结构）
    $grid.exportData({
      type: 'xlsx',
      filename: `医生信息_${new Date().toLocaleDateString()}`,
      sheetName: '医生数据',
      columns: [
        { field: '医生ID', title: '医生ID' },
        { field: '医生姓名', title: '医生姓名' },
        { field: '电话', title: '电话' },
        { field: '邮箱', title: '邮箱' },
        { field: '性别', title: '性别' },
        { field: '职位', title: '职位' },
        { field: '个人简介', title: '个人简介' }
      ],
      data: exportData
    })
    return false // 禁止默认导出行为
  }
},
        checkboxConfig: {
          labelField: 'id',
          reserve: true,
          highlight: true,
          range: true
        },
         editRules: {
          doctor_name: [
            { required: true, message: '医生姓名必须填写' }
          ],
          password: [
            { required: true, message: '密码必须填写' },
            { min: 6, max: 20, message: '密码长度在 6 到 20 个字符' }
          ],
          password_confirm: [
            { required: true, message: '确认密码必须填写' },
          ],
          gender: [
            { required: true, message: '性别必须填写' }
          ],
          position: [
            { required: true, message: '职位必须填写' }
          ]
        },
        editConfig: {
          trigger: 'click',
          mode: 'row',
          showStatus: true
        }
      }
    };
  },
  methods: {
    handleToolbar({ code }) {
      if (code === 'insert_actived') {
        this.isCreating = true;
        this.$refs.xGrid.insertRow({}, 0); 
      } else if (code === 'save') {
        this.handleSave();
      } else if (code === 'custom_delete') { 
        this.handleDelete();
      } else if (code === 'custom_quit') { 
        this.handleQuit();
      } else if (code === 'query') { 
        this.handleSearch();
      }
    },
    handleProxyQuery({ page }) {
    const { currentPage, pageSize } = page; 
    const startIndex = (currentPage - 1) * pageSize;  
    const endIndex = currentPage * pageSize;  
  
    this.tableData = this.allData.slice(startIndex, endIndex);  
  },
    async handleDelete() {
      const $grid = this.$refs.xGrid;
      const selection = $grid.getCheckboxRecords();
      
      if (selection.length !== 1) {
        this.$message.warning('请选择且仅选择一条要删除的记录');
        return;
      }

      const doctorId = selection[0].doctor_id.toString(); 

      this.$confirm(
        `确定要删除医生工号：【${doctorId}】吗？`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          const response = await fetch('http://121.196.228.176:9002/user/adminDelDoctorAccount/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'token': `${getToken()}` 
            },
            body: JSON.stringify({
              doctor_id: doctorId  
            })
          });

          const data = await response.json();
          if (response.ok && data.code === 200) {
            this.$message.success('删除成功');
            this.handleSearch(); // 刷新数据
          } else {
            this.$message.error(`删除失败：${data.msg || '未知错误'}`);
          }
        } catch (error) {
          console.error('删除请求失败:', error);
          this.$message.error('网络请求失败，请检查控制台');
        }
      }).catch(() => {
        this.$message.info('已取消删除');
      });
    },
    async handleSave() {
      try {
        const $grid = this.$refs.xGrid;
        const errMap = await $grid.validate().catch(errMap => errMap);
        if (errMap) return;

        const { insertRecords } = $grid.getRecordset();
        if (insertRecords.length === 0) {
          this.$message.warning('没有需要保存的数据');
          return;
        }

        const saveData = insertRecords[0]; 
        const response = await fetch('http://121.196.228.176:9002/user/adminAddDoctorAccount/', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'token': `${getToken()}` 
          },
          body: JSON.stringify({
            doctor_name: saveData.doctor_name,
            password: saveData.password,
            password_confirm: saveData.password_confirm,
            gender: saveData.gender,
            position: saveData.position
          })
        });

        const data = await response.json();
        if (response.ok && data.msg === '添加医生账号成功') {
          this.isCreating = false;
          $grid.removeCheckboxRow();
          this.handleSearch(); // 刷新数据
          this.$message.success('保存成功');
        } else {
          this.$message.error(data.msg || '保存失败');
        }
      } catch (error) {
        console.error('保存失败:', error);
        this.$message.error('请求失败，请检查网络');
      }
    },
    handleSearch() {
      // ✅ 确保调用方式正确
      this.$refs.xGrid.commitProxy('query')
    },
    handleQuit() {
      this.$refs.xGrid.commitProxy('query');
      this.isCreating = false;
      this.$message.info('已取消操作');
    }
  },
  mounted() {
    // 初始化时直接调用 handleSearch 方法获取数据
    this.handleSearch();
  }
};
</script>

<style lang="scss">
@import '../assets/css/bootstrap-grid.min.css';
.vxe-table .avatar-cell img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}
</style>
<template>
    <div class="container">
      <div>
        <vxe-grid ref="xGrid" 
                  :columns="isCreating ? createColumns : fullColumns"
                  :data="tableData"
                  @toolbar-button-click="handleToolbar"
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
                  :formConfig="gridOptions.formConfig"
                  :toolbarConfig="gridOptions.toolbarConfig" 
                  :proxyConfig="gridOptions.proxyConfig"
                  :importConfig="gridOptions.importConfig"
                  :exportConfig="gridOptions.exportConfig" 
                  :checkboxConfig="gridOptions.checkboxConfig"
                  :editRules="gridOptions.editRules" 
                  :editConfig="gridOptions.editConfig"
                  @proxy-query="handleProxyQuery">
        </vxe-grid>
      </div>
      <el-dialog
      title="更改信息"
      :visible.sync="dialogVisible"
      width="50%"
      @close="handleClose"
    >
      <el-form
        ref="updateForm"
        :model="updateForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="updateForm.patientName"
            placeholder="请输入姓名"
          ></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input
            v-model="updateForm.phone"
            placeholder="请输入电话"
          ></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select
            v-model="updateForm.gender"
            placeholder="请选择性别"
          >
            <el-option label="男" value="male"></el-option>
            <el-option label="女" value="female"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="出生日期" prop="birthday">
          <el-date-picker
            v-model="updateForm.birthday"
            type="date"
            placeholder="选择日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="记录" prop="record">
          <el-input
            v-model="updateForm.record"
            placeholder="请输入记录"
          ></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancel">取消</el-button>
        <el-button type="primary" @click="confirm">确定</el-button>
      </span>
    </el-dialog>
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
         dialogVisible: false,
     updateForm: {
        patient_id: "",
        patientName: "",
        phone: "",
        gender: "",
        birthday: "",
        record: ""
      },
      rules: {
         patientName: [{ required: true, message: "请输入姓名", trigger: "blur" }],
        phone: [{ required: true, message: "请输入电话", trigger: "blur" }],
        gender: [{ required: true, message: "请选择性别", trigger: "change" }],
        birthday: [{ required: true, message: "请选择日期", trigger: "change" }],
        record: [{ required: true, message: "请输入记录", trigger: "blur" }]
      },
        
        isCreating: false,
        tableData: [],
        serveApiUrl: 'http://121.196.228.176:9002/user/adminAddDoctorAccount',
     createColumns: [
    { type: 'checkbox', width: 60 },
    { field: 'patientName', title: '患者姓名', editRender: { name: 'input' } },
    { field: 'phone', title: '电话', editRender: { name: 'input' } },
    { field: 'gender', title: '性别', editRender: { name: '$select', options: [{ label: '男', value: '男' }, { label: '女', value: '女' }] } },
    { field: 'birthday', title: '出生年月', editRender: {  name: '$input', 
              props: {
                type: 'date',
                placeholder: '选择日期',
                format: 'yyyy-MM-dd', 
                valueFormat: 'yyyy-MM-dd'
              } } },
    { field: 'record', title: '病情记录', editRender: { name: 'input' } }
  ],
        fullColumns: [
          { type: 'checkbox', width: 60 },
          { field: 'patient_id', title: '患者ID' },
          { field: 'patientName', title: '患者姓名' },
          { field: 'phone', title: '电话' },
          // { field: 'email', title: '邮箱' },
          { field: 'gender', title: '性别' },
           { field: 'birthday', title: '出生年月', },
          { field: 'record', title: '病情描述', showOverflow: true }
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
    pageSize: 50,  // 每页显示50条
    pageSizes: [50, 100, 200, 500, 1000],  // 可选择每页显示条数
    remote: false,  // 设置为false表示前端分页
    layout: 'total, sizes, prev, pager, next, jumper'  // 分页控件的布局
  },
          formConfig: {
            titleWidth: 100,
            titleAlign: 'right',
            items: [ 
              {
                field: 'doctor_id',
                title: '工号',
                span: 6,
                itemRender: { name: '$input', props: { placeholder: '请输入工号', } }
              },
              {
                field: 'doctor_name',
                title: '医生姓名',
                span: 6,
                itemRender: { name: '$input', props: { placeholder: '请输入医生姓名' } }
              },
              {
                field: 'gender',
                title: '性别',
                span: 5,
                itemRender: { 
                  name: '$select', 
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
          toolbarConfig: {
            buttons: [
              { code: 'insert_actived', name: '新增' },
               { code: 'update', name: '更改' },
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
       // 修改 proxyConfig 的 query 方法
    proxyConfig: {
            seq: true,
            sort: false,
            filter: false,
            form: true,
            props: {
              result: 'result',
              total: 'page.total'
            },
            ajax: {
              query: () => {
                return fetch('http://121.196.228.176:9002/user/detail/', {
                  method: 'GET',
                  headers: { 'token': `${getToken()}` }
                })
                .then(response => response.json())
                .then(data => {
                  this.allData = data.data; 
                  return {
                    page: {
                      total: data.length
                    },
                    result: data
                  };
                });
              }
            }
          },
          columns: [
             { type: 'checkbox', title: '选择', width: 80 , align: 'center',
    headerAlign: 'center' },
    {
      field: 'patient_name',
      title: '医生姓名',
      editRender: { name: 'input', attrs: { placeholder: '请输入医生姓名' } },
       align: 'center',    
    headerAlign: 'center' 
    },
            {
              field: 'phone',
              title: '电话',
              editRender: { name: 'input', attrs: { placeholder: '请输入电话', } },
               align: 'center',    
    headerAlign: 'center' 
            },
            {
              field: 'birthday',
              title: '生日',
              editRender: { name: 'input', attrs: { placeholder: '请输入生日',} },
               align: 'center',    
    headerAlign: 'center' 
            },
            {
              field: 'gender',
              title: '性别',
              editRender: {
                name: '$select',
                options: [
                  { label: '男', value: '男' },
                  { label: '女', value: '女' }
                ],
                props: { placeholder: '请选择性别' }
              },
               align: 'center',    
    headerAlign: 'center' 
            },
             {
              field: 'record',
              title: '病情描述',
              editRender: { name: 'input', attrs: { placeholder: '请输入病情描述',} },
               align: 'center',    
    headerAlign: 'center' 
            },
          ],
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
            remote: true,
            types: ['xlsx'],
            modes: ['current','selected', 'all'],
            exportMethod({ options }) {
              const $grid = this.$refs.xGrid;
              if ($grid) {
                const proxyInfo = $grid.getProxyInfo();
                const body = {
                  filename: options.filename,
                  sheetName: options.sheetName,
                  isHeader: options.isHeader,
                  original: options.original,
                  mode: options.mode,
                  pager: proxyInfo ? proxyInfo.pager : null,
                  ids:
                    options.mode ==='selected'
                     ? options.data.map(item => item.id)
                      : [],
                  fields: options.columns.map(column => {
                    return {
                      field: column.field,
                      title: column.title
                    };
                  })
                };
                return fetch(`${this.serveApiUrl}/export`, {
                  method: 'POST',
                  headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getToken()}` 
                  },
                  body: JSON.stringify(body)
                })
                  .then(response => response.json())
                  .then(data => {
                    if (data.id) {
                      VXETable.modal.message({
                        content: '导出成功，开始下载',
                        status: 'success'
                      });
                      fetch(`${this.serveApiUrl}/export/download/${data.id}`, {
                        headers: {
                          'Authorization': `Bearer ${getToken()}` 
                        }
                      }).then(response => {
                        response.blob().then(blob => {
                          VXETable.saveFile({
                            filename: '导出数据',
                            type: 'xlsx',
                            content: blob
                          });
                        });
                      });
                    }
                  })
                  .catch(() => {
                    VXETable.modal.message({ content: '导出失败！', status: 'error' });
                  });
              }
              return Promise.resolve();
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
        }else if (code === 'update') {
          this.handleUpdate();
        }
      },
    async handleUpdate() {
      const $grid = this.$refs.xGrid;
      const selection = $grid.getCheckboxRecords();
      
      if (selection.length !== 1) {
        this.$message.warning('请选择且仅选择一条要更改的记录');
        return;
      }
      
      const doctorId = selection[0].patient_id; 
      if (!doctorId) {
        this.$message.error('更改记录不能为空');
        return;
      }
      this.updateForm.patient_id = doctorId;
      this.dialogVisible = true;
    },
    handleClose() {
      this.$refs.updateForm.resetFields();
    },
    cancel() {
      this.dialogVisible = false;
    },
    confirm() {
     this.$refs.updateForm.validate(valid => {
    if (valid) {
      // 表单验证通过，提交数据
      const url = 'http://121.196.228.176:9002/user/selectAndUpdate/';
      const token = getToken(); // 获取实际的 token 值
      const headers = {
        'Content-Type': 'application/json',
        'token': token
      };
      
      // 格式化 birthday 和 gender
      const formattedData = {
        birthday: this.formatDate(this.updateForm.birthday),
        gender: this.updateForm.gender === 'male' ? '男' : '女', // 将 gender 转换为中文
        patientName: this.updateForm.patientName,
        patient_id: this.updateForm.patient_id,
        phone: this.updateForm.phone,
        record: this.updateForm.record
      };
      
      const body = JSON.stringify(formattedData);

      fetch(url, {
        method: 'PATCH',
        headers: headers,
        body: body
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          this.$message({
            type: 'success',
            message: '更改成功'
          });
          this.dialogVisible = false;
          // 根据后端返回的数据进行其他处理
        })
        .catch(error => {
          this.$message.error('更改失败: ' + error.message);
        });
    } else {
      this.$message.error('请按要求填写表单');
      return false;
    }
  });
    },
    formatDate(date) {
  if (!date) return '';
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
},
        async handleDelete() {
    const $grid = this.$refs.xGrid;
    const selection = $grid.getCheckboxRecords();
    
    if (selection.length !== 1) {
      this.$message.warning('请选择且仅选择一条要删除的记录');
      return;
    }
  
    const doctorId = selection[0].patient_id; 
    if(!doctorId){
      this.$message.error('删除记录不能为空');
      return;
    }
    this.$confirm(
      `确定要删除医生工号：【${selection[0].patient_id}】吗？`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(async () => {
      try {
        const response = await fetch('http://121.196.228.176:9002/user/selectAndUpdate/', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'token': `${getToken()}` 
          },
          body: JSON.stringify({
            patient_id: doctorId  
          })
        });
  
        const data = await response.json();
        if (response.ok && data.msg === '删除成功') {
          this.$message.success('删除成功');
          $grid.commitProxy('query');
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
          const info = JSON.parse(localStorage.getItem('info')) || {};
          const response = await fetch('http://121.196.228.176:9002/user/detail/', {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'token': `${getToken()}` 
            },
            body: JSON.stringify({
              patientName: saveData.patientName,
              phone: saveData.phone,
              birthday: saveData.birthday,
              gender: saveData.gender,
              doctor_id: info.userId,
              record: saveData.record
            })
          });
  
          const data = await response.json();
          if (response.ok && data.msg === '成功添加患者信息并建立医患关系') {
            this.isCreating = false;
            $grid.removeCheckboxRow();
            $grid.commitProxy('query');
            this.$message.success('保存成功');
          } else {
            this.$message.error(data.msg || '保存失败');
          }
        } catch (error) {
          console.error('保存失败:', error);
          this.$message.error('请求失败，请检查网络');
        }
      },
     handleProxyQuery({ page }) {
    const { currentPage, pageSize } = page; 
    const startIndex = (currentPage - 1) * pageSize;  
    const endIndex = currentPage * pageSize;  
  
    this.tableData = this.allData.slice(startIndex, endIndex);  
  },
      proxyQuery() {
        console.log('数据代理查询事件');
      },
      proxyDelete() {
        console.log('数据代理删除事件');
      },
      proxySave() {
        console.log('数据代理保存事件');
      },
      handleQuit() {
        // 点击取消按钮时刷新页面
        this.$refs.xGrid.commitProxy('query');
        this.isCreating = false;
        this.$message.info('已取消操作');
      }
    },
    mounted() {
     const sexList = [
        { label: '女', value: '0' },
        { label: '男', value: '1' }
      ];
      const { formConfig, columns } = this.gridOptions;
      
      if (columns) {
        const sexColumn = columns[4]; 
        if (sexColumn && sexColumn.editRender) {
          sexColumn.editRender.options = sexList;
        }
      }
      
      if (formConfig && formConfig.items) {
        const sexItem = formConfig.items[3]; 
        if (sexItem && sexItem.itemRender) {
          sexItem.itemRender.options = sexList;
        }
      }
      this.$refs.xGrid.commitProxy('query');
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
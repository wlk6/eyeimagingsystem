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

    <!-- 审核意见弹窗 -->
    <el-dialog title="审核意见" :visible.sync="auditDialogVisible" width="30%">
      <el-input type="textarea" :rows="4" placeholder="请输入审核意见" v-model="auditOpinion"></el-input>
      <div slot="footer" class="dialog-footer">
        <el-button>取 消</el-button>
        <el-button type="primary" @click="confirmAudit">确 定</el-button>
      </div>
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
        { 
          field: 'check_info_id', 
          title: '审核信息ID',
          align: 'center'
        },
        {
          field: 'doctor_id', 
          title: '医生工号',
          align: 'center',
        },
        { 
          field: 'alter_time', 
          title: '修改时间',
          align: 'center',
        }
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
          pageSize: 50,
          pageSizes: [50, 100, 200, 500, 1000],
          remote: false,
          layout: 'total, sizes, prev, pager, next, jumper'
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
            { code: 'quit', name: '不通过',status: 'danger'},
            { code: 'save', name: '通过',status: 'success'},
            { code: 'query', name: '查询', status: 'success' }
          ],
          refresh: true,
          import: true,
          export: true,
          print: true,
          zoom: true,
          custom: true
        },
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
              return fetch('http://121.196.228.176:9002/Login/checkPasswordView/', {
                method: 'POST',
                headers: { 'token': `${getToken()}` }
              })
              .then(response => response.json())
              .then(data => {
                if (!data.data || !Array.isArray(data.data)) {
                  throw new Error('无效的数据结构');
                }
                
                this.allData = data.data.map(item => ({
                  ...item,
                  check_info_id: item.check_info_id ?? 'N/A',
                  doctor_id: Number(item.doctor_id) || 0,
                  alter_time: item.alter_time || '未知时间'
                }));
                return {
                  page: { total: data.data.length },
                  result: this.allData
                };
              });
            }
          }
        },
        columns: [
           { type: 'checkbox', title: '选择', width: 80 , align: 'center',
          headerAlign: 'center' },
          {
            field: 'doctor_name',
            title: '医生姓名',
            editRender: { name: 'input', attrs: { placeholder: '请输入医生姓名' } },
            align: 'center',    
            headerAlign: 'center' 
          },
          {
            field: 'password',
            title: '密码',
            editRender: { name: 'input', attrs: { placeholder: '请输入密码', type: 'password' } },
            align: 'center',    
            headerAlign: 'center' 
          },
          {
            field: 'password_confirm',
            title: '确认密码',
            editRender: { name: 'input', attrs: { placeholder: '请再次输入密码', type: 'password' } },
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
            field: 'position',
            title: '职位',
            editRender: {
              name: '$select',
              options: [
                { label: '主任医师', value: 'chief_physician' },
                { label: '副主任医师', value: 'associate_physician' },
                { label: '主治医师', value: 'attending_doctor' }
              ],
              props: { placeholder: '请选择职位' }
            },
            align: 'center',    
            headerAlign: 'center' 
          }
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
      },
      auditDialogVisible: false, // 审核意见弹窗是否可见
      auditOpinion: '' // 审核意见
    };
  },
  methods: {
    handleToolbar({ code }) {
      if (code === 'insert_actived') {
        this.isCreating = true;
        this.$refs.xGrid.insertRow({}, 0); 
      }else if (code === 'custom_delete') { 
        this.handleDelete();
      } else if (code === 'quit') { 
        this.handleQuit();
      } else if (code === 'save') { // 审核按钮点击事件
        this.handleAudit();
      }
    },
  handleAudit() {
  const $grid = this.$refs.xGrid;
  const selection = $grid.getCheckboxRecords();

  if (selection.length !== 1) {
    this.$message.warning('请选择且仅选择一条要审核的记录');
    return;
  }

  const doctorId = selection[0].doctor_id.toString();

  this.$confirm(
    `确定要通过医生工号：【${doctorId}】密码审核吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    this.auditSubmit(doctorId);
  }).catch(() => {
    this.$message.info('已取消审核');
  });
},

async auditSubmit(doctorId) {
  try {
    const response = await fetch('http://121.196.228.176:9002/Login/adminGivePasswordCheckAdvice/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'token': `${getToken()}` 
      },
      body: JSON.stringify({
        doctor_id: doctorId,
        result: 1 // 传递审核意见
      })
    });

    const data = await response.json();
    if (response.ok && data.msg === '医生密码修改成功') {
      this.$message.success('审核成功');
      const $grid = this.$refs.xGrid;
      $grid.commitProxy('query');
    } else {
      this.$message.error(data.msg || '审核失败');
    }
  } catch (error) {
    console.error('审核请求失败:', error);
    this.$message.error('审核不通过，请检查网络或控制台');
  }
},
async auditSubmitt(doctorId) {
  try {
    const response = await fetch('http://121.196.228.176:9002/Login/adminGivePasswordCheckAdvice/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'token': `${getToken()}` 
      },
      body: JSON.stringify({
        doctor_id: doctorId,
        result: 0 // 传递审核意见
      })
    });

    const data = await response.json();
    if (response.ok && data.msg === '审核不通过') {
      this.$message.success('审核成功');
      const $grid = this.$refs.xGrid;
      $grid.commitProxy('query');
    } else {
      this.$message.error(data.msg || '审核失败');
    }
  } catch (error) {
    console.error('审核请求失败:', error);
    this.$message.error('审核不通过，请检查网络或控制台');
  }
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
        `确定要删除医生工号：【${selection[0].doctor_name}】吗？`,
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
    
    handleProxyQuery({ page }) {
      const { currentPage, pageSize } = page; 
      const startIndex = (currentPage - 1) * pageSize;  
      const endIndex = currentPage * pageSize;  

      this.tableData = this.allData.slice(startIndex, endIndex);  
    },
    handleQuit() {
     const $grid = this.$refs.xGrid;
  const selection = $grid.getCheckboxRecords();

  if (selection.length !== 1) {
    this.$message.warning('请选择且仅选择一条要审核的记录');
    return;
  }

  const doctorId = selection[0].doctor_id.toString();

  this.$confirm(
    `确定要不通过医生工号：【${doctorId}】密码审核吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    this.auditSubmitt(doctorId);
  }).catch(() => {
    this.$message.info('已取消审核');
  });
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
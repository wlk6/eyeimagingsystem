import request from '@/utils/request';
import { getInfo } from '@/utils/storage';

export const info = (formData) => { 
    const { token } = getInfo();
    const config = {
        headers: {
            token: `${token}`,
            'Content-Type': 'multipart/form-data' // 明确文件上传格式
        }
    };

    return request.post('user/doctorAlterInfo/', formData, config);
};
import request from '@/utils/request';
import { getInfo } from '@/utils/storage';

export const getinfo = () => { 
    const { token, userId } = getInfo();
    const config = {
        headers: {
            token: `${token}`,
            'Content-Type': 'application/json', // 确保请求头中包含 Content-Type
        }
    };

    // 构造请求体
    const requestBody = {
        doctor_id: userId // 确保 doctor_id 是字符串类型
    };

    return request.post('user/getDoctorInfo/', JSON.stringify(requestBody), config);
};
import request from '@/utils/request'

export const adminlog = (id, password) => {
    // 实现登录请求 axios
    return request.post('Login/adminLoginView/', {
        ID: id,
        password: password
    })
}
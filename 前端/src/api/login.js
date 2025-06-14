import request from '@/utils/request'

export const login = (id, password) => {
    // 实现登录请求 axios
    return request.post('Login/doctorLoginView/', {
        ID: id,
        password: password
    })
}
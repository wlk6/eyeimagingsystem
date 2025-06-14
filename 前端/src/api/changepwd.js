import request from '@/utils/request'

export const changepwd = (doctor_id,password,password_verify,captcha_key,captcha_code) => {
    // 实现登录请求 axios
    return request.post('Login/alterPasswordView/', {
        doctor_id: doctor_id,
        password: password,
        password_verify: password_verify,
        captcha_key: captcha_key,
        captcha_code: captcha_code
       
    })
}
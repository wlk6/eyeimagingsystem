import axios from "axios";
const instance = axios.create({
    baseURL: 'http://8.155.59.127:34561/',
    timeout: 5000,
});
//拦截器
instance.interceptors.request.use(
    config => {
       
       
        return config;
    },
    error => {
        //对请求错误做些什么
        return Promise.reject(error);
    }
);
//添加响应拦截器
instance.interceptors.response.use(
    response => {   
        // if (response.status !== 200) {
        //     //对响应数据做点什么
        //     return Promise.reject(response.message);
        // }
        // setTimeout(function () {
        //     document.querySelector('.success').style.display = 'block';
        // }, 3200);

        // // setTimeout(function () {
        // //     this.$router.push('/');;
        // // }, 4000);
        return response.data;
    },
    error => {
        //对响应错误做点什么
        return Promise.reject(error);
    }
);
export default instance;
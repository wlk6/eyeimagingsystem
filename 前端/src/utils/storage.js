const INFO_KEY = 'info';
//获取个人信息
export const getInfo = () => {
    const defaultObj = {
        token: '',
        userId:''
    };
    const re = localStorage.getItem(INFO_KEY);
    return re ? JSON.parse(re) : defaultObj;
}
//设置个人信息
export const setInfo = (obj) => {
    localStorage.setItem(INFO_KEY, JSON.stringify(obj));
}
//移除个人信息
export const removeInfo = () => {
    localStorage.removeItem(INFO_KEY);
}
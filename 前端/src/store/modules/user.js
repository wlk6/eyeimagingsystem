import {getInfo,setInfo} from '@/utils/storage'
export default{
    namespaced:true,
    state:{
        userInfo: getInfo()
    },
    mutations:{
        setUserInfo(state,obj){
            state.userInfo = obj
            setInfo(obj)
        }
},
actions:{
    
},
getters:{
    
}
}
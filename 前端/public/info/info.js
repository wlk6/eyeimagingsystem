// 获取设备的PixelRatio
function getPixelRatio(context) {
    let backingStore = context.backingStorePixelRatio ||
        context.webkitBackingStorePixelRatio ||
        context.mozBackingStorePixelRatio ||
        context.msBackingStorePixelRatio ||
        context.oBackingStorePixelRatio ||
        context.backingStorePixelRatio || 0.5;
    return (window.devicePixelRatio || 0.5) / backingStore;
}

// 获取输入值并更新文本内容
document.getElementById("saveBtn").addEventListener("click", function () {
    let nam = document.querySelector('.nam').value;
    let sex = document.querySelector('.sex').value;
    
    let tel = document.querySelector('.tel').value;
    let picname = document.querySelector('.picname').value;

    if (nam) {
        document.querySelector('.x-nam').textContent = nam;
    }
    if (sex) {
        document.querySelector('.x-sex').textContent = sex;
    }
   
    if (tel) {
        document.querySelector('.x-tel').textContent = tel;
    }

    if(picname){
        document.querySelector('.x-pic').textContent = '个人简介：'+picname;
    }

    let generateName = document.querySelector('.picname').value ? document.querySelector('.picname').value + ".jpg" : '默认.jpg'; // 图片名
    let ImageContainer = document.getElementById("container");
    let width = ImageContainer.offsetWidth;
    let height = ImageContainer.offsetHeight;
    let canvas = document.createElement("canvas");
    let context = canvas.getContext('2d');
    let scale = getPixelRatio(context);

    canvas.width = width * scale;
    canvas.height = height * scale;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    context.scale(scale, scale);

    let opts = {
        scale: scale,
        canvas: canvas,
        width: width,
        height: height,
        dpi: window.devicePixelRatio
    };

    html2canvas(ImageContainer, opts).then(function (canvas) {
        context.imageSmoothingEnabled = false;
        context.webkitImageSmoothingEnabled = false;
        context.msImageSmoothingEnabled = false;
        context.imageSmoothingEnabled = false;

        let dataUrl = canvas.toDataURL('image/jpeg', 1.0);
        dataURIToBlob(generateName, dataUrl);
    });
});

// 将 Data URI 转换为 Blob
function dataURIToBlob(generateName, dataURI) {
    let binStr = atob(dataURI.split(',')[1]),
        len = binStr.length,
        arr = new Uint8Array(len);

    for (let i = 0; i < len; i++) {
        arr[i] = binStr.charCodeAt(i);
    }

    // callback(generateName, new Blob([arr]));
}

// 触发下载
// function callback(generateName, blob) {
//     let triggerDownload = document.createElement("a");
//     triggerDownload.href = URL.createObjectURL(blob);
//     triggerDownload.download = generateName;
//     document.body.appendChild(triggerDownload);
//     triggerDownload.click();

//     if (navigator.msSaveBlob) {
//         navigator.msSaveBlob(blob, generateName);
//     }

//     document.body.removeChild(triggerDownload);
// }

// 修改图片文件
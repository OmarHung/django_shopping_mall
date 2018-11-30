function alert_delete(url) {
    var r = confirm('是否確定刪除此項目?');
    if(r==True) {
        window.location.replace(url);
    }
};
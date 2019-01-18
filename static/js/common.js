//==================================================
//===============    刪除警告    ==================
//=================================================//
function alert_delete(url) {
    var r = confirm('是否確定刪除此項目?');
    if(r==True) {
        window.location.replace(url);
    }
};

//==================================================
//===============    下拉選單頁面刷新  ==================
//=================================================//
/**
 * @param {[type]} form_name   [表單名稱]
 * @param {[type]} select_name [下拉選單名稱]
 */
function SelectIt(form_name,select_name){
  if ( document.forms[form_name].elements[select_name].options[document.forms[form_name].elements[select_name].selectedIndex].value != "none"){
    location = document.forms[form_name].elements[select_name].options[document.forms[form_name].elements[select_name].selectedIndex].value
  }
}
window.addEvent('domready', function(){
    var ord_phone = $$('#mobile_phone')[0];
    var ord_address = $$('#address')[0];
    var new_phone = $$('#m_mobile')[0];
    var new_address = $$('#m_address')[0];
    var modify_info = $$('#modify_info')[0];
    var account_info = $$('#account_info')[0];
    var change_info = function(){
        new Request.JSON({
            'url': '/user/modifyinfo/',
            onSuccess: function(data){
                if ('ok' == data['ret']){
                    ord_phone.innerHTML = new_phone.value;
                    ord_address.innerHTML = new_address.value;
                    modify_info.setStyle('display', 'none');
                    account_info.setStyle('display', 'block');
                } else {
                    alert(data['ret']);
                }
            },
            onFailure: function(){
                alert('ERROR!');
            }
        }).get({'phone': new_phone.value, 'address': new_address.value});
    };
    $$('.count_li> p > input')[2].addEvent('click', function(){
        change_info();
    });
    $$('.my_count > h4 > span > a')[0].addEvent('click', function(){
        modify_info.setStyle('display', 'block');
        account_info.setStyle('display', 'none');
        new_phone.value = ord_phone.innerHTML;
        new_address.value = ord_address.innerHTML;
    });
});
window.addEvent('domready', function(){
    var iflogin = function(){
        span_num = $$('.user > li > span');
        if (1 == span_num.length){
            return true;
        }else{
            return false;
        }
    }
    var add_to_cart = function(id, name, price, day_cart){
        day_cart = day_cart.toInt();
        date_today = new Date();
        tbd = $$('.cart_list_table > table > tbody')[0];
        the_trs = tbd.getElements('tr[name='+ id +'][pos='+ day_cart +']');
        if (1 == the_trs.length){
            ipt = the_trs[0].getElement('input');
            ipt.set('value', parseInt(ipt.get('value')) + 1);
            change_price();
            return;
        }
        var position = tbd.getElements('.menu_t')[day_cart];
        var another = new Element('tr', {
            'name': id,
            'pos': day_cart,
            'date_day': date_today.increment('day', day_cart).format('%Y-%m-%d')
        });
        another.set('html', '<td>'+ name +'</td><td><input type="text" value="1" /></td><td>'+ price +'</td><td><a href="javascript:void(0);">删除</a></td>')
        another.inject(position, 'after');
        another.getElement('a').addEvent('click', function(){
            this.getParent().getParent().erase('name');
            this.getParent().getParent().erase('html');
            change_price();
        });
        another.getElement('input').addEvent('change', function(){
            change_price();
        })
        change_price();
    }
    
    var all_list = $$('.cate_list > li > dl > dd');
    all_list.addEvents({
        'click': function(){
            if (! iflogin()){
                setTimeout(function(){
                    window.location.href="/user/login/";
                }, 0);
                return;
            }
            lnk = this.getElement('a');
            name = lnk.innerHTML;
            id = lnk.get('name');
            price = this.getElement('span').innerHTML.toInt();
            day_cart = lnk.get('day_cart');
            add_to_cart(id, name, price, day_cart);
        },
        'mouseenter': function(){
            this.addClass('hover');
        },
        'mouseleave': function(){
            this.removeClass('hover');
        }
    })

    $$('.cart_list > input')[0].addEvent('click', function(){
        var price_dom = $$('.subtotal > span')[0];
        var ord_phone = $('mobile_phone');
        var ord_address = $('address');
        if (0 == price_dom.innerHTML){
            alert('请点击左侧菜单点菜');
            return;
        };
        if ('' == ord_phone.innerHTML.trim() || '' == ord_address.innerHTML.trim()){
            alert('请填写手机号和地址');
            return;
        };
        if (!confirm('是否确定提交定单？\n\n提交后我们会在每日 11:30 到 12:30 把当日午餐送出。\n应付款： ' + price_dom.innerHTML + ' 元， 支付方式： 货到付款。')){
            return;
        }
        var pay_list = $$('.cart_list_table > table > tbody > tr');
        var regionid = document.URL.match('/product/([0-9]+)/list/')[1];
        var data = {'region': regionid, 'orders': {}};
        pay_list.each(function(item){
            if (item.get('name') != null){
                if (data['orders'][item.get('date_day')] == undefined){
                    data['orders'][item.get('date_day')] = {};
                }
                if (data['orders'][item.get('date_day')][item.get('name')] == undefined){
                    data['orders'][item.get('date_day')][item.get('name')] = {};
                }
                data['orders'][item.get('date_day')][item.get('name')] = item.getElement('input').get('value');
            }
        });
        var newform = $$('#order_form')[0];
        newform.getElement('input[name=data]').set('value', JSON.encode(data));
        newform.submit()
    });
    var change_price = function(){
      var price_dom = $$('.subtotal > span')[0];
      var pay_list = $$('.cart_list_table > table > tbody > tr');
        var price = 0;
        pay_list.each(function(item){
            if (item.get('name') != null){
                price += item.getElements('td')[2].innerHTML.toInt() * item.getElement('input').get('value').toInt();
            }
        });
        price_dom.set('html', price);
    };
})
var CartClass = new Class({
    initialize: function(cart_id){
        this.cartID = cart_id;
        this.errorSleepTime = 2000;
        this.typeDict = new Hash({
            'chat': this.addChat.bind(this),
            'add': this.addDish.bind(this),
            'del': this.delDish.bind(this),
            'inc': this.incDish.bind(this),
            'dec': this.decDish.bind(this)
        });
        this.chatDom = $('msg_box');
        this.cartDom = $$('.scroll_box table tbody')[0];
        this.cartBottom = $$('.cart_bottom')[0];
        this.notifyDom = $$('.notify')[0];
        this.chatForm = $('online_chat');
        this.chatForm.addEvent('submit', function(e){
            new Event(e).stop();
            this.sendChat();
        }.bind(this));
        this.initCart();
        this.initChat();
        this.refreshCart();
    },
    poll: function(){
        new Request.JSON({
            url: '/cart/waiting/',
            onSuccess: this.success.bind(this),
            onFailure: this.failure.bind(this)
        }).get({'cart_id': this.cartID});
    },
    initCart: function(){
        new Request.JSON({
            url: '/order/get/',
            onSuccess: function(response){
                if (200 != response['ret']){
                    return;
                }
                response['data'].each(function(item){
                    this.addDish(item);
                }.bind(this));
            }.bind(this)
        }).get({'order_id': this.cartID})
    },
    initChat: function(){
        new Request.JSON({
            url: '/chat/get/',
            onSuccess: function(response){
                if (200 != response['ret']){
                    return;
                }
                response['data'].each(function(item){
                    this.addChat(item);
                }.bind(this));
            }.bind(this)
        }).get({'order_id': this.cartID})
    },
    sendChat: function(content){
        var cartID = this.cartID;
        var chatBox = this.chatForm.getElements('input')[1];
        var chatText = chatBox.get('value').trim();
        if (0 == chatText.length){
            return;
        }
        new Request.JSON({
            url: '/cart/update/',
            onSuccess: function(){
                console.log('chat success');
            }
        }).get({'type': 'chat', 'cart_id': cartID, 'content': chatText});
        chatBox.set('value', '');
    },
    refreshCart: function(){
        var bottomList = this.cartBottom.getElements('p');
        var submitDom = this.cartBottom.getElement('input');
        var dishList = this.cartDom.getElements('tr');
        var dishPrice = 0;
        var dishCount = dishList.length;
        var itemRe = [];
        dishList.each(function(item){
            itemRe = item.getElements('td p')[2].get('html').match('(.+)元 x (.+)');
            dishPrice += itemRe[1].toFloat() * itemRe[2].toInt();
        });
        bottomList[0].set('html', '共计&nbsp;' + dishCount + '&nbsp;道菜');
        bottomList[1].set('html', '共需&nbsp;' + dishPrice + '&nbsp;元');
        if (0 == dishCount){
            submitDom.set('disabled', true);
        }else{
            submitDom.set('disabled', false);
        };
    },    
    addChat: function(data){
        var chatItem = new Element('li', {
            'html': '<li><span><a href="javascript:;;">' + data['user']['username'] + '</a>' + data['time'] + '</span><p>' + data['cont'] + '</p></li> '
        });
        chatItem.inject(this.chatDom, 'bottom');
        //this.chatDom.slideOut();
    },
    getDish: function(dishID){
        return $('dish' + dishID);
    },
    createDish: function(data){
        var dishItem = new Element('tr', {
            'id': 'dish' + data['cont'],
            'html': '<td><img class="cart_img" src="' + data['dish']['pic']['small'] + '" alt="" /> </td> <td><p>' + data['dish']['name'] + '</p> <p>' + data['user']['username'] + '</p></td> <td><p>' + data['dish']['price'] + '元 x ' + data['dish']['discount'] + '</p> <p> <a class="inc" href="javascript:;;">+</a> <a class="dec" href="javascript:;;">-</a> <a class="del" href="javascript:;;">x</a></p></td>'
        });
        return dishItem;
    },
    addDish: function(data){
        if (null != this.getDish(data['cont'])){
            //this.notify('这道菜已经在购物车里了');
            console.log('HAD IN CART');
            return;
        }
        var dishItem = this.createDish(data);
        var cart_id = this.cartID;
        var typeList = ['inc', 'dec', 'del'];
        var buttonList = dishItem.getElements('.inc, .dec, .del');
        buttonList.each(function(item, index){
            item.addEvent('click', function(){
                new Request.JSON({
                    url: '/cart/update/',
                    onSuccess: function(response){
                        console.log(response);
                        if (440 == response['ret']){
                            this.notify('订单已锁定');
                        }
                    }.bind(this)
                }).get({'type': typeList[index], 'cart_id': cart_id, 'content': data['cont']});
            }.bind(this))
        }.bind(this));
        dishItem.inject(this.cartDom, 'bottom');
    },
    delDish: function(data){
        var dishItem = this.getDish(data['cont']);
        if (null == dishItem){
            console.log('ERROR NO DISH');
            return;
        }
        dishItem.dispose();
    },
    incDish: function(data){
        var dishItem = this.getDish(data['cont']);
        if (null == dishItem){
            console.log('ERROR NO DISH');
            return;
        }
        var dishNumDom = dishItem.getElements('td p')[2];
        var re = dishNumDom.get('html').match('(.+ x )(.+)');
        dishNumDom.set('html', re[1] + (re[2].toInt() + 1)).highlight();
    },
    decDish: function(data){
        var dishItem = this.getDish(data['cont']);
        if (null == dishItem){
            console.log('ERROR NO DISH');
            return;
        }
        var dishNumDom = dishItem.getElements('td p')[2];
        var re = dishNumDom.get('html').match('(.+ x )(.+)');
        if (1 != re[2].toInt()){
            dishNumDom.set('html', re[1] + (re[2].toInt() - 1)).highlight();
        }else{
            //this.notify('不能再减了');
            console.log('CANT DEL')
        };
    },
    notify: function(s){
        var notifyDom = this.notifyDom;
        notifyDom.set('html', s);
        notifyDom.setStyle('display', 'block');
        var hiddenIt = function(){
            notifyDom.setStyle('display', 'none');
        };
        hiddenIt.delay(1500);
    },
    success: function(response){
        if (200 == response['ret']){
            var legalData = response['data'].filter(function(item){
                return this.typeDict.has(item['type']);
            }.bind(this));
            legalData.each(function(item){
                this.typeDict[item['type']](item);
            }.bind(this));
            this.refreshCart();
            this.poll.delay(0, this);
        }else if (401 == response['ret']){
            console.log('no user');
        }else{
            this.failure(response);
        };
    },
    failure: function(response){
        console.log('FAIL');
        this.poll.delay(this.errorSleepTime, this);
    }
});

var xTab = new ShopTabClass($$('.shop_nav li'), $$('.pagelist'), ORDER_ID);

window.addEvent('hashchange', function(){
    xTab.getData();
});

window.addEvent('domready', function(){
    var followUL = $$('.follow ul')[0];
    var addFollow = new AddFollow(followUL, 1);
    var cart = new CartClass(ORDER_ID);
    xTab.getData();
    cart.poll();
});

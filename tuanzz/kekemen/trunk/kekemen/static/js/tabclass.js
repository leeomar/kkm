var TabClass = new Class({
    initialize: function(tabs, helps){
        this.tabDict = this.makeTabDict(tabs);
        helps.setStyle('display', 'none');
        this.helpDict = new Hash({
            'loading': helps[0],
            'netError': helps[1],
            'showMore': helps[2],
            'noUpdate': helps[3]
        });
        this.helpDict['showMore'].addEvent('click', function(){
            this.getData();
        }.bind(this));
        this.helpDict['netError'].addEvent('click', function(){
            this.getData();
        }.bind(this));
        this.actTab = this.tabDict.getKeys()[0];
        this.anchor = -1;
    },
    init: function(tabType){
        this.changeAct(tabType);
        this.helpDict['noUpdate'].setStyle('display', 'none');
        this.helpDict['netError'].setStyle('display', 'none');
        this.helpDict['showMore'].setStyle('display', 'none');
        this.helpDict['loading'].setStyle('display', 'block');
    },
    changeAct: function(actTab){
        if (actTab == this.actTab){
            return;
        };
        this.tabDict[this.actTab].removeClass('cur');
        this.tabDict[actTab].addClass('cur');
        this.cleanBody(actTab);
        this.actTab = actTab;
        this.anchor = -1;
    },
    cleanBody: function(actTab){
        this.body.set('html', '');
    },
    noUpdate: function(){
        this.helpDict['showMore'].setStyle('display', 'none');
        this.helpDict['loading'].setStyle('display', 'none');
        this.helpDict['noUpdate'].setStyle('display', 'block');
    },
    getHashURL: function(){
        try{
            return  window.location.hash.match('#!/(.+)')[1];
        }catch(err){
            return this.tabDict[this.actTab].getElement('a').hash.match('#!/(.+)')[1];
        } 
    },
    getData: function(){
        url = this.getURL();
        this.init(this.getNewActTab());
        new Request.JSON({
            url: url,
            onSuccess: function(response){
                this.process(response);
            }.bind(this),
            onFailure: function(response){
                this.helpDict['netError'].setStyle('display', 'block');
            }.bind(this),
            onComplete: function(){
                this.helpDict['loading'].setStyle('display', 'none');
            }.bind(this)
        }).get({'anchor': this.anchor});
    },
    process: function(response){
        console.log(response);
        if (200 == response['ret']){
            this.mainProcess(response);
        }else if (401 == response['ret']){
            this.login();
        }else{
            this.noUpdate();
            console.log('UNKNOW ERRER');
        }
    },
    login: function(){
        var urlPath = window.location.pathname;
        var urlHash = window.location.hash;
        window.setTimeout(function(){
            window.location.href = '/accounts/login/?next=' + encodeURIComponent(urlPath + urlHash);
        }, 0);
    }
});

var HomeTabClass = new Class({
    Extends: TabClass,
    initialize: function(tabs, helps){
        this.parent(tabs, helps);
        this.body = $('maincont');
    },
    makeTabDict: function(tabs){
        var tabDict = new Hash();
        tabs.each(function(item){
            tabDict.include(item.getElement('a').hash.match('#!/(.+)/')[1], item);
        });
        return tabDict;
    },
    getURL: function(){
        return '/ajax/' + this.getHashURL();
    },
    getNewActTab: function(){
        return this.getHashURL().match('(.+)/')[1]
    },
    mainProcess: function(response){
        this.helpDict['showMore'].setStyle('display', 'block');
        this.anchor = response['anchor'];
        if ('feed' == this.actTab){
            this.refreshFeed(response['data']);
        }else{
            this.refreshDish(response['data']);
        }
    },
    createDish: function(data){
        photoList = '';
        data['commenters'].each(function(item){
            photoList += '<li><a href="/user/' + item['uid'] + '"><img class="avatar" src="' + item['pic']['small'] + '" alt="' + item['username'] + '" title="' + item['username'] + '" /></a></li>';
        });
        var dishDom = new Element('li', {
            'class': 'item_box index',
            'html': '<a href="/shop/' + data['detail']['shopID'] + '" title=""><img class="pic" src="' + data['detail']['pic']['middle'] + '" alt="" title="" /></a> <div class="pic_side"> <div class="have_buy"> <span class="label">他们都吃过..</span> <ul>' + photoList + '</ul> <span class="total">共<span class="num"><a href="javascript:;;">' + data['count'] + '</a></span>人</span> </div> <h3><a href="/shop/' + data['detail']['shopID'] + '">￥<span class="price">' + data['detail']['price'] + '</span>' + data['detail']['name'] + '</a></h3> <p class="posted">@<a href="/shop/' + data['detail']['shopID'] + '">' + data['detail']['shopName'] + '</a></p> </div> <div class="newestComment" style="display: none"></div><p class="btm_link"> <a class="fr" href="/shop/' + data['detail']['shopID'] + '">进店</a> <a href="javascript:;;">评论(' + data['statistic']['comment'] + ')</a> <a href="javascript:;;">想吃(' + data['statistic']['want'] + ')</a> <a href="javascript:;;">吃过(' + data['statistic']['eat'] + ')</a> <a href="javascript:;;">喜欢(' + data['statistic']['like'] + ')</a> </p> <div class="comments" style="display: none"> <div class="toggle"> <a href="javascript:;;" class="input_btn">查看全部</a> <a href="javascript:;;" class="input_btn">只看好友</a></div><ul class="clearfix"></ul> </div>'
        });
        var wholeCommentBody = dishDom.getElements('.comments')[0];
        var commentCountBlock = dishDom.getElements('p.btm_link a')[1];
        var newestComment = dishDom.getElements('.newestComment')[0];
        //这儿用来初始化最新评论
        new Request.JSON({
            url: '/newest/comment/',
            onSuccess: function(response) {
                    if(response['ret'] == 200)
                    {
                        var data = response['data'];
                        data.each(function(item,index){
                            if(index == data.length-1)
                            {
                                var commentDom = new Element('li',{'html': '<a href="#"><img class="avatar" src="'+item['user']['pic']['small']+ '"/></a><p><a href="#">'+item['user']['username']+'</a><span>'+item['ts']+'</span></p><p>'+item['cont']+'</p>'}); 
                                console.log(data.length-1);
                                newestComment.setStyle('display', '');
                                commentDom.inject(newestComment, 'bottom');
                            }
                        }.bind(this));
                    }
            }.bind(this), 
            onFailure: function(response){ 
                console.log('wrong'); 
            } 
         }).get({'dish_id': data['dID']}); 
        
        var commentObject = new CommentClass(wholeCommentBody, commentCountBlock, data['dID'],newestComment);
        var liDoms = dishDom.getElements('p.btm_link a');
        var shopAction = new ShopAction(liDoms[2], liDoms[3], liDoms[4], data['dID']);
        return dishDom;
    },
    refreshDish: function(data){
        if (0 == data){
            this.noUpdate();
            return;
        };
        data.each(function(item){
            this.createDish(item).inject(this.body, 'bottom');
        }.bind(this));
    },
    createFeed: function(data){
        console.log(data);
        var feedDom = new Element('li', {
            'class': 'item_box feed',
            'html': '<li class="item_box feed"> <a href="/user/' + data['user']['uid'] + '"><img class="avatar" src="' + data['user']['pic']['small'] + '" alt="' + data['user']['username'] + '" title="' + data['user']['username'] + '" /></a> <div class="goods_info"> <p class="user"><a href="/user/' + data['user']['uid'] + '"><strong>' + data['user']['username'] + '</strong></a></p> <p class="describe">' + data['cont']['content'] + '</p> <h3><a href="/shop/' + data['cont']['sid'] + '">' + data['cont']['dname'] + '</a></h3> <p class="posted">@<a href="/shop/' + data['cont']['sid'] + '">' + data['cont']['sname'] + '</a></p> <p><a href="/shop/' + data['cont']['sid'] + '"><img class="goods_img" src="' + data['cont']['pic']['middle'] + '"/></a></p> </div> </li>'
        });
        return feedDom;
    },
    refreshFeed: function(data){
        if (0 == data.length){
            this.noUpdate();
            return;
        };
        data.each(function(item){
            this.createFeed(item).inject(this.body, 'bottom');
        }.bind(this));
    },
});

var ShopTabClass = new Class({
    Extends: TabClass,
    initialize: function(tabs, helps, cart_id){
        this.parent(tabs, helps);
        this.cartID = cart_id;
        this.body = $$('.content ul')[0];
        this.notifyDom = $$('.notify')[0];
    },
    makeTabDict: function(tabs){
        var tabDict = new Hash();
        tabs.each(function(item){
            tabDict.include(item.getElement('a').hash.match('#!/menu/(.+)/')[1],  item);
        });
        return tabDict;
    },
    getURL: function(){
        var urlPath = window.location.pathname;
        return urlPath + this.getHashURL();
    },
    getNewActTab: function(){
        return this.getHashURL().match('menu/(.+)/')[1]
    },
    mainProcess: function(response){
        this.refreshDish(response['data']);
    },
    createDish: function(data){
        var cart_id = this.cartID;
        var dishDom = new Element('div', {
            'class': 'shop_goods',
            'html': '<img class="pic" src="' + data['detail']['pic']['middle'] + '" alt="" /> <p><a class="add_cart" href="javascript:;;">加入购物车</a>' + data['detail']['name'] + '<br /> 价格<span>￥' + data['detail']['price'] + '</span></p> <p> <a class="fl" href="javascript:;;">评论(' + data['statistic']['comment'] + ')</a> <a class="fr" href="javascript:;;">吃过(' + data['statistic']['eat'] + ')</a> </p> '
        });
        var shopAction = new ShopAction(null, dishDom.getElement('a.fr'), null, data['dID']);
        dishDom.getElement('.add_cart').addEvent('click', function(){
            new Request.JSON({
                url: '/cart/update/',
                onSuccess: function(response){
                    if (401 == response['ret']){
                        this.login();
                    }else if (440 == response['ret']){
                        this.notify('订单已锁定');
                    }
                }.bind(this)
            }).get({'type': 'add', 'cart_id': cart_id, 'content': data['dID']});
        }.bind(this));
        return dishDom;
    },
    createItemBox: function(){
        var boxDom = new Element('li', {
            'class': 'item_box clearfix',
            'html': '<div class="comments" style="display:none;"><div class="toggle"> <a href="javascript:;;" class="input_btn">查看全部</a> <a href="javascript:;;" class="input_btn">只看好友</a></div><ul class="clearfix"></ul></div>'
        });
        return boxDom;
    },
    refreshDish: function(data){
        if (0 == data.length){
            this.nullUpdate();
            return;
        };
        var itemBox = this.createItemBox();
        var dishDom;
        var wholeCommentBody;
        var commentCountBlock;
        var dishID;
        var commentObject;
        data.each(function(item, index){
            if (0 != index && 0 == index % 3){
                itemBox.inject(this.body, 'bottom');
                itemBox = this.createItemBox();
            };
            // this.createDish(item).inject(itemBox, 'top');
            dishDom = this.createDish(item);
            wholeCommentBody = itemBox.getElements('.comments')[0];
            commentCountBlock = dishDom.getElements('a.fl')[0];
            dishID = item['dID'];
            commentObject = new CommentClass(wholeCommentBody, commentCountBlock, dishID);
            dishDom.inject(itemBox, 'top');
        }.bind(this));
        itemBox.inject(this.body, 'bottom');
    },
    notify: function(s){
        var notifyDom = this.notifyDom;
        notifyDom.set('html', s);
        notifyDom.setStyle('display', 'block');
        var hiddenIt = function(){
            notifyDom.setStyle('display', 'none');
        };
        hiddenIt.delay(1500);
    }
});

var UserTabClass = new Class({
    Extends: HomeTabClass,
    initialize: function(tabs, helps){
        this.parent(tabs, helps);
    },
    getURL: function(){
        user_id = window.location.pathname.match('/user/(.+)/')[1];
        return '/ajax/' + this.getHashURL() + '?user_id=' + user_id;
    },
    mainProcess: function(response){
        this.helpDict['showMore'].setStyle('display', 'block');
        this.anchor = response['anchor'];
        this.refreshFeed(response['data']);
    }
})

var AddFollow = new Class({
    initialize: function(uldom, shop_id){
        if (0 == shop_id){
            this.url = '/ajax/pop/';
        }else{
            this.url = '/shop/customer/?shop_id=' + shop_id;
        }
        this.uldom = uldom;
        this.getData();
    },
    getData: function(){
        var theurl = this.url;
        new Request.JSON({
            url: theurl,
            onSuccess: function(response){
                if ('200' == response['ret']){
                    this.process(response['data']);
                }else{
                    console.log('ERROR ' + response['ret'] + ' ' + response['desc']);
                }
            }.bind(this),
            onFailure: function(response){
                console.log('ERROR ' + response);
            }
        }).get();
    },

    createFollower: function(data){
        var newFollower = new Element('li', {
            'html': '<p class="fr"></p> <a href="/user/' + data['uid'] + '"><img src="' + data['pic']['small'] + '" title="" alt=""/></a> <div class="user_info"> <p><a href="/user/' + data['uid'] + '">' + data['username'] + '</a></p> <p>' +data['rnum'] + '人已关注</p> </div>'
        });
        AddFollow.createFollowLink(data).inject(newFollower.getElement('p'), 'top');
        return newFollower;
    },
    process: function(data){
        data.each(function(item){
            this.createFollower(item).inject(this.uldom, 'bottom');
        }.bind(this))
    }
});
AddFollow.createFollowLink = function(data){
    var followLink = new Element('a',{
        'class': 'input_btn',
        'href': 'javascript:;;'
    });
    var followEvents = {
        'mouseenter': function(){
            followLink.innerHTML = '取消关注';
        },
        'mouseleave': function(){
            followLink.innerHTML = '已关注';
        },
        'click': function(){
            console.log('follow');
            new Request.JSON({
                'url': '/unfollow/' + data['uid'],
                onSuccess: function(response){
                    console.log(response);
                    if (200 == response['ret']){
                        followLink.innerHTML = '关注';
                        followLink.removeEvents();
                        followLink.addEvents(unfollowEvents);
                    }else if (401 == response['ret']){
                        window.setTimeout(function(){
                            window.location.href = '/accounts/login/?next=/home/';
                        }, 0);
                    }
                }
            }).get()
        }
    };
    var unfollowEvents = {
        'click': function(){
            console.log('unfollow');
            new Request.JSON({
                'url': '/follow/' + data['uid'],
                onSuccess: function(response){
                    console.log(response);
                    if (200 == response['ret']){
                        followLink.innerHTML = '已关注';
                        followLink.removeEvents();
                        followLink.addEvents(followEvents);
                    }else if (401 == response['ret']){
                        window.setTimeout(function(){
                            window.location.href = '/accounts/login/?next=/home/';
                        }, 0);
                    }
                }
            }).get();
        }
    };
    if (null == data['follow']){
        followLink.set('html', '我自己');
    }else if (true == data['follow']){
        followLink.addClass('followed');
		followLink.set('html', '已关注')
        followLink.addEvents(followEvents);
    }else{
        followLink.set('html', '关注');
        followLink.addEvents(unfollowEvents);
    };
    return followLink;
}
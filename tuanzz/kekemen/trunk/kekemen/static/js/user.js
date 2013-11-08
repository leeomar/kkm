var xTab = new UserTabClass($$('.tab li'), $$('.pagelist'));

window.addEvent('hashchange', function(){
    xTab.getData();
});

window.addEvent('domready', function(){
    xTab.getData();
    var addPoople = function(dom, list){
        list.each(function(item){
            new Element('li',{
                'html': '<a href="/user/' + item['uid'] + '"><img src="' + item['pic']['small'] + '" alt="" /></a>'
            }).inject(dom, 'bottom');
        });
    };
    AddFollow.createFollowLink(data).inject($('follow'), 'top');
    var ulList = $$('.my_sns div ul');
    new Request.JSON({
        url: 'following/',
        onSuccess: function(response){
            if (200 == response['ret']){
                addPoople(ulList[0], response['data']);
            }
        }
    }).get();
    new Request.JSON({
        url: 'follower/',
        onSuccess: function(response){
            if (200 == response['ret']){
                addPoople(ulList[1], response['data']);
            }
        }
    }).get();
});

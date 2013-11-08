var xTab = new HomeTabClass($$('.tab li'), $$('.pagelist'));

window.addEvent('hashchange', function(){
    xTab.getData();
});

window.addEvent('domready', function(){
    var followUL = $$('.follow ul')[0];
    var addFollow = new AddFollow(followUL, 0);
    var wallDom = $$('.food_wall ul');
    new Request.JSON({
        url: '/ajax/wall',
        onSuccess: function(response){
            if (200 == response['ret']){
                response['data'].each(function(item, index){
                    if (index > 17) return;
	                new Element('li', {
                        'html': '<a href="javascript:;;"><img src="' + item['detail']['pic']['middle'] + '" alt=" 美食" title="美食" /><p>￥' + item['detail']['price'] + '</p></a></li>'
                    }).inject(wallDom[Math.floor(index/6)], 'bottom');
                });
            };
        }
    }).get();
    xTab.getData();
});

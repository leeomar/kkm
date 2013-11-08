var ShopAction = new Class({
    initialize: function(domWant, domEat, domLike, did){
        domList = [domWant, domEat, domLike];
        this.statisticDict = ['want', 'eat', 'like'];
        this.did = did;
        this.actDoms(domList);
    },
    actionIt: function(actUrl, did){
        new Request.JSON({
            url: '/action/' + actUrl + '/' + did,
            onSuccess: function(data){
                if ('200' == data['ret']){
                    var thisRe = this.innerHTML.match('(.{3})([0-9]+)');
                    this.innerHTML = thisRe[1] + (thisRe[2].toInt() + 1) + ')';
                }
            }.bind(this)
        }).get();        
    },
    actDoms: function(domList){
        var actionIt = this.actionIt;
        var statisticDict = this.statisticDict;
        var did = this.did;
        domList.each(function(item, index){
            if (null != item){
                item.addEvent('click', function(){
                    actionIt.bind(this)(statisticDict[index], did);
                    this.removeEvents();
                    this.addEvent('click', function(){
                        alert('您的操作太频繁了');
                    });
                });
            };
        }.bind(this));
    }
});

var Scroll = new Class({
	initialize: function(){
		this.obj = $$('.food_wall ul');
	},
	copyLi: function(){
		this.obj.each(function(sObj, index){
			sItem = sObj.getFirst('li');
			sItem.clone().inject(sObj, 'bottom');
			this.fx1.delay(index*400, this, sItem);
		}.bind(this))
	},
	fx1: function(sItem){
		new Fx.Morph(sItem, {
			duration: '600',
			onComplete: function(){
				sItem.destroy();
			}
		}).start({
			'opacity': '0',
			'width': '0'
			});
	},
	poll: function(){
		return this.copyLi.periodical(3000, this);
	}
});


window.addEvent('domready', function(){
	var scroll = new Scroll();
	var timer = scroll.poll();
	$$('.food_wall').addEvents({
		'mouseenter': function(){
			$clear(timer);
		},
		'mouseleave': function(){
			timer = scroll.poll();
		}
	});
});



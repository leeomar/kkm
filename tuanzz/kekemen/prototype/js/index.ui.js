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
	$$('.show_cate_box').addEvent('click', function(){
		var showBox = $$('.cate_box')[0];
		var sHeight = showBox.getStyle('height');
		console.debug(sHeight);
		new Fx.Morph(showBox, {
			duration: '200',
			onComplete: function(){
				showBox.getElements('li').each(function(item){
					item.setStyle('visibility','visible');
				});
			}
		}).start({
			'visibility': 'visible',
			'width': [0,'150px'],
			'height': [0,sHeight]
		});
	});


});



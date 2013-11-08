var CommentClass = new Class({
    initialize: function(wholeCommentBody, commentCountBlock, dishID, newestComment){
       
        this.commentBody = wholeCommentBody.getElement('ul.clearfix');
        this.wholecomment = wholeCommentBody;
        this.hasshowed = false;//标记是否在展开状态
        this.dishID = dishID; this.commentCountBlock = commentCountBlock; 
        this.commentCount = this.commentCountBlock.get('html').match('[0-9]+')[0].toInt();
        this.commentState = 0; //0代表所有，1代表朋友
        this.newestComment = newestComment;
        var commentButton = this.commentCountBlock;
        commentButton.addEvent('click',
            function(){
                this.showComments();
                var checkAllButton = this.wholecomment.getElements('.toggle a')[0];
                checkAllButton.removeEvents(); 
                checkAllButton.addEvent('click',
                    function(){
                        console.log('check all'); 
                        this.commentState = 0;
                        this.refreshComments();
                    }.bind(this)
                );
                var checkFriendButton = this.wholecomment.getElements('.toggle a')[1];
                checkFriendButton.removeEvents();
                checkFriendButton.addEvent('click',
                    function(){
                        this.commentstate = 1;
                        this.refreshFriendComments();
                    }.bind(this)
                );
            }.bind(this));
        this.refreshComments();//得到评论
        
        
       
    },

    showComments: function()
    {
        if(this.hasshowed == false)
        {
            if(CommentClass.nowComment == '')
            {
                ;
            }
            else
            {
                CommentClass.nowComment.showComments();
            }
            CommentClass.nowComment = this;
            this.wholecomment.setStyle('display', 'block');
            this.commentCountBlock.set('html', '关闭评论(' + this.commentCount + ')');
            this.refreshComments();
            this.hasshowed = true;
        }
        else{
            CommentClass.nowComment = '';
            this.wholecomment.setStyle('display', 'none');
            this.commentCountBlock.set('html', '评论(' + this.commentCount + ')');
            this.hasshowed = false;
        }
        //this.updateNewestComment();
    },

    updateNewestComment: function()
    {
        
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
                                this.newestComment.set('html', '');
                                commentDom.inject(this.newestComment, 'bottom');
                            }
                        }.bind(this));
                    }
            }.bind(this), 
            onFailure: function(response){ 
                console.log('wrong'); 
            } 
         }).get({'dish_id': this.dishID}); 
    },
    refreshFriendComments: function()
    {
        new Request.JSON({
            url: '/friend/comment/get/',
            onSuccess: function(response) {
                if(response['ret'] == 200)
                {
                    var data = response['data'];
                    this.commentBody.set('html','');
                    data.each(function(item){
                        this.createCommentDom(item).inject(this.commentBody, 'top');
                    }.bind(this));
                    this.createCommentResponse(data).inject(this.commentBody, 'bottom');
                }
                else if(401 == response['ret']){
                    this.login();
                }
            }.bind(this),
            onFailure: function(response){
                console.log('wrong');
            }
        }).get({'dish_id': this.dishID});

    },
          
    login: function(){
        var urlPath = window.location.pathname;
        var urlHash = window.location.hash;
        window.setTimeout(function(){
            window.location.href = '/accounts/login/?next=' + encodeURIComponent(urlPath + urlHash);
        }, 0);
    },
    refreshComments: function()
    {
        new Request.JSON({
            url: '/comment/get/',
            onSuccess: function(response) {
                if(response['ret'] == 200)
                {
                    var data = response['data'];
                    this.commentBody.set('html','');
                    data.each(function(item){
                        this.createCommentDom(item).inject(this.commentBody, 'top');
                    }.bind(this));
                    this.createCommentResponse(data).inject(this.commentBody, 'bottom');
                }
                else if(401 == response['ret']){
                        this.login(); 
                     } 
            }.bind(this), 
            onFailure: function(response){ 
                console.log('wrong'); 
            } 
         }).get({'dish_id': this.dishID}); 
    },
    createCommentDom: function(data) { 
        var commentDom = new Element('li',{'html': '<a href="#"><img class="avatar" src="'+data['user']['pic']['small']+ '"/></a><p><a href="#">'+data['user']['username']+'</a><span>'+data['ts']+'</span></p><p>'+data['cont']+'</p>'}); 
        return commentDom; 
    },
    
    addClass: function(classname, node)
    {
        node.className += ' '+classname;
        return node.className;
    },
    

    createCommentResponse: function(data) 
    { 
        var commentResponseDom = new Element('li',
                { 'class': 'respond', 
                'html': '<form class="comment_response" action="#" method="post"><image class="avatar" src="images/avatar2.jpg" alt=""/><div class="input_border">'
            +'<textarea class="input_text" row="2" cols="30"></textarea></div>'
            +'<p><input type="submit" value="提交评论" class="input_btn"/></p><form/>'
        });
        var commentResponseForm = commentResponseDom.getElement('.comment_response');
        var contentBox1 = commentResponseForm.getElement('.input_text');
        contentBox1.onfocus = function()
        {
                this.className +='focus';
        };
        contentBox1.onblur = function()
        {
            this.className = 'input_text';
        };
        contentBox1.onmouseout = function()
        {
            this.blur();
        };
        commentResponseForm.addEvent(
                'submit', function(e){                                                                                                                                     
                new Event(e).stop();
                var contentBox = commentResponseForm.getElement('.input_text');
                var content = contentBox.get('value');
                if(content.trim() == '')
                {
                    alert('评论内容不能为空！');
                    return ; 
                }
                new Request.JSON(
                {
                    url: '/comment/add/',
                    onSuccess: function(response){
                        if(401 == response['ret']){
                                this.login();
                        }
                    }.bind(this),
                    onFailure: function(response){
                        console.log('failed');

                    }
                }).get({'dish_id': this.dishID, 'content': content});
                contentBox.set('value', '');
                if(this.commentState == 0)
                {
                    this.refreshComments();
                }
                else{
                    this.refreshFriendComments();
                }
                this.commentCount++;
                this.commentCountBlock.set('html', '关闭评论('+this.commentCount+')');
                this.updateNewestComment();
            }.bind(this)
        );
            return commentResponseDom;

    }

});
CommentClass.nowComment = '';

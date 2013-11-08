var orderViewComment = new Class({
initialize: function(){
    console.log('why');
    this.supportframe = $$('.supportframe');
    console.log(this.supportframe);
    this.supportframe.addEvent('onload', function(){
        alert('OK');

    });
    this.allMainBody = $$('tbody.dishesBody')[0];
    console.log(this.allMainBody);
    this.items = this.allMainBody.getElements('tr');
    console.log(this.items);
    var commentButtonDom;
    var commentWholeBody;
    this.items.each(function(item,index){
        
        var dishID = item.get('id');
        if(index%2 == 0)
        {
            commentButtonDom = item.getElements('.input_btn')[0];
        }
        else{
            commentWholeBody = item;
            var commentObject = new commentClass(commentWholeBody,commentButtonDom, dishID);
        }

    }.bind(this));
    /* 评价店铺
    console.log($$('.shopcomment'));
    var shopcommentResponseForm = $$('.shopcomment')[0].getElements('form')[0];
    console.log('##');
    console.log(shopcommentResponseForm);
    
    shopcommentResponseForm.addEvent(
        'submit',  function(e){
        new Event(e).stop();
        var contentBox =shopcommentResponseForm.getElements('.input_text')[0];
        var content = contentBox.get('value');
        if(content.trim() == '')
        {
            alert('评论不可为空！');
            return ;
        }
        
        new Request.JSON(
        {
            

            url: '/comment/add/',
            onSuccess: function(response){
                console.log(response['ret']);
                if(401 == response['ret'])
                {
                    console.log('未登录');
                }
            }.bind(this)

        }).get({'dish_id': this.dishID, 'content': content});
        contentBox.set('value', '');
    }.bind(this)   
    );
    */



},

});

var commentClass=new Class({
initialize: function(wholeCommentBody, commentButton, dishID)
{
    this.dishID=dishID;
    this.hasshowed = false;
    this.wholeCommentBody = wholeCommentBody;
    this.thankyouP = this.createThankyouP();
    this.thankyouP.inject(this.wholeCommentBody, 'after');
    this.thankyouP.setStyle('display', 'none');
    var commentResponseForm = this.wholeCommentBody.getElement('.comment_response');
    var uploadPictureButton = commentResponseForm.getElements('.input_btn')[0];//功能先不实现
    commentButton.addEvent('click',
        function(){
            this.thankyouP.setStyle('display', 'none');
            this.showComment();
        }.bind(this)
    );
    commentResponseForm.addEvent(
        'submit',  function(e){
        new Event(e).stop();
        var contentBox = commentResponseForm.getElements('.input_text')[0];
        var content = contentBox.get('value');
        var pictureBox = commentResponseForm.getElements('.picUrl')[0];
        var pictureFile = '';
        console.log(pictureBox);
        pictureFile = pictureBox.get('value').src;
        console.log('picturefile');
        console.log(pictureFile);
        if(content.trim() == '')
        {
            alert('评论不可为空！');
            return ;
        }
        commentResponseForm.submit({

                onSuccess: function(response){
                    console.log('response');
                    console.log(response);
                },
                onComplete: function(response){
                    console.log(response);
                }
        });
        console.log('success1');
        contentBox.set('value','');
        pictureBox.set('value', '');
        this.showComment();
        this.thankyouP.setStyle('display', '');
    }.bind(this));
},
    
createThankyouP: function()
{
    thankyouDom = new Element('p',{
        'html': '<p> 感谢您的评论 </p>'
    });
    return thankyouDom;
},
showComment: function()
{
    console.log(commentClass.nowComment);
    if(this.hasshowed == false)
    {
        if(commentClass.nowComment == '')
        {
            ;
        }
        else{
            commentClass.nowComment.showComment();
            
        }
        commentClass.nowComment = this;
        this.wholeCommentBody.setStyle('display', '');
        this.hasshowed = true;
    }
    else{
        commentClass.nowComment = '';
        this.wholeCommentBody.setStyle('display', 'none');
        this.hasshowed = false;
    }
},
/*
createCommentBody: function()
{
    commentBodyDom=new Element('tr',{
        'html': '<td style=" text-align:right;" colspan="6" ><form action="/image/save/" method="post" class="comment_response" enctype="multipart/form-data"><p><textarea id="" class="input_text" name="content" rows="10" clos="30"></textarea></p><p><input name="imgfile" type="file" class="picUrl" value="" /></p><p><input type="hidden" name="dish_id" value="'+this.dishID+'"/><input type="button" class="input_btn" value="添加图片" /><input type="submit" class="input_btn" value="提交评论" /></p></form></td>'
    });
    return commentBodyDom;




},
*/

    

});
commentClass.nowComment = '';
window.addEvent('domready',  function(){
    console.log('?');
    var orderViewCommentClass = new orderViewComment();
    console.log('here');

});

function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    }
  }
}

function insertAfter(newElement,targetElement) {
  var parent = targetElement.parentNode;
  if (parent.lastChild == targetElement) {
    parent.appendChild(newElement);
  } else {
    parent.insertBefore(newElement,targetElement.nextSibling);
  }
}

function addClass(element,value) {
  if (!element.className) {
    element.className = value;
  } else {
    newClassName = element.className;
    newClassName+= " ";
    newClassName+= value;
    element.className = newClassName;
  }
}

function removeClass(element, value) {
	var oldClassName = element.className;
	var reg = eval("/\s*"+value+"/");
	if (reg.test(oldClassName)) {
		element.className = oldClassName.replace(reg, "");
	}
}

function ddHighLight() {
	var date_list = document.getElementById("date_list");
	var dd_list = document.getElementsByTagName("dd");
	for (var i=0, len=dd_list.length; i<len; i++) {
		dd_list[i].onmouseover = function() {
			addClass(this, "hover");
		}
		dd_list[i].onmouseout = function() {
			removeClass(this, "hover");
		}
	}
}

function setTab(name,cursel,n) {
	for(i=1;i<=n;i++) {
		var menu = document.getElementById(name+i);
	 	var con = document.getElementById("con_"+name+"_"+i);
		if (i == cursel) {
			addClass(menu, "hover");
		} else {
			removeClass(menu, "hover");
		}
	 	con.style.display = (i==cursel) ? "block" : "none";
	}    
}

function showPlace() {
	var change_place = document.getElementById("change_place");
	var choice_place = document.getElementById("choice_place");
	var close = document.getElementById("close");
	var show = function() {
		choice_place.style.display = "block";
	}
	var hide = function() {
		choice_place.style.display = "none";
	}
	change_place.onclick = function() {
		show();
	}
	close.onclick = function() {
		hide();
	}
}

function modify() {
	var phone_value = document.getElementById("mobile_phone").firstChild.nodeValue;
	var addres_value = document.getElementById("address").firstChild.nodeValue;
	var modify_info = document.getElementById("modify_info");
	var account_info = document.getElementById("account_info");
	account_info.style.display = "none";
	modify_info.style.display = "block";
	document.getElementById("m_mobile").value = phone_value;
	document.getElementById("m_address").value = addres_value;
}

function saveModify() {
	var modify_info = document.getElementById("modify_info");
	var account_info = document.getElementById("account_info");
	account_info.style.display = "block";
	modify_info.style.display = "none";
}

function countDown() {
	var now = new Date();
	var end_year = now.getFullYear();
	var end_month = now.getMonth() + 1;
	var end_date = now.getDate();
	if(end_month < 10) {
		end_month = "0" + end_month;
	}
	if(end_date < 10) {
		end_date = "0" + end_date;
	}
	var deadline = new Date(end_year + "/" + end_month + "/" + end_date);

	//var timeDiff = now.getTimezoneOffset();
	//var leave = deadline.getTime() + 11*3600*1000  - now.getTime() + timeDiff*60*1000;
	var leave = deadline.getTime() + 11*3600*1000  - now.getTime()
	var minute = 1000 * 60;
	var hour = minute * 60;
	var day = hour * 24;
	var countDay = Math.floor(leave/day);
	var countHour = Math.floor(leave/hour - countDay*24);
	var countMinute = Math.floor(leave/minute) - countDay*24*60 - countHour*60;
	var countSecond = Math.floor(leave/1000) - countDay*24*60*60 - countHour*60*60 - countMinute*60;

	var today_menu = document.getElementById("today_menu"); 
	var tomorrow_menu = document.getElementById("tomorrow_menu"); 
	var after_tmr_menu = document.getElementById("after_tmr_menu");
	var today_shadow = document.getElementById("today_shadow");
	if(leave < 0) {
		today_shadow.className = "cate_list_shadow";
		today_menu.innerHTML = "今日点餐时间已结束！";
		tomorrow_menu.innerHTML = "点餐剩余时间：<span>"+countHour+"</span>小时 <span>"+countMinute+"</span>分 <span>"+countSecond+"</span>秒";
		after_tmr_menu.innerHTML = "点餐剩余时间：<span>1</span>天 <span>"+countHour+"</span>小时 <span>"+countMinute+"</span>分 <span>"+countSecond+"</span>秒";
	} else {
		today_shadow.className = "cate_list";
		today_menu.innerHTML = "点餐剩余时间：<span>"+countHour+"</span>小时 <span>"+countMinute+"</span>分 <span>"+countSecond+"</span>秒";
		tomorrow_menu.innerHTML = "点餐剩余时间：<span>1</span>天 <span>"+countHour+"</span>小时 <span>"+countMinute+"</span>分 <span>"+countSecond+"</span>秒";
		after_tmr_menu.innerHTML = "点餐剩余时间：<span>2</span>天 <span>"+countHour+"</span>小时 <span>"+countMinute+"</span>分 <span>"+countSecond+"</span>秒";
	}
} 

function runCountDown() {
	setInterval("countDown()", 1000);
}

window.onscroll = function() {
	var scrollTop = Math.max(document.documentElement.scrollTop, document.body.scrollTop);		
	var cart_list = document.getElementById("cart_list");
	var after_tmr = document.getElementById("after_tmr");
	var x = after_tmr.getBoundingClientRect().right;
	if(scrollTop > 324) {
		cart_list.style.position = "fixed";
		cart_list.style.left = x+"px";
		cart_list.style.top = 0;
		cart_list.style.zIndex = 2;
	} else {
		cart_list.style.position = "relative";
		cart_list.style.left = 0;
		cart_list.style.top = 0;
	}
}

//splide script;
function $(id) { return document.getElementById(id); }

function moveElement(elementID,final_x,final_y,interval) {
  if (!document.getElementById) return false;
  if (!document.getElementById(elementID)) return false;
  var elem = document.getElementById(elementID);
  if (elem.movement) {
    clearTimeout(elem.movement);
  }
  if (!elem.style.left) {
    elem.style.left = "0px";
  }
  if (!elem.style.top) {
    elem.style.top = "0px";
  }
  var xpos = parseInt(elem.style.left);
  var ypos = parseInt(elem.style.top);
  if (xpos == final_x && ypos == final_y) {
		return true;
  }
  if (xpos < final_x) {
    var dist = Math.ceil((final_x - xpos)/10);
    xpos = xpos + dist;
  }
  if (xpos > final_x) {
    var dist = Math.ceil((xpos - final_x)/10);
    xpos = xpos - dist;
  }
  if (ypos < final_y) {
    var dist = Math.ceil((final_y - ypos)/10);
    ypos = ypos + dist;
  }
  if (ypos > final_y) {
    var dist = Math.ceil((ypos - final_y)/10);
    ypos = ypos - dist;
  }
  elem.style.left = xpos + "px";
  elem.style.top = ypos + "px";
  var repeat = "moveElement('"+elementID+"',"+final_x+","+final_y+","+interval+")";
  elem.movement = setTimeout(repeat,interval);
}

function classNormal(iFocusBtnID,iFocusTxID){
	var iFocusBtns= $(iFocusBtnID).getElementsByTagName('li');
	var iFocusTxs = $(iFocusTxID).getElementsByTagName('li');
	for(var i=0; i<iFocusBtns.length; i++) {
		iFocusBtns[i].className='not_show';
		iFocusTxs[i].className='normal';
	}
}

function classCurrent(iFocusBtnID,iFocusTxID,n){
	var iFocusBtns= $(iFocusBtnID).getElementsByTagName('li');
	var iFocusTxs = $(iFocusTxID).getElementsByTagName('li');
	iFocusBtns[n].className='current';
	iFocusTxs[n].className='current';
}

function iFocusChange() {
	if(!$('ifocus')) return false;
	var iFocusBtns = $('ifocus_btn').getElementsByTagName('li');
	var listLength = iFocusBtns.length;
	iFocusBtns[0].onmouseover = function() {
		moveElement('ifocus_piclist',0,0,5);
		classNormal('ifocus_btn','ifocus_tx');
		classCurrent('ifocus_btn','ifocus_tx',0);
	}
	if (listLength>=2) {
		iFocusBtns[1].onmouseover = function() {
			moveElement('ifocus_piclist',-960,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',1);
		}
	}
	if (listLength>=3) {
		iFocusBtns[2].onmouseover = function() {
			moveElement('ifocus_piclist',-1920,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',2);
		}
	}
	if (listLength>=4) {
		iFocusBtns[3].onmouseover = function() {
			moveElement('ifocus_piclist',-2880,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',3);
		}
	}
}

var timer;
function autoiFocus() {
	if(!$('ifocus')) return false;
	var atuokey = false;
	$('ifocus').onmouseover = function(){atuokey = true};
	$('ifocus').onmouseout = function(){atuokey = false};
	var focusBtnList = $('ifocus_btn').getElementsByTagName('li');
	var listLength = focusBtnList.length;
	if(timer) {
		clearInterval(timer);
		timer = null;
	}
	timer= setInterval( function(){
		if(atuokey) return false;
		for(var i=0; i<listLength; i++) {
			if (focusBtnList[i].className == 'current') var currentNum = i;
		}
		if (currentNum==0&&listLength!=1 ){
			moveElement('ifocus_piclist',-960,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',1);
		}
		if (currentNum==1&&listLength!=2 ){
			moveElement('ifocus_piclist',-1920,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',2);
		}
		if (currentNum==2&&listLength!=3 ){
			moveElement('ifocus_piclist',-2880,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',3);
		}
		if (currentNum==2 ){
			moveElement('ifocus_piclist',0,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',0);
		}
		if (currentNum==1&&listLength==2 ){
			moveElement('ifocus_piclist',0,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',0);
		}
		if (currentNum==2&&listLength==3 ){
			moveElement('ifocus_piclist',0,0,5);
			classNormal('ifocus_btn','ifocus_tx');
			classCurrent('ifocus_btn','ifocus_tx',0);
		}
	},3000);
}
addLoadEvent(iFocusChange);
addLoadEvent(autoiFocus);

addLoadEvent(ddHighLight);
addLoadEvent(showPlace);
addLoadEvent(runCountDown);















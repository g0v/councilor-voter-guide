
import {YTT }  from '../youtube.js';
import {GLOBAL} from '../config.js';
import {getBrowserHeight,getBrowserWidth ,updateImg } from "../common.js";

export {Main}

class Main{
	constructor(NAME='main' , ifFB = false , ifYT = false, ifScrollHandle = false ){
		this.NAME = NAME;
		this.ifFB = ifFB;
		this.ifYT = ifYT;	
		this.ifScrollHandle = ifScrollHandle;
	}
	bind(){
		console.log(this.NAME + ' binding.....');
		
	}
	init(){
		console.log(this.NAME + ' initialing.....');
		let interval
		if(this.ifFB){
			console.log('page:'+ this.NAME + ' add fb ing.....');
		}
		if(this.ifYT){
			console.log('page:'+ this.NAME + ' add youtube.....');
			this.YT = new YTT($('.yt').data('id') , 'player');
  			onYouTubeIframeAPIReady = this.YT.onYouTubeIframeAPIReady;
		}
		if(this.ifScrollHandle){
			

			window.onscroll = function(e) {_scrollHandle(e);}

			
			
				function _scrollHandle(e) {
				    // if(e){
				    // 	e.preventDefault();
				    // }
				    let page = $('#page').val();
				    let top = $(window).scrollTop();
				    const bg = $('.navbar .bg-cover')
				    const statenav = $('.navbar-menu').attr('data-toggle');
				    let dir = (GLOBAL.oldtop < top) ? 'down' : 'up';
				    GLOBAL.top = top;		    if(top>60 || statenav == 'expand'){
			    	TweenMax.to(bg , .5, {opacity:1,ease:Expo.easeOut})	
			    }else{
			    	TweenMax.to(bg , .5, {opacity:0,ease:Expo.easeOut})
			    }

			    if(page == 'index'){
			    	let vh = getBrowserHeight();
			    	clearTimeout(interval)
			    	
			    	if(top>=vh - 80){
			    		$('.navbar-brand').stop().fadeIn(500);
			    		
			    	}else{
			    		$('.navbar-brand').stop().fadeOut();
			    		
			    	}

			    }else{
			    	$('.navbar-brand').fadeIn(500);
			    }



			    if(page.indexOf('resume')>=0){
			    	if(statenav == 'collapse'){
			    		if(top>60){
			    			TweenMax.to($('.navbar') , .5 , {top:-$('.navbar').height(),ease:Expo.easeOut})	
			    			TweenMax.to($('.wrapper-header') , .5 , {top:0,ease:Expo.easeOut})	
			    		}else{
			    			TweenMax.to($('.navbar') , .5, {top:0,ease:Expo.easeOut});
			    			TweenMax.to($('.wrapper-header') , .5 , {top:$('.navbar').height(),ease:Expo.easeOut})	
			    		}

			    	}
			    }
			    GLOBAL.oldtop = top
			}
			_scrollHandle();
		}
		if(location.href.indexOf('localhost')	>=0)
		{
			this.TEST = true;
			console.log('run test mode......')
		}
		
    /*common component*/
		//new SUB_MENU();
		this.bind();   
	}
	onresize(handle){
		$( window ).resize(handle);
	}
}
/*
處理滾動頁面選單
 */


import {GLOBAL} from './config.js';
import {getBrowserHeight,getBrowserWidth ,updateImg } from "./common.js";
export{SUB_MENU}
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class SUB_MENU{
	constructor( data ){
		this.data = data;	
		this.DOM = $(".nav-inside");
		this.logo = this.DOM.find('.logo')
		this.page = $('#page').val();
		this.update = this.update.bind(this);
		this.state = 'st'
		this.init();
	}
	init(){
		this.update();
		this.bind();
	}
	
	update() {

	    if (GLOBAL.top > 500) {
	        if (this.state != 'fx') {
	            this.DOM.css({ "position": "fixed", 'top': 0, 'left': 0, "z-index": 1000, 'width': '100%' });
	            this.logo.fadeIn('fast');
	            if (Number(getBrowserWidth()) >= 768) {
	                $('.sec1 > .title').css({ 'margin-top': 180 })
	                //TweenMax.to($('.sec1 > .title') , .5 , {css:{marginTop:280,autoRound:false}})
	            }
	        }
	        this.state = 'fx'
	    } else {
	        this.DOM.css("position", "static");
	        this.logo.fadeOut('fast');
	        this.state = 'st'
	        if (Number(getBrowserWidth()) >= 768) {
	            $('.sec1 > .title').css({ 'margin-top': 100 })
	        }
	    }
	    setTimeout(this.update, 100);
	}
	bind(){
		$(" .navbar-nav a.custom.hash, .nav-inside a.custom.hash").each(function() {
		    $(this).click(function(e) {
		        e.preventDefault();
		        var act = $(this).data("ga");
		        var link = $(this).data("href");
		        GLOBAL.ga.GT('/menu', '.btn.' + act);
		        setTimeout(function() { route(act); }, 300);
		        return false;
		    })

		})
		function route(id) {
		    if (id.indexOf("top") >= 0) {
		        let top = 0
		            //TweenMax.set(window, {scrollTo:{y:top}});
		        $body.animate({
		            scrollTop: top
		        }, 600);
		    } else if (id.indexOf("intro") >= 0) {
		        let top = $(".sec1").offset().top - 100
		            //TweenMax.set(window, {scrollTo:{y:top}});
		        $body.animate({
		            scrollTop: top
		        }, 600);
		    } else if (id.indexOf("drive") >= 0) {
		        let top = $(".sec2").offset().top - 100
		            //TweenMax.set(window, {scrollTo:{y:top}});
		        $body.animate({
		            scrollTop: top
		        }, 600);
		    } else  if (id.indexOf("spec") >= 0) {
		        let top = $(".sec3").offset().top- 100
		            //TweenMax.set(window, {scrollTo:{y:top}});
		        $body.animate({
		            scrollTop: top
		        }, 600);
		    } else  if (id.indexOf("feature") >= 0) {
		        let top = $(".sec4").offset().top - 100
		            //TweenMax.set(window, {scrollTo:{y:top}});
		        $body.animate({
		            scrollTop: top
		        }, 600);
		    } else   {
		        let top = $(".sec5").offset().top - 100
		            //TweenMax.set(window, {scrollTo:{y:top}});
		        $body.animate({
		            scrollTop: top
		        }, 1000);
		    } 
		    $('.collapse').collapse('hide')
		}
	}
	anim(){		
	}
}
//import _ from 'underscore';
import { GLOBAL } from '../config.js';
import { getQueryVariable, getBrowserHeight, getBrowserWidth, getParameterByName, updateImg } from '../common.js';
import { Main } from "./main.js";
//import { FB_ASSET } from "../fb_assets.js";
//import { ARROWS } from "../arrows.js";
export {
    DEFAULT as DEFAULT,
};
// String.prototype.replaceAll = function(search, replacement) {
//     var target = this;
//     return target.replace(new RegExp(search, 'g'), replacement);
// };
var $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
class DEFAULT extends Main {
    constructor(NAME = 'default', ifFB = true, ifYT = false, ifScrollHandle = true) {
        super(NAME, ifFB, ifYT, ifScrollHandle);
        this.TEST = false;
        // this.data = new DATA();
        // this.data.init();
        
        this.init();
        this.watchScroll();
        // let hash = this.chkIgContainsHash();
        // this.datafetch( hash );
        
    }
    init() {
        let context = this;
        super.init();
        this.anim()
        
    }
    anim() {
        
        let pg = $('#page').val();
        console.log('anim init...' + pg );
        if(pg == 'about'){
            TweenMax.fromTo($('.part-left')  , .5 , {y:-50 , opacity:0} , {delay:.8, y:0 , opacity  :1 ,ease:Expo.easeOut})
            TweenMax.fromTo($('.part-right')  , .5 , {y:50 , opacity:0} , {delay:.8, y:0 , opacity  :1 ,ease:Expo.easeOut})
            TweenMax.fromTo($('.bg-right') , .5, {scaleY:0} , {delay:.5,scaleY:1 , transformOrigin:"0 100%"})    
        }
        
    }
    
    watchScroll() {

    }
    
    bind() {
        
    }

}


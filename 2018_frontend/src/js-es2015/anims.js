
export{
	loopArr as loopArr,
	AnimBlur as AnimBlur,
	AnimSatur as AnimSatur,
	SmoothRoller,
	AnimMask,
	AnimContrast,
	loopAnim,
	AnimBright,
};
import {getBrowserWidth} from "./common.js";
function loopArr(obj, period , delay , offset) {
		    TweenMax.killTweensOf(obj);		   	
		    TweenMax.to(obj, period / 2,  offset );
		    
		    TweenMax.to(obj, period / 2, {
		        delay: (offset.delay==0)?delay + period / 2 :delay * 2 + period / 2,
		        x:0,
		        y:0,
		        opacity:1,
		        rotation: 0,
		        scaleX:1, scaleY:1, 
		        ease: offset.ease,
		        transformOrigin:offset.transformOrigin,
		        onComplete: function() {
		        	offset.delay = delay;
		            loopArr(obj, period,delay, offset)
		        }
		    })
		    //setTimeout( function(){loopArr(obj , period , offset)}, period * 1000 + 200 );
		}
/**/
function loopAnim(obj, period , delay , createoffset){
	TweenMax.killTweensOf(obj);
	let prop = createoffset();
	prop.delay = 0;
	prop.onComplete =  function() {
	        loopAnim(obj, period, delay, createoffset)
	}
	setTimeout(function(){
		TweenMax.fromTo(obj, period / 2,  {x:0 , y:0 , opacity:1 }, prop)
	} , delay * 1000)
	
		  
}
/*
BLUR
 */

function AnimBlur(OBJ , fromBLUR=0 , toBLUR=5 , time=1 , delay=0){
	let blurElement = OBJ
	let prop = { blur: fromBLUR }

	applyBlur( blurElement, prop)
	TweenMax.fromTo(prop, time ,{blur:fromBLUR},{delay:delay, blur: toBLUR, onUpdate: applyBlur, onUpdateParams: [blurElement, prop] })
	    //here you pass the filter to the DOM element
	function applyBlur(obj, prop) {
	  //  console.log(prop.blur)
	    let a = prop.blur
	    TweenMax.set(obj, { filter: "blur(" + a + "px)", webkitFilter: "blur(" + a + "px)" });
	}

}
function AnimSatur(OBJ , from=0 , to=5 , time=1 , delay=0){
	let blurElement = OBJ
	let prop = { sat: from }

	applyBlur( blurElement, prop)
	TweenMax.fromTo(prop, time ,{sat:from},{delay:delay, sat: to, onUpdate: applyBlur, onUpdateParams: [blurElement, prop] })
	    //here you pass the filter to the DOM element
	function applyBlur(obj, prop) {
	  //  console.log(prop.blur)
	    let a = prop.sat
	    TweenMax.set(obj, { filter: "saturate(" + a + ")", webkitFilter: "saturate(" + a + ")" });
	}

}
function AnimBright(OBJ , from=0 , to=5 , time=1 , delay=0 ,cb =null){
	let blurElement = OBJ
	let prop = { val: from }

	applyBlur( blurElement, prop)
	TweenMax.fromTo(prop, time ,{val:from},{delay:delay, val: to, onUpdate: applyBlur, onUpdateParams: [blurElement, prop] , onComplete:function(){
		if(cb){
			
			cb();
		}
	} })
	    //here you pass the filter to the DOM element
	function applyBlur(obj, prop) {
	  //  console.log(prop.blur)
	    let a = prop.val
	    TweenMax.set(obj, { filter: "brightness(" + a + ")", webkitFilter: "brightness(" + a + ")" });
	}

}
function AnimContrast(OBJ , from=0 , to=5 , time=1 , delay=0){
	let blurElement = OBJ
	let prop = { sat: from }

	applyBlur( blurElement, prop)
	TweenMax.fromTo(prop, time ,{sat:from},{delay:delay, sat: to, onUpdate: applyBlur, onUpdateParams: [blurElement, prop] })
	    //here you pass the filter to the DOM element
	function applyBlur(obj, prop) {
	  //  console.log(prop.blur)
	    let a = prop.sat
	    TweenMax.set(obj, { filter: "contrast(" + a + ")", webkitFilter: "saturate(" + a + ")" });
	}

}
function AnimMask(obj,cp1,cp2,t,ease){
	TweenMax.to(obj , t, /*{clip:cp1 },*/{delay:.1,clip:cp2,ease:ease })
}
/*
隨著父層的left
不斷更新屬性x
 */
class SmoothRoller{
	constructor( DOM , Ks= {'bottom1':-.4 , 'bottom2':-.3 , 'waso':-.2 , 'prd':-.32, 'model':.2}){
		this.DOM = DOM;
		this.CENTER  = 0;
		this.Ks = Ks;
		this.render = this.render.bind(this);
		this.init();
	}
	init(){
		this.render();
	}
	render() {
		const k = this.Ks
		const dom = this.DOM
		this.DOM.find('> div').each(function(){
			let center = getBrowserWidth()/2;
			let posx = parseInt(dom.css('left'));
			let name = $(this).data('name');
			if(typeof name != 'undefined'){
				let newx = (posx-center) * k[name] 
				TweenMax.set($(this) , {x:newx })
			}
			
		});
		setTimeout( this.render, 1000/30)
	}
}



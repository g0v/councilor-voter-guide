
import {getLengthInBytes} from './common.js';
export{ validateAndUpdate,
		Validator,
		inputManager,
		inputManager_school}


function validateAndUpdate(validator, typ){
		
		let val = $('.sec3 .inputs .input-'+typ+' input').val();

		let state = (typ=='name')? validator.chk_input(val): validator.chk_input2(val);
		let ph = $('.sec3 .inputs .ph' +typ)
		if(state==0 || state=='>'){
			// $('.c3 .btn-items .custom-item input').val('')
			ph.html("不符合字數限制喔！");
			return false;
		}else if(state=='lang'){
			ph.html("你講哪國話啊？");
			return false;
		}
		ph.html('')
		$('.sec3 .paper .'+typ+'t').html(val);
		return true;

}
class Validator {
	constructor( ) {
		//this.input = input;
	}	
	//檢查是否
	chk_input(str) {
			const Chinese = /^[\u4e00-\u9fa5]+$/;
			const english = /^[A-Za-z ]*$/;
			const MAX = 10;
			let state = 1;
			
			
			let t = $.trim(str).toString();
			if (getLengthInBytes(t) == 0) {
				state = '0';
				return state;
			} else if (getLengthInBytes(t) > MAX) {
				state = '>';return state;
			} 
			
			console.log('t....'+t)
			for(var i in t){
				if(!Chinese.test(t.charAt(i))){
					if(!english.test(t.charAt(i))){
						console.log(t.charAt(i))
						
						return state='lang';
					}
				}
			}
			return state;
	}
	chk_input2(str) {
			const Chinese = /^[\u4e00-\u9fa5]+$/;
			let state = 1;
			const MAX = 14;
			const  english = /^[A-Za-z ]*$/;
			
			let t = $.trim(str).toString();
			if (getLengthInBytes(t) == 0) {
				state = '0';
				return state;
			} else if (getLengthInBytes(t) > MAX) {
				state = '>';return state;
			} 
			
			console.log('t....'+t)
			for(var i in t){
				if(!Chinese.test(t.charAt(i))){
						
						return state='lang';
					
				}
			}
			return state;
	}

	validate() {
		let val = this.input.val();
		let state = this.chk_input(val);
		if (state != 1) {
			alert("您的宣言不符合字數限制喔！");
			return {tof:false , t:null};
		};
		return {tof:true , t: break_words(val)};

		
	}
		/*檢查FB 初始化*/
	
}
class inputManager {
	constructor(input ,validateAndUpdate,validator) {
		this.input = input;
		
		this.validateAndUpdate = validateAndUpdate;
		this.validator = validator;
		this.interval = {}
		this.init();

	}
	init() {
		this.bind();

	}
	bind() {
		
		this.input.on('change keydown keyup', function() {
			
			clearTimeout(this.interval);
			let val = this.input.val();
			const context = this;
			this.interval = setTimeout(function() {
				context.loop(val)
			}, 100);

		}.bind(this))
	}

	loop(val){
		if ($.trim(val) != '') {
			this.validateAndUpdate(this.validator, 'name');
		} else {					
			//context.updateContent(1)
		}
	}
}
class inputManager_school extends inputManager{
	constructor(input ,validateAndUpdate,validator ) {
		super(input ,validateAndUpdate,validator )
	}
	loop(val){
		if ($.trim(val) != '') {
			this.validateAndUpdate(this.validator, 'school');
		} else {					
			//context.updateContent(1)
		}
	}
}
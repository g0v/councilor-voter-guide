import { FB_ASSET } from "./fb_assets.js";
import { DATA } from './data.js';
import { InitStores, InitAddress } from "./address.js";
export {
	TextImageCombineManager,
};
/*
TextImageCombineManager
文字圖片合成 
 */
function TextImageCombineManager() {
	let curr = 1; //目前選取
	let result = '';
	let interval;
	const d = new DATA();
	const address = new InitAddress();
	const fb = new FB_ASSET();
	const announce = [{}, { id: 1, txt: '不靠虛假修飾，<br/>我用真實為自己打底。' }, { id: 2, txt: '自己的美，<br/>不需他人說嘴。' }, { id: 3, txt: '追求差異性，<br/>就是我的獨特性。' }, { id: 4, txt: '懂我的，就懂。<br/>不懂我的，我也沒空。' }, { id: 5, txt: '框架，<br/>是為沒個性的人設的。' }, { id: 6, txt: '沒有高顏值，<br/>至少為人真實。' }, { id: 7, txt: '過於保守，<br/>你也只能被牽著鼻子走。' }];
	const validator = new Validator($('.c3 .btn-items .custom-item input') );
	const inputmanager = new inputManager($('.c3 .btn-items .custom-item input'), chkFbInitial,validateAndUpdate, updateContent);
	
	function updateSelector() {
		$('.c3 .btn-items .btn-item').each(function() {
			let id = $(this).data('id');
			if (curr == id) {
				$(this).addClass('act')
				TweenMax.to($(this).find('.icov'), .5, { scaleX: 1, scaleY: 1, width: 22, ease: Expo.easeOut })
			} else {
				$(this).removeClass('act')
				TweenMax.to($(this).find('.icov'), .5, { scaleX: 0, scaleY: 0, width: 0, ease: Expo.easeOut })
			}
		})
	}
	/**/
	function updateContent(typ, parts) {
		const Seperator = '<br/>';
		curr = typ;
		if (typ <= 7) {
			$('.c2 .share-lg .Title').html(announce[typ].txt);
		} else {
			let str
			if (parts.length == 1) {
				str = parts[0]
			} else {
				str = parts[0] + Seperator + parts[1]
			}
			$('.c2 .share-lg .Title').html(str)
			curr = 8;
			result = str;
		}
		updateSelector();
	}
	/*
	
	 */
	function validateAndUpdate(){
		let result = validator.validate();
		if(result.tof){
			//console.log(break_words(val));
			this.updateContent(8, result.t ); 
		}
	}
	/* 檢查效度並更新*/
	function chkFbInitial() {
		if (fb.get_FBID() == '0') {
			fb.get_login(null);
			return false;
		}
		return true;
		console.log("fbid..." + fb.get_FBID());
	}

	function bind() {
		$('.c3 .btn-items .btn-item').click(function() {
			if (!chkFbInitial()) {
				return
			}

			let id = $(this).data('id');
			let ph = $('.c3 .btn-items .custom-item .placeholder')
			curr = id;
			$('.c3 .btn-items .custom-item input').val('');
			ph.html('自行創作（20字以內）');
			//updateSelector();
			updateContent(curr);
		})

		$('.c3 .btn-submit').click(function() {
				if (!chkFbInitial()) {
					return
				}
				if (curr == 8) {
					if (!validateAndUpdate()) {
						return; }
				} else {
					result = announce[curr].txt
				}
				let pid = carousel.getCurr();
				GLOBAL.CONTEXT = result;
				d.outpic(GLOBAL.pics[pid], result, cb);
				GLOBAL.ga.GT("share", ".btn.step2.choose" + pid);
				cy_action_conver('5558404', 'oirhrqqm', '53', '7');

				function cb(file) {
					console.log(file);
					GLOBAL.FILE = file;
					GLOBAL.FILEPATH = GLOBAL.api_root + 'uploads/' + file
						//update pop-share
					updateImg($('.pop-share .share-lg img'), GLOBAL.api_root + 'uploads/' + file)
					$('.pop-share').delay(200).fadeIn(500);
					TweenMax.fromTo($('.pop-share .content'), .5, { y: 100 }, { delay: .2, y: 0, ease: Back.easeOut })
				}
				//this.outpic = function( picid , context , cb){
			})
			/*.pop-share ui */
		let DOM = $('.pop-share'),
			FORM = $('.pop-form');
		DOM.find('.btn-close').click(
			function() {
				GLOBAL.ga.GT("share", ".btn.share.close");
				DOM.fadeOut(500)
			}
		)
		FORM.find('.btn-close').click(
			function() {
				GLOBAL.ga.GT("share", ".btn.step3.close");
				FORM.fadeOut(500)
			}
		)
		DOM.find('.btn-share').click(function() {
			GLOBAL.ga.GT("share", ".btn.share");
			fb.get_ui_post('【WASO ＃BeReal 做自己宣言】真實，才能與眾不同！', '美麗不用刻意，最真實即是最好的我。WASO肌膚的和食主義，用純粹，展現肌膚原始之美。搶先全球新上市！', GLOBAL.FILEPATH, 'https://waso.campaigns.com.tw/?fb=1', ['#BeReal'], afterPost)
		})
		FORM.find('.btn-submit').click(function() {

			if (d.checkStep1form()) {

				grecaptcha.execute();
			}
		})
		function afterPost() {
			DOM.fadeOut(500);
			FORM.delay(500).fadeIn(500);
			TweenMax.fromTo($('.pop-form .content'), .5, { y: 100 }, { delay: .5, y: 0, ease: Back.easeOut })
		}
		onSuccess = function(response) {
			console.log("end of recaptcha!...." + grecaptcha.getResponse());
			sendData(fb.get_FBID(), grecaptcha.getResponse(), GLOBAL.FILE, GLOBAL.CONTEXT, cb);
			GLOBAL.ga.GT("share", ".btn.step3.submit");

			function cb(typ) {
				if (typ == 're') {
					location.href = "share.html";
				} else
					location.href = "index.html";
			}
		};

		sendData = function(fbid, g_recaptcha_response, pic, context, cb) {
			var DOM = $('.pop-form');
			$('#loadingajax').fadeIn(400);
			var cName = DOM.find('#cname');
			var tel = DOM.find('#tel');
			var uCity = DOM.find('#zone1');
			var uArea = DOM.find('#zone2');
			var uAddr = DOM.find('#addr');

			$.post(`${GLOBAL.api_root}api/?mode=savedata`, {
					'fbid': fbid,
					'name': cName.val(),
					'tel': tel.val(),
					// email: email.val(),
					'addr': uCity.val() + uArea.val() + uAddr.val(),
					'pic': pic,
					'context': context,
					'g-recaptcha-response': g_recaptcha_response,
				},
				(pResponse) => {
					$('#loadingajax').fadeOut(400);
					if (pResponse.state == '1') {
						alert('成功送出');
						cb();
					} else {
						cb('re');
						alert('出現錯誤，請稍後再試！');
					}
				}, 'json');
		};
	}

	function init() {
		updateSelector();
		bind();
		
	}
	init();
}

class Validator {
	constructor(input ) {
		this.input = input || $('.c3 .btn-items .custom-item input');
	}	
	chk_input(str) {
			var state = 1;
			const MAX = 20;
			if (str.trim().length == 0) {
				state = '0';
			} else if (str.length > MAX) {
				state = '>';
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


/*
chkFunc:通常用來判斷是否已在FB登入狀態
validateAndUpdate: 檢查輸入文字/更新
updateContent :更新其他預設文字
 */
class inputManager {
	constructor(input, chkFunc ,validateAndUpdate, updateContent) {
		this.input = input;
		this.chkFunc = chkFunc;
		this.validateAndUpdate = validateAndUpdate;
		this.updateContent = updateContent;
		this.interval = {}
		this.ph = $('.c3 .btn-items .custom-item .placeholder');
		this.init();
	}
	init() {
		this.bind();
	}
	bind() {
		this.input.click(function() {
			if (!this.chkFunc()) {
				return
			}
			let val = this.input.val();
			let ph = this.ph
			ph.html('');
		}.bind(this))
		this.input.on('change keydown keyup', function() {
			if (!this.chkFunc()) {
				return
			}
			clearTimeout(this.interval);
			let val = this.input.val();
			const context = this;
			let ph = this.ph
			this.interval = setTimeout(function() {
				if (val != '') {
					ph.html('');
					context.validateAndUpdate();

				} else {
					ph.html('自行創作（20字以內）');
					context.updateContent(1)
				}
			}, 100);

		}.bind(this))
	}
}
/*
當斷點在pos時 
各段的文字長度
 */
function findpartsLength(parts, pos) {
	let l1 = 0,
		l2 = 0;
	for (let i in parts) {
		if (i <= pos) {
			l1 += parts[i].length;
		} else {
			l2 += parts[i].length;
		}
	}
	return { 1: l1, 2: l2 }
}
/*回傳分段後的字數*/
function iterateAllpos(parts) {
	const MAX = 10;
	for (var i in parts) {
		if (i < parts.length - 1) {
			let lengths = findpartsLength(parts, i)
			if (lengths[1] <= MAX && lengths[2] <= MAX) {
				return { breakable: true, pos: i }
			}
		}
	}
	return { breakable: false, pos: null }

}
/* 
	單行文字拆為兩段 
	Seperator: 最後用來隔開的符號
	brkMark   那些為可能需要拆分的符號

*/
function break_words(t) {
	const Seperator = '<br/>';
	const MAX = 11; //一行最多10
	const brkMark = ['　', ' ', ',', '，', "。"];
	let parts = t;

	for (let i in brkMark) {
		parts = parts.split(brkMark[i]).join(brkMark[i] + Seperator);
	}
	parts = parts.split(Seperator);
	let count = 0;

	parts = $.map(parts, function(element) {
		if (element.trim() == "") {
			return null;
		} else {
			return element;
		}
	});

	let newt = '';
	for (let i in parts) {
		newt += parts[i];
	}
	t = newt;

	//find break point;
	let break_res = iterateAllpos(parts);

	if (parts.length == 2 && parts[0].length <= MAX && parts[1].length <= MAX) {
		return parts;
	} else {

		//

		if (t.length <= MAX) {
			parts = [t];
			return parts;
		} else {
			if (break_res.breakable) {
				let pos = break_res.pos;
				let parts1 = '',
					parts2 = '';

				for (let i in parts) {
					if (i <= pos)
						parts1 += parts[i]
					else
						parts2 += parts[i]
				}

				return [parts1, parts2];


			} else {
				parts = [t.substr(0, MAX), t.substr(MAX, t.length)];
				return parts;
			}

		}

	}

}

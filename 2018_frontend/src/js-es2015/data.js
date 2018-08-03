// import './jq-global.js';
// //import TweenMax from "TweenMax";
// var $ = jQuery;

import {GLOBAL} from './config.js';
import {InitAddress} from './address.js';
export{DATA as DATA};
function DATA() {
	let sName;
	let nName;
	let uName;
	let tel;
	let stel;
	let email;
	let uCity;
	let uArea;
	let uAddr;
	function checkEmail(__email) {
		/* eslint max-len: ["error", 180] */
		/* eslint no-useless-escape: 0 */
		const EmailCheck = new RegExp(/^([a-zA-Z0-9]+)([\.\-\_]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.[a-zA-Z0-9\_\-]+)+$/);
		if (EmailCheck.test(__email)) {
			return true;
		}
		return false;
	}

	function ValidEmail(emailtoCheck) {
		const regExp = /^[^@^\s^,]+@[^\.@^\s^,]+(\.[^\.@^\s^,]+)+$/;
		if (emailtoCheck.match(regExp)) {
			return true;
		}
		return false;
	}
	
	this.init = function () {
		const d = new InitAddress();
		
	};
	this.chgPlaceholderBehavior=function() {
	    $('input').each(function() {
	        let ph = $(this).data('ph');
	        //console.log('ph:' + ph);
	        if(ph){
	        	if(typeof ph != 'undefined'){
	        		//$(this).attr("placeholder", ph).val("").focus().blur();
	        		$(this).focus(function(){
	        			$(this).attr("placeholder", "");
	        		})
	        		$(this).blur(function(){
	        			$(this).attr("placeholder", ph);
	        		})
	        	}
	        }
	        //.attr("placeholder", "Type a Location").val("").focus().blur();

	    })
	}
	this.checkStep1form = function () {
		
		const DOM = $('.form form');

		let cName = DOM.find('#cname');		
		let tel = DOM.find('#tel');		
		let uCity = DOM.find('#zone1');
		let uArea = DOM.find('#zone2');
		let uAddr = DOM.find('#addr');
		


		const testmail = /^.+@.+\..{2,3}$/;
		const word = /^[A-Za-z]+$/;
		const num = /^[0-9]+$/;
		const specialChars = /^[a-zA-Z0-9]+$/;
		const Chinese = /^[\u4e00-\u9fa5]+$/;
		const cellPhone = /^09[0-9]|{8|}+$/;
		let str = '';
		// CHECK DATA
			
			if (cName.val() === '') {
				str += '請填寫中文全名 !\n';
			} else if (!Chinese.test(cName.val())) {
				str += '請填寫中文全名 !\n';
			}
			
			if ($.trim(tel.val()) === '') {
				str += '請填寫電話號碼 !\n';
			} else if (tel.val().length < 8) {
				str += '請填寫完整電話號碼 !\n';
			} else if (isNaN(tel.val()) || !(cellPhone.test(tel.val()))  ) {
				str += '請以數字填寫電話號碼 !\n';
			}
				

			// if (email.val() === '') {
			// 	str += '請填寫電子信箱 !\n';
			// } else if (!checkEmail(email.val())) {
			// 	str += '電子信箱不正確 !\n';
			// }

			if (uCity.val() === '') {
				str += '請選擇 縣市 !\n';
			}
			if (uArea.val() === '') {
				str += '請選擇 區域 !\n';
			}
			if (uAddr.val() === '') {
				str += '請填入完整地址 !\n';
			}
			if (!document.getElementById('checkbox').checked) {
				str += '您尚未勾選同意個資法條款及活動辦法！\n';
			}
		// } else {
		// 	if (sName.val() === '') {
		// 		str += '請填入門市名稱 !\n';
		// 	}

		// 	if ($.trim(stel.val()) === '') {
		// 		str += '請填入門市電話號碼 !\n';
		// 	} else if (stel.val().length < 9) {
		// 		str += '請填入完整門市電話號碼 !\n';
		// 	} else if (isNaN(stel.val())) {
		// 		str += '請以數字填入門市電話號碼 !\n';
		// 	}

		// 	if (uCity.val() === '') {
		// 		str += '請選擇 縣市 !\n';
		// 	}
		// 	if (uArea.val() === '') {
		// 		str += '請選擇 區域 !\n';
		// 	}
		// 	if (uAddr.val() === '') {
		// 		str += '請填入完整地址 !\n';
		// 	}

		// 	if (uName.val() === '') {
		// 		str += '請填入中文全名 !\n';
		// 	} else if (!Chinese.test(uName.val())) {
		// 		str += '請以中文填入全名 !\n';
		// 	}

		// 	if ($.trim(tel.val()) === '') {
		// 		str += '請填入電話號碼 !\n';
		// 	} else if (tel.val().length < 9) {
		// 		str += '請填入完整電話號碼 !\n';
		// 	} else if (isNaN(tel.val())) {
		// 		str += '請以數字填入電話號碼 !\n';
		// 	}

		// 	if (email.val() === '') {
		// 		str += '請填入電子信箱 !\n';
		// 	} else if (!checkEmail(email.val())) {
		// 		str += '電子信箱 不正確 !\n';
		// 	}

		// 	if (!document.getElementById('readRule_sto').checked) {
		// 		str += '您尚未勾選同意個資法條款及活動辦法！\n';
		// 	}
		// }
		/* eslint consistent-return: 0 */
		if (str !== '') {
			alert(str);			
			return false;
		}
		return true;
		//sendData();
		//return true;
		// if(uName.val() == '') {
		//     str+='請填入中文全名 !\n';
		// }else if( !Chinese.test(uName.val())){
		//     str+='請以中文填入全名 !\n';
		// }
		// if($.trim(tel.val()) == '') {
		//     str+='請填入電話號碼 !\n';
		// }else if(tel.val().length < 9) {
		//     str+='請填入完整電話號碼 !\n';
		// }else if(isNaN(tel.val())) {
		//     str+='請以數字填入電話號碼 !\n';
		// }
		// if(email.val() == '') {
		//     str+='請填入電子信箱 !\n';
		// }else if(!checkEmail( email.val())) {
		//     str+='電子信箱 不正確 !\n';
		// }
		// if(uCity.val() == '') {
		//     str+='請選擇 縣市 !\n';
		// }if(uArea.val() == '') {
		//     str+='請選擇 區域 !\n';
		// }if(uAddr.val() == '' ) {
		//     str+='請填入完整地址 !\n';
		// }
		// if(!document.getElementById('readRule').checked) {
		//     str+='您尚未勾選同意個資法條款及活動辦法！\n';
		// }
		// if(!document.getElementById('readRule3').checked) {
		//     str+='您尚未勾選已確認資料無誤！\n';
		// }
		// set cookie
		// SetCookie('fbid' , _fb.get_FBID())
		// SetCookie('cne' , uName.val());
		// SetCookie('tel' , tel.val());
		// SetCookie('eml' , email.val());
		// SetCookie('addr3' , uAddr.val());
		// SetCookie('addr1' , uCity.val());
		// SetCookie('addr2' , uArea.val());
	};
	this.checkTrialform = function () {
		
		const DOM = $('.form form');

		var cName = DOM.find('#cname');
		
		var tel = DOM.find('#tel');
		
		//email = DOM.find('.email');
		var select2 = document.getElementById('select2');
		

		const testmail = /^.+@.+\..{2,3}$/;
		const word = /^[A-Za-z]+$/;
		const num = /^[0-9]+$/;
		const specialChars = /^[a-zA-Z0-9]+$/;
		const Chinese = /^[\u4e00-\u9fa5]+$/;
		const cellPhone = /^09[0-9]|{8|}+$/;
		let str = '';
		// CHECK DATA
		
			if (cName.val() === '') {
				str += '請填入中文全名 !\n';
			} else if (!Chinese.test(cName.val())) {
				str += '請以中文填入全名 !\n';
			}
			if ($.trim(tel.val()) === '') {
				str += '請填入手機號碼 !\n';
			} else if (tel.val().length < 9 ) {
				str += '請填入完整手機號碼 !\n';
			} else if (isNaN(tel.val()) || !(cellPhone.test(tel.val())) ) {
				str += '請以數字填入手機號碼 !\n';
			}
//			console.log('select2' + select2.value)
			if(!(select2.value>0)){
				str += '請選擇櫃點 !\n';
			}
			if (!document.getElementById('checkbox').checked) {
				str += '您尚未勾選同意個資法條款及活動辦法！\n';
			}
	
		if (str !== '') {
			alert(str);
			
			return false;
		}
		//sendData();
		return true;
	}
	this.checkResendform = function () {
		
		const DOM = $('.pop-resend form');
		var cname = DOM.find('#cname2');
		var tel = DOM.find('#tel2');
		var eml = DOM.find('#eml2');
		const testmail = /^.+@.+\..{2,3}$/;
		const word = /^[A-Za-z]+$/;
		const num = /^[0-9]+$/;
		const specialChars = /^[a-zA-Z0-9]+$/;
		const Chinese = /^[\u4e00-\u9fa5]+$/;
		const cellPhone = /^09[0-9]|{8|}+$/;
		let str = '';
			if (cname.val() === '') {
				str += '請填入中文全名 !\n';
			} else if (!Chinese.test(cname.val())) {
				str += '請以中文填入全名 !\n';
			}
			
			if ($.trim(tel.val()) === '') {
				str += '請填入手機號碼 !\n';
			} else if (tel.val().length < 9 ) {
				str += '請填入完整手機號碼 !\n';
			} else if (isNaN(tel.val()) || !(cellPhone.test(tel.val())) ) {
				str += '請以數字填入手機號碼 !\n';
			}
//			console.log('select2' + select2.value)
			if (eml.val() === '') {
				str += '請填入電子信箱 !\n';
			} else if (!checkEmail(eml.val())) {
				str += '電子信箱不正確 !\n';
			}
	
		if (str !== '') {
			alert(str);			
			return false;
		}
		//sendData();
		return true;
	}
	this.outpic = function( picid , context , cb){
		$('#loadingajax').show();
		$.post(`${GLOBAL.api_root}api/?mode=outpic`,
			{
				picid: picid,
				context: context,
			},
			(pResponse) => {
				$('#loadingajax').fadeOut(400);
				if (pResponse.state == 1) {
					cb(pResponse.data);
				} else {
					alert('出現錯誤，請稍後再試！');
				}
			}, 'json');
	}
	this.sendData = function ( opt={} , cb) {
		console.log('!@#!@#! send DATA....')
		$('#loadingajax').fadeIn(400);
		const DOM = $('.form form');
		var cName = DOM.find('#cname');		
		var tel = DOM.find('#tel');		
		let email = DOM.find('#email');
		let momage = DOM.find('#momageSelect');
		let product = DOM.find('#productSelect');
		let size =DOM.find("#sizeSelect")
		let babyname =DOM.find("#babyname")
		let babyagey = DOM.find('#babyage-y');
		let babyagem = DOM.find('#babyage-m');
		let message = DOM.find('#message');

		$.post(`${GLOBAL.api_root}savePhoto.php?nocache=${Math.floor(Math.random()*1000000)}`,
			{
				fbuid: opt.fbid ,
				fbname:opt.fbname,
				name: cName.val(),
				tel: tel.val(),
				email: email.val(),
				momage: momage.val(),
				product:product.val(),
				size:size.val(),
				babyname:babyname.val(),
				age:babyagey.val() + babyagem.val(),
				msg:message.val(),				
				photobase64: opt.pic1 ,
				fbbase64:opt.pics
				// pic:GLOBAL.resultP,
				// picid:GLOBAL.pid,
				// context:GLOBAL.context
			},
			(pResponse) => {
				$(".pop-ajax").hide();
				$('#loadingajax').fadeOut(400);
				if (pResponse.rs === 'ok') {
					//alert('成功送出');
					let id= pResponse.id ,purl = pResponse.photourl , fburl = pResponse.fburl;
					cb({id:id , purl :purl , fburl:fburl });
				} else {
					let msg;
					if(pResponse.errorcode == 'event_expired')
					msg = "活動已下線";
					else if(pResponse.errorcode == "existed")
					msg = "您已參加過本活動";
					else //if( pResponse.errorcode == "invalid_data")
					msg = "資料不完整";
					
					alert(msg);
				}
			}, 'json');
	}
	this.updatePhotoById = function ( opt={} , cb) {
		//console.log('!@#!@#! send DATA....')
		$('#loadingajax').fadeIn(400);
		

		$.post(`${GLOBAL.api_root}admin/updatePhoto.php?nocache=${Math.floor(Math.random()*1000000)}`,
			{
				id:opt.id,	
				photobase64: opt.pic1 ,
				fbbase64:opt.pics
				// pic:GLOBAL.resultP,
				// picid:GLOBAL.pid,
				// context:GLOBAL.context
			},
			(pResponse) => {
				$(".pop-ajax").hide();
				$('#loadingajax').fadeOut(400);
				if (pResponse.rs === 'ok') {
					alert('成功送出');
					let id= pResponse.id ,purl = pResponse.photourl , fburl = pResponse.fburl;
					
				} else {
					let msg;
					
					msg = "資料有誤";
					alert(msg);
				}
			}, 'json');
	}
	function clearForm() {
		// $('#q-text select[name= 'Product']').val(null);
		// $('#q-text input[name= 'Pserial']').val('');
		// $('#q-text input[name= 'Preceipt']').val('');
		// $('#q-text select[name= 'Store']').val(null);
		// $('#q-text input[name= 'Store_name']').val('');
		// $('#q-text input[name= 'Buydate']').val('');
		// $('#q-text input[name='uName']').val('');
		// $('#q-text input[name='tel']').val('');
		// $('#q-text input[name='email']').val('');
		// $('#zone1').val('');
		// $('#zone2').val('');
		// $('#q-text input[name='address']').val('');
		// $('#step1frm input[name='zipcode']').val('');
		// document.getElementById('readRule').checked = false;
		// document.getElementById('sendRule').checked = false;
	}
	
}

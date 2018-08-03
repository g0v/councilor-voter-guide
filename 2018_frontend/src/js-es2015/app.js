
import {LoadModle,getParameterByName,redirectHandle,checkVersion,redirectHandleFromMobile} from './common.js';
import {GLOBAL} from './config.js';
import {INDEX} from './pages/index.js';
import {RESUME} from './pages/resume.js';
import {COUNTY_MAYER_AREA} from './pages/county-mayer-area.js';
import {COUNTY_MAYER} from './pages/county-mayer.js';

import {COUNCILMEN_AREA} from './pages/councilmen_area.js';
import {COUNCILMEN_COUNTY} from './pages/councilmen_county.js';
import {COUNCILMEN} from './pages/councilmen.js';

import {BILL_AREA} from './pages/bill_area.js';
import {BILL_COUNTY} from './pages/bill_county.js';
import {BILL} from './pages/bill.js';
import {BALLOT} from './pages/ballot.js';
import {WISH_LIST} from './pages/wish-list.js';
import {WISH} from './pages/wish.js';
import {WISH_EDITOR} from './pages/wish-editor.js';
import {RESUME_BILLS} from './pages/resume-bills.js';


//import {COUNCILMEN_COUNTY} from './pages/councilmen_county.js';
//import {COUNCILMEN} from './pages/councilmen.js';

import {SEEMORE} from './pages/seemore.js';
import {SEEMORE_DETAIL} from './pages/seemore-detail.js';
import {DEFAULT} from './pages/default.js';
import {MENU} from './menu.js';
import {FB_ASSET} from './fb_assets.js';

var app = {};
function APP(){
	const requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame ||
	    function(callback) {
	        window.setTimeout(callback, 1000 / 60);
	    };
	window.requestAnimationFrame = requestAnimationFrame;

	function route() {
		let page = $('#page').val()
		switch(page){
			
			case 'index':
				new INDEX();
				return true;				
				break;
			case 'county-mayor-area':
				new COUNTY_MAYER_AREA();
				return true;
				break;
			case 'county-mayor':
				new COUNTY_MAYER();
				return true;
				break;
			case 'resume':
				new RESUME();
				return true;
				break;

			case 'councilmen-area':
				new COUNCILMEN_AREA();
				return true;
				break;
			case 'councilmen-county':
				new COUNCILMEN_COUNTY();
				return true;
				break;
			case 'councilmen':
				new COUNCILMEN();
				return true;
				break;
			case 'seemore':
				new SEEMORE();
				return true;
				break
			case 'seemore-detail':
				new SEEMORE_DETAIL();
				return true;
				break
			case 'bill-area':
				new BILL_AREA();
				return true;
				break
			case 'bill-county':
				new BILL_COUNTY();
				return true;
				break
			case 'bill':
				new BILL();
				return true;
				break
			case 'ballot':
				new BALLOT();
				return true;
				break
			case 'wish-list':
				new WISH_LIST();
				return true;
				break
			case 'wish':
				new WISH();
				return true;
				break
			case 'wish-editor':
				new WISH_EDITOR();
				return true;
				break
			case 'resume-bills':
				new RESUME_BILLS();
				return true;
				break
			default:
				new DEFAULT();
				return true;				
				break;
		}
		
	}
	
	function init() {
		new LoadModle($('body img') , ()=>{
			//GLOBAL.ga = new GA();
			app.menu = new MENU();
			let tof = route();
			if(tof){

				$('.loading img').fadeOut(500);
				$('.loading').delay(500).fadeOut(500);
			}
		});
	};
	init();
	console.log('app start.....')
}
app.start = new APP();

	




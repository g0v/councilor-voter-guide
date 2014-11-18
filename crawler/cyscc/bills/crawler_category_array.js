
var cheerio = require("cheerio");
var http = require("http");
var fs = require('fs');
var id = ["1", "3", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "52", "55", "56", "57", "58", "59", "60", "61", "62", "63", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "79", "80", "81", "82", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "96", "97", "98", "99", "100", "101", "102", "103", "104", "105", "106", "107", "109", "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "123", "125", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "173", "175", "176", "177", "178", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199", "200", "201", "202", "203", "204", "206", "207", "209", "210", "211", "212", "213", "214", "215", "216", "217", "218", "219", "220", "221", "222", "223", "225", "236", "238", "239", "240", "241", "242", "243", "244", "245", "246", "248", "250", "251", "253", "254", "255", "256", "257", "258", "259", "260", "261", "262", "263", "264", "265", "266", "267", "268", "269", "270", "271", "272", "273", "274", "275", "276", "277", "278", "281", "282", "283", "285", "286", "290", "291", "292", "293", "294", "295", "296", "297", "299", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "314", "315", "316", "317", "318", "319", "320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331", "332", "334", "335", "336", "337", "338", "339", "340", "341", "342", "343", "344", "345", "346", "347", "348", "349", "350", "351", "352", "353", "354", "355", "356", "357", "358", "359", "360", "361", "362", "363", "364", "365", "366", "367", "368", "369", "370", "371", "372", "373", "374", "375", "376", "377", "378", "379", "380", "381", "382", "383", "384", "385", "386", "387", "388", "389", "390", "392", "394", "395", "396", "397", "398", "400", "401", "402", "403"]
var link = []
var bill_no = []
var type = []
var category = []
var proposed_by = []
var petitioned_by = []
var abstract = []
var description = []
var method = []
var motion_a = []
var motion_b = []
 
var results = [];
 
var output = "test.json"
 
var outputStream = fs.createWriteStream(output);
 
// ================================================================================
 
function crawl (id) {
  
  var url = 'www.cyscc.gov.tw/chinese/Discussing_Detail.aspx?s=' + id;
  
  var options = {
    hostname: 'www.cyscc.gov.tw',
    port: 80,
    path: '/chinese/Discussing_Detail.aspx?s=' + id,
    method: 'GET',
    encoding: null
  };
  var req = http.request(options, function(res) {
  
    var data = '';
    
    var chunks = []
    res.setEncoding(null);
    res.on('data', function (chunk) {
        chunks.push(chunk);
    });
 
    res.on('end', function(){
      todo--;
      console.log('BODY: ' + url);
      
      var first = chunks[0];
      var data = first.concat(chunks.slice(1)).toString('utf8');
      
      var $ = cheerio.load(data);
      results.push({
        id : id,
        election_year : "2009",
        county : "嘉義縣",
        links : "http://www.cyscc.gov.tw/chinese/Discussing_Detail.aspx?s=" + id,
        bill_no : $('#ctl00_ContentPlaceHolder1_fvDetail_Label7').text(),
        type : $('#ctl00_ContentPlaceHolder1_fvDetail_Label2').text(),
        category : $('#ctl00_ContentPlaceHolder1_fvDetail_lbType').text()
          .replace(/[\r\n]+/g," ")
          .replace(/(?:縣長|副?議長|代理)/g, '')
          .replace(/(?:^\s+|\s+$)/g, "")
          .split(/[\.，、\s,]+/g),
        proposed_by : $('#ctl00_ContentPlaceHolder1_fvDetail_Label8').text()
          .replace(/[\r\n]+/g," ")
          .replace(/(?:縣長|副?議長|代理)/g, '')
          .replace(/(?:^\s+|\s+$)/g, "")
          .split(/[\.，、\s,]+/g),
        petitioned_by : $('#ctl00_ContentPlaceHolder1_fvDetail_lbParliamentary').text()
          .replace(/[\r\n]+/g," ")
          .replace(/(?:縣長|副?議長|代理)/g, '')
          .replace(/(?:^\s+|\s+$)/g, "")
          .split(/[\.，、\s,]+/g),
        "abstract" : $('#ctl00_ContentPlaceHolder1_fvDetail_lbCaseName').text().replace(/[\r\n\s]+/g," "),
        description :  $('#ctl00_ContentPlaceHolder1_fvDetail_lbContent').text().replace(/[\r\n\s]+/g," "),
        method : $('#ctl00_ContentPlaceHolder1_fvDetail_lbWay').text().replace(/[\r\n\s]+/g," "),
        motions : [
          {          
            "date":null,
            "motion":"審查意見", 
            "resolution": $('#ctl00_ContentPlaceHolder1_fvDetail_lbOpinion').text().replace(/[\r\n\s]+/g," ")
          },
          {          
            "date":null,
            "motion":"大會決議", 
            "resolution": $('#ctl00_ContentPlaceHolder1_fvDetail_lbResolution').text().replace(/[\r\n\s]+/g," ")
          }
        ]
     
      });
      check() 
    })
    
  });
 
  req.on('error', function(e) {
    console.log('problem with request: ' + e.message);
  });
  req.end();
}
 
function check() {
  console.log('todo : ' + todo)
  if (todo===0) {
    outputStream.write(JSON.stringify(results, null, 2));
  }
}
 
var todo = id.length;
 
for (var i = id.length - 1; i >= 0; i--) {
  crawl (id[i]);
}

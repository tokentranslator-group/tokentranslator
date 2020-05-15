console.log("log teditor.js");


//['jquery', 'jquery-ui-custom/jquery-ui'],
//
define(['require', 'jquery', 'jquery-ui-custom/jquery-ui', 
	
	"codemirror", "codemirror/mode/python/python",
        "codemirror/keymap/emacs",
	"codemirror/addon/edit/matchbrackets",
	"codemirror/addon/comment/comment",
	"codemirror/addon/dialog/dialog",
	"codemirror/addon/search/searchcursor",
	"codemirror/addon/search/search",
        ],
       function(require, $, ui, CodeMirror){

	   $ = require('jquery');
	   
	   
	   CodeMirror = require('codemirror');

	   function TEditor(div_storage_id, handler){
	       var self = this;

	       self.div_storage_id = div_storage_id;
	       self.div_code_id = "code";
	       self.handler = handler;
	   }


	   TEditor.prototype.make_editor = function(){
	       var self = this;

	       CodeMirror.commands.save = function() {
		   
		   var elt = editor.getWrapperElement();
		   elt.style.background = "#def";
		   setTimeout(function() { elt.style.background = ""; }, 300);
		   console.log("saved");
		   console.log(elt);
	       };
	       
	       var editor = CodeMirror.fromTextArea(document.getElementById(self.div_code_id), {
		   lineNumbers: true,
		   mode: {name: "python",
			  version: 3,
			  singleLineStringErrors: false},
		   matchBrackets: true,
		   keyMap: "emacs"
	       });
	       self.editor = editor;
	   };

	   TEditor.prototype.on_button_click = function(keys, row_data){
	       
	       var self = this;

	       var term_name = row_data[keys[0]];
	       var brackets = row_data[keys[1]];

	       // FOR get value:
	       self.editor.save();
	       console.log(self.editor.getTextArea().value);  
	       var code = self.editor.getTextArea().value;
	       // var code = self.editor.getOption("value");
	       
	       // console.log(code);
	       // END FOR

	       // console.log("from code_button.click: code.text1");
	       // console.log($("#code").text());
	       // console.log(document.getElementById("code").value);
	       
	       // FOR set replacer data from server:
	       
	       var to_send = JSON.stringify({
		   action: "set",
		   dialect_name: "cpp",
		   brackets: brackets,
		   term_name: term_name,
		   code: code
	       });
	       console.log("\n sending (from code_button)");
	       console.log(to_send);
	       
	       self.send_data_to_server(to_send, " no such term "+term_name);
	       // END FOR
	   };


	   TEditor.prototype.apply_controls = function(){
	   };


	   TEditor.prototype.set_default_value = function(default_value){
	       var self = this;
	       self.editor.setOption("value", default_value);
	   };


	   TEditor.prototype.load_term = function(keys, row_data){
	       var self = this;
	       var term_name = row_data[keys[0]];
	       var brackets = row_data[keys[1]];

	       var to_send = JSON.stringify({
		   action: "load",
		   dialect_name: "cpp",
		   term_name: term_name,
		   brackets: brackets
	       });
	       console.log("\n sending (from rowClick)");
	       console.log(to_send);
	       
	       // get replacer data from server:
	       self.send_data_to_server(to_send, " no such term "+term_name);
	   };

	   TEditor.prototype.remove_term = function(keys, row_data){
	       var self = this;
	       var term_name = row_data[keys[0]];
	       var brackets = row_data[keys[1]];


	       var to_send = JSON.stringify({
		   action: "remove",
		   dialect_name: "cpp",
		   term_name: term_name,
		   brackets: brackets
	       });

	       console.log("\n sending (from delete (save button))");
	       console.log(to_send);
	       
	       // remove term replacer data from server:
	       self.send_data_to_server(to_send, " error while removing term "+term_name);
	   };


	   TEditor.prototype.draw = function(){
	       var self = this;

	       var str = (('<div id="replacer_info">'
			   + '<p>replacer editor:</p>'
			   + '<div id="replacer_terms"></div>'
			   + '<input id="code_button" type="button" value="set" class="ui-button"><br>'
			   + '</div>')

			  + '<div id="replacer" class="style_replacer_static">'
			  + '<ul>'
			  + '<li><a href="#tif-0"> cpp </a></li>'
			  + '</ul>'
			  + '<div id="tif-0" style="background: #CCCCCC;">'
			  + '<textarea id="'+self.div_code_id+'" name="code" class="frame_codemirror"></textarea>'
			  + '</div>'
			  + '</div>');
	       $("#"+ self.div_storage_id).html(str);
	       $("#replacer").tabs();

	   };


	   TEditor.prototype.remove = function(){
	       var self = this;
	       console.log("replacer");
	       console.log($("#replacer"));
	       if($("#replacer").length){
		   // console.log(self);
		   // console.log(self.editor);
		   self.editor.toTextArea();
		   console.log("codemirror.toTextArea done");
		   $("#replacer").remove();
		   $("#replacer_info").remove();
	       }
	   };
	   

	   TEditor.prototype.send_data_to_server = function(to_send, error_msg){
	       var self = this;
	       $.ajax(
		   {
		       url: self.handler, //  'api/tables/replacer',
		       method: 'POST',
		       data: to_send,
		       
		       success: function (jsonResponse) {
			   console.log("from replacer get success:");
			   
			   var objresponse = JSON.parse(jsonResponse);
			   var data = objresponse;
			   // console.log(data["source"]);
			   
			   // set value
			   self.editor.setOption("value", data["source"]);
			   // console.log(data);
			   console.log("available_terms:");
			   console.log(data["available_terms"]);
			   $("#replacer_terms").text(data["available_terms"]);
		       },
		       
		       error: function () {
			   //$("#responsefield").text("Error to load api");
			   console.log("Error to load api");							   				
			   // set value
			   self.editor.setOption("value",
						 "#"+error_msg);
		       }
		   }
	       );
	       
	   };


	   return {
	       TEditor: TEditor	 
	   };
	   
       });

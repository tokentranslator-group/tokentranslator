console.log("log editor_signatures.js");


define(['jquery', 'modules/teditor'],
       function($, teditor){

	   function SEditor(div_storage_id, handler){
	       teditor.TEditor.call(this, div_storage_id, handler);
	       
	   };

	   // inheritance:
	   SEditor.prototype = Object.create(teditor.TEditor.prototype);
	   Object.defineProperty(SEditor.prototype, 'constructor',
				{value: SEditor, enumerable: false, writable:true});

	   
	   SEditor.prototype.on_button_click = function(keys, row_data){
	       var self = this;
	       var predicate = row_data[keys[0]];
	       var signature = row_data[keys[1]];

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
		   predicate: predicate,
		   signature: signature,
		   code: code
	       });
	       console.log("\n sending (from code_button)");
	       console.log(to_send);
	       
	       self.send_data_to_server(to_send, " no such term "+"("+predicate+", "+signature+")");
	       // END FOR
	   };


	   SEditor.prototype.load_term = function(keys, row_data){
	       var self = this;
	       var predicate = row_data[keys[0]];
	       var signature = row_data[keys[1]];

	       var to_send = JSON.stringify({
		   action: "load",
		   dialect_name: "cpp",
		   predicate: predicate,
		   signature: signature
	       });
	       console.log("\n sending (from rowClick)");
	       console.log(to_send);
	       
	       // get replacer data from server:
	       self.send_data_to_server(to_send, " no such term "+"("+predicate+", "+signature+")");
	   };

	   SEditor.prototype.remove_term = function(keys, row_data){
	       var self = this;
	       var predicate = row_data[keys[0]];
	       var signature = row_data[keys[1]];

	       var to_send = JSON.stringify({
		   action: "remove",
		   dialect_name: "cpp",

		   predicate: predicate,
		   signature: signature
	       });

	       console.log("\n sending (from delete (save button))");
	       console.log(to_send);
	       
	       // remove term replacer data from server:
	       self.send_data_to_server(to_send, " error while removing term "+"("+predicate+", "+signature+")");
	   };


	   return {
	       SEditor: SEditor
	   };
       });


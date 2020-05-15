console.log("log editor_tags.js");

define(['jquery', 'ttabs'],
       function($, ttabs){

	   function TabsEditor(div_storage_id, handler){
	       var self = this;

	       // default entry key:
	       self.key = undefined;

	       this.tabs = new ttabs.Tabs({
		   div_id: div_storage_id,
		   subdiv_id_name: "dbtabs",
		   header: "selected entry data:",

		   tabs_ids: ["parser", "out"],
		   tabs_contents: ["2+2", "4"],

		   buttons_names: ["save", "refresh"],
		   tabs_buttons_callbacks: 
		   [
		       function(tab_id, tab_content_text_id){
			   return(function(event){
			       console.log("clicked at first button");
			       console.log("clicked at element:");
			       console.log(tab_id);
			       var text = $("#"+tab_content_text_id).text();
			       console.log("default button clicked:");
			       console.log(text);
			       console.log(tab_content_text_id);
			       var to_send = {
				   action: "save",
				   id: self.key,
				   tabs_ids: self.tabs.data["tabs_ids"],
				   tabs_contents: self.tabs.data["tabs_contents"]
			       };

			       console.log("\n sending (from save button callback):");
			       console.log(to_send);
			       
			       var succ = function(data){
				   self.tabs.load(data);
			       };
			       
			       // get replacer data from server:
			       self.send_data(to_send, succ);	       

			       /*
				// var math = document.getElementById(to_parse_div_id);
				MathJax.Hub.Queue(["Typeset", MathJax.Hub, to_parse_div_id]);
				*/
			   });},

		       function(tab_id, tab_content_text_id){
			   return(function(event){
			       console.log("clicked at second button");
			       console.log("clicked at element:");
			       console.log(tab_id);
			       var text = $("#"+tab_content_text_id).text();
			       console.log("default button clicked:");
			       console.log(text);
			       console.log(tab_content_text_id);
			       var to_send = {
				   action: "load",
				   id: self.key
			       };

			       console.log("\n sending (from refresh button callback):");
			       console.log(to_send);
			       
			       var succ = function(data){
				   self.tabs.load(data);
			       };
			       
			       // get replacer data from server:
			       self.send_data(to_send, succ);

			       /*
				// var math = document.getElementById(to_parse_div_id);
				MathJax.Hub.Queue(["Typeset", MathJax.Hub, to_parse_div_id]);
				*/
			   });}
		   ]
	       });
	       this.handler = handler;
	       this.default_value = "None";
	   };


	   TabsEditor.prototype.set_table_name = function(table_name){
	       var self = this;
	       self.table_name = table_name;
	   };


	   TabsEditor.prototype.on_button_click = function(keys, row_data){
	       var self = this;
	       var key0= row_data[keys[0]];

	       self.key = key0;
	   };


	   TabsEditor.prototype.load_term = function(keys, row_data){
	       var self = this;
	       var key0= row_data[keys[0]];
	       self.key = key0;
	       var to_send = {
		   action: "load",
		   id: key0
	       };
	       console.log("\n sending (from TabsEdiotr.load_term)");
	       console.log(to_send);
	       
	       var succ = function(data){
		   self.tabs.load(data);
	       };
	       
	       // get replacer data from server:
	       self.send_data(to_send, succ);
	   };

	   TabsEditor.prototype.remove = function(){
	       var self = this;
	       console.log("from TabsEditor.remove");
	       self.tabs.remove();
	   };

	   TabsEditor.prototype.draw = function(){
	       var self = this;
	       console.log("from TabsEditor.draw");

	       // init tabs:
	       var data = {
		   tabs_ids: ["info"],
		   tabs_contents: [self.default_value]
	       };
	       self.tabs.load(data);
	   };

	   TabsEditor.prototype.make_editor = function(){
	       console.log("from TabsEditor.make_editor");
	   };

	   TabsEditor.prototype.set_default_value = function(default_value){
	       var self = this;
	       console.log("from TabsEditor.set_default_value");
	       self.default_value = default_value;
	   };

	   TabsEditor.prototype.remove_term = function(keys, row_data){
	       var self = this;
	       /*
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
		*/
	   };


	   TabsEditor.prototype.send_data = function(to_send, succ){

	       /*
		-- ``succ`` - if given, will be called after success
		with data as arg.
		*/
	       var self = this;
	       to_send["table_name"] = self.table_name;
	       console.log("send_data to_send:");
	       console.log(to_send);
	       $.ajax(
		   {
		       url: this.handler,
		       type: 'POST',
		       data: JSON.stringify(to_send),
			   
		       success: function (jsonResponse) {
			   var objresponse = JSON.parse(jsonResponse);
			   
			   var data = objresponse;
			   console.log("\ndata_successfuly_recived:");
			   console.log(data);
			   // to_send["result"] = data;
			   if (succ)
			       succ(data);
		       },

		       error: function (data) {
			   console.log("error to send");
			   console.log(data);
		       }
		   });
	       
	   };
	   

	   return {
	       TabsEditor: TabsEditor
	   };
       });


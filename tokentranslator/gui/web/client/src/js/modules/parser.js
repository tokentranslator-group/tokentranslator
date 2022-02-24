console.log("log parser.js");


define(['jquery', 'modules/parser_base', 'modules/tnet',
	'modules/tnet_tabs', 'modules/parser_params_tabs'],
       function($, parser_base, tnet, tnet_tabs, params_tabs){

	   function TParser(net, dialect){
      	       /*
		Create to_parse_div editable div for
		writing sent to parse.
		Call NetHandlerParsing at server side.
		Get lex step result to lex_out_div.
		Get net step result.
		*/
 	       var self = this;
	       self.gnet = net;
	       self.dialect = dialect;

	       self.storage_id = "div_scene";

	       self.frame_cy_div_id = "frame_cy";
	       
	       // for save entry for table
	       self.entry = {};

	       // name where parser will be drawn:
	       self.parser_storage_div_id = "parser_div";

	       /*
	       var default_input;
	       var input_default_contents = [];
	       var input_button_callback;
	       
	       if(self.dialect=="eqs"){
		   default_input = self.default_input_eqs || "U'=a*(D[U,{x,2}]+ D[U,{y,2}])";
		   input_default_contents.push(default_input);

		   input_button_callback = self.get_button_parse_callback_eqs;
		   // fix array objects this bug:
		   // input_buttons_callbacks.push(self.get_button_parse_callback_eqs.bind(self));
	       };

	       if(self.dialect=="cs"){
		   default_input = self.default_input_cs || "abelian(G) \\and subgroup(H, G,) => abelian(H)";
		   input_default_contents.push(default_input);

		   input_button_callback = self.get_button_parse_callback_cs;
		   // fix array objects this bug:
		   // input_buttons_callbacks.push(self.get_button_parse_callback_cs.bind(self));
	       }

	       this.tabs = new ttabs.Tabs({
		   div_id: self.parser_storage_div_id,
		   subdiv_id_name: "parser",
		   header: "output data:",

		   tabs_ids: [self.dialect],
		   tabs_contents: input_default_contents,

		   buttons_names: ["parse", "save", "refresh"],
		   tabs_buttons_callbacks: 
		   [
		       function(tab_id, tab_content_text_id){
			   return(function(event){
			       console.log("clicked at first button");
			       console.log("clicked at element:");
			       console.log(tab_id);
			       
			       input_button_callback(tab_content_text_id);
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

			       /
				// var math = document.getElementById(to_parse_div_id);
				MathJax.Hub.Queue(["Typeset", MathJax.Hub, to_parse_div_id]);
				/
			   });},

		       function(tab_id, tab_content_text_id){
			   return(function(event){
		
			       console.log("clicked at third button");
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

			       /
				// var math = document.getElementById(to_parse_div_id);
				MathJax.Hub.Queue(["Typeset", MathJax.Hub, to_parse_div_id]);
				/
			   });}
		   ]
	       });
	       */
	       self.pbase = new parser_base.ParserBase(self, self.parser_storage_div_id, "parser");
	       self.net = new tnet.Net(self.frame_cy_div_id);
	       
	       if(["eqs", "cs"].indexOf(dialect) < 0){
		   var msg = ('dialect "'+dialect+'" not supported.'
			      + ' Supported dialect names is: "eqs", "cs"');
		   alert(msg);
		   throw new Error(msg);
	       };
	   };

	   TParser.prototype.set_default_input_eqs = function(value){
	       var self = this;
	       self.default_input_eqs = value;
	   };


	   TParser.prototype.set_default_input_cs = function(value){
	       var self = this;
	       self.default_input_cs = value;
	   };

	   
	   TParser.prototype.remove = function(){
	       var self = this;
	       self.net.remove_net();
	       
	       // self.tabs.remove();

	       $("#frame_scene").remove();
	       $("#div_buttons").remove();
	       $("#frame_before_parser").remove();
	       $("#frame_parser").remove();
	       $("#"+self.frame_cy_div_id).remove();
	       $("#frame_after_parser").remove();
	       // $("#"+self.storage_id).remove();
	       
	   };

	   TParser.prototype.init_board = function(){
	       /*
		- ``dialect`` -- either "eqs" or "cs"
		*/
	       
	       var self = this;
	       console.log("self out out", self);

	       self.draw();

	       $("#frame_parser").css("top","20px");
	       // ui-widget ui-widget-content 
	       //	  + "Let(G: group(G) in: abelian(G)=>commutative(G),"
	       //	   + " commutative(G)=>abelian(G),)"

	       params_tabs.create_parser("#frame_before_parser");

	       // FOR input tabs:
	       var input_names = [self.dialect];
	       // var input_names = ["eqs", "cs_0"];
	       var input_default_contents = [];
	       var default_input;
	       if(self.dialect=="eqs"){
		   default_input = self.default_input_eqs || "U'=a*(D[U,{x,2}]+ D[U,{y,2}])";
		   input_default_contents.push(default_input);
	       };
	       if(self.dialect=="cs"){
		   default_input = self.default_input_cs || "abelian(G) \\and subgroup(H, G,) => abelian(H)";
		   input_default_contents.push(default_input);
	       };
	       // var input_default_contents = ["U'=a*(D[U,{x,2}]+ D[U,{y,2}])",
	       //  			        "abelian(G) \\and subgroup(H, G,) => abelian(H)"];
	       var input_buttons_callbacks = [];
	       if(self.dialect=="eqs"){ 
		   // fix array objects this bug:
		   input_buttons_callbacks.push(self.get_button_parse_callback_eqs.bind(self));
	       };
	       if(self.dialect=="cs"){
		   // fix array objects this bug:
		   input_buttons_callbacks.push(self.get_button_parse_callback_cs.bind(self));
	       };
	       // var input_buttons_callbacks = [self.get_button_parse_callback_eqs,
	       //			      self.get_button_parse_callback_cs];
	       
	       /*
	       var default_input;
	       if(self.dialect=="eqs"){
		   default_input = self.default_input_eqs || "U'=a*(D[U,{x,2}]+ D[U,{y,2}])";
	       };

	       if(self.dialect=="cs"){
		   default_input = self.default_input_cs || "abelian(G) \\and subgroup(H, G,) => abelian(H)";
	       }
	       
	       self.tabs.load({
		   tabs_ids: [self.dialect],
		   tabs_contents: [default_input]
	       });*/
	       self.pbase.create_input_field(input_names, input_default_contents,
	        			     input_buttons_callbacks, self.save_entry.bind(self));
	       // END FOR
	   };


	   TParser.prototype.draw = function(){
	       var self = this;

	       var str = 
		   `<div id="frame_scene">
		      <div id="div_parser_scene"></div>
		   </div>

		   <div id="div_buttons" class="above_net_left">
	           </div>

		   <div id="frame_before_parser">
		   </div>

		   <div id="frame_parser" class="above_net_left" top>
		      <div id="`+self.parser_storage_div_id+`">
		      </div>
		   </div>

		   <div id="`+self.frame_cy_div_id+`" ></div>
		   

		   <div id="frame_after_parser">
		   </div>`;

	       $("#"+self.storage_id).html(str);
	   };


	   TParser.prototype.save_entry = function(){

	       /*Save entry for table.
		TODO: unite with parser_base/ttabs.*/

	       var self = this;
	       console.log("save_entry");
	       console.log("self:");
	       console.log(self);
	       console.log("self.entry:");
	       console.log(self.entry);
	       
	       console.log("self.gnet.boards:");
	       console.log(self.gnet.boards["tables_db_eqs"]);
	       if(self.dialect=="eqs"){
		   if (!("input" in self.entry & "sympy" in self.entry)){
		       var msg = ('entry["input"] or entry["sympy"] is undefined.'
				  + '\n use parse first');
		       alert(msg);
		       throw new Error(msg);
		   };
	       
		   self.gnet.boards["tables_db_eqs"].save_entry(self.entry);
	       }
	       if(self.dialect=="cs"){
		   if (!("input" in self.entry)){
		       var msg = ('entry["input"] is undefined.'
				  + '\n use parse first');
		       alert(msg);
		       throw new Error(msg);
		   };
	       
		   self.gnet.boards["tables_db_cs"].save_entry(self.entry);
	       }
	       self.entry = {}
	   };


	   TParser.prototype.get_button_parse_callback_eqs = function(to_parse_div_id){
	       var self = this;
	       console.log("self out", this);
	       return(function(event){
		   var text = $(to_parse_div_id).text();
		   var params = {};

		   params["dim"] = $("#param_dim").val();
		   params["blockNumber"] = $("#param_bn").val();
		   params["vars_idxs"] = $("#param_vidxs").val();
		   params["coeffs"] = $("#param_coeffs").val();
		   params["diffType"] = "pure";
		   params["diffMethod"] = $("#param_dm").val();
		   params["btype"] = $("#param_btype").val();
		   params["side"] = $("#param_side").val();
		   params["vertex_sides"] = $("#param_sn").val();
		   params["func"] = $("#param_func").val();
		   params["firstIndex"] = $("#param_fi").val();
		   params["secondIndexSTR"] = $("#param_si").val();
		   params["shape"] = $("#param_shape").val();
		   console.log("text for parsing:");
		   console.log(text);
		   console.log("params for parsing:");
		   console.log(params);
		   console.log("self in ", self);
		   self.parse("eqs", text, params);
		   
		   // self.parse("eqs", text, params);
	       });
	   };


	   TParser.prototype.get_button_parse_callback_cs = function(to_parse_div_id){
	       var self = this;
	       return(function(event){
		   var text = $(to_parse_div_id).text();

		   var params = {};   
		   self.parse("cs", text, params);
		   // self.parse("eqs", text, params);
	       });
	   };

	   
	   TParser.prototype.parse = function(dialect, text, params){
		       
	       /*parse text with dialect parser
		and print parsed cytoscape net
		and set result to "#frame_after_parser"
		result will be: lex out, cpp/sympy out
		vars, slambda out*/
	       var self = this;

	       // FOR sending data to server:
	       if(text.length){
		   var to_send = JSON.stringify({dialect: dialect,
						 text: text,
						 params: params});
		   // var to_send = data_to_send;
		   console.log("\n sending");
		   console.log(to_send);
		   
		   $.ajax(
		       {
			   url: 'api/net_parsing',
			   type: 'POST',
			   data: to_send,
			   
			   success: function (jsonResponse) {
			       var objresponse = JSON.parse(jsonResponse);
			       data_lex = objresponse['lex'];
			       data_net = objresponse['net'];
			       data_vars = objresponse["vars"];
			       data_output_cpp = objresponse["eq_cpp"];
			       data_output_sympy = objresponse["eq_sympy"];
			       data_output_slambda = objresponse["slambda"];

			       console.log("\ndata_lex");
			       console.log(data_lex);
			       console.log("\ndata_net");
			       console.log(data_net);
			       console.log("\ndata_vars");
			       console.log(data_vars);
			       console.log("\ndata_output_cpp");
			       console.log(data_output_cpp);
			       console.log("\ndata_output_sympy");
			       console.log(data_output_sympy);
			       console.log("\ndata_output_slambda");
			       console.log(data_output_slambda);

			       // FOR save entry for table:
			       // "input" here because it used as identifier
			       // and must be defined last:
			       self.entry["input"] = text;
			       // self.entry["input"] = objresponse["text"];

			       if(self.dialect=="eqs"){
				   self.entry["net"] = JSON.stringify(data_net);
				   self.entry["cpp"] = data_output_cpp;
				   self.entry["sympy"] = data_output_sympy;
				   self.entry["vars"] = data_vars;
			       }
			       
			       if(self.dialect=="cs"){
				   self.entry["net"] = JSON.stringify(data_net);
				   self.entry["vars"] = data_vars;
			       }
			       // END FOR

			       $("#lex_out_div").text(data_lex);
			       self.net.create_net(data_net);

			       // FOR create tabs:
			       tnet_tabs.create_tabs("#frame_after_parser", data_vars,
						     data_output_cpp, data_output_sympy,
						     data_output_slambda);
			       // END FOR

			       // copy data:
			       // var data_local = data.slice();
			       // $("#div_editor").text(data[0].kernel);
			   },
			   
			   error: function (data) {
			       console.log("error to send");
			       console.log(data.responseText);

			       var msg = ("parse error:\n\n responseText: \n"
					  + data.responseText);
			       alert(msg);
			       throw new Error(msg);

			   }
		       });
	       }
	       else{
		   console.log("\n nothing to send");
	       };
	   };
	   
	   return {
	       Parser: TParser
	   };
       });

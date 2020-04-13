console.log("log parser.js");


define(['jquery', 'modules/parser_base', 'modules/tnet',
	'modules/tnet_tabs', 'modules/parser_params_tabs'],
       function($, parser_base, tnet, tnet_tabs, params_tabs){

	   function TParser(dialect){
      	       /*
		Create to_parse_div editable div for
		writing sent to parse.
		Call NetHandlerParsing at server side.
		Get lex step result to lex_out_div.
		Get net step result.
		*/
 	       var self = this;
	       self.pbase = new parser_base.ParserBase();
	       self.net = new tnet.Net();
	       
	       if(["eqs", "cs"].indexOf(dialect) < 0){
		   var msg = ('dialect "'+dialect+'" not supported.'
			      + ' Supported dialect names is: "eqs", "cs"');
		   alert(msg);
		   throw new Error(msg);
	       };
	       self.dialect = dialect;

	       // name where parser will be drawn:
	       self.parser_storage_id = "parser_div";
	   };

	   
	   TParser.prototype.remove = function(){
	       self.net.remove_net();
	       $("#"+self.parser_storage_id).remove();
	       
	   };

	   TParser.prototype.init_board = function(){
	       /*
		- ``dialect`` -- either "eqs" or "cs"
		*/

	       var self = this;
	       console.log("self out out", self);

	       $("#frame_parser").css("top","20px");
	       // ui-widget ui-widget-content 
	       //	  + "Let(G: group(G) in: abelian(G)=>commutative(G),"
	       //	   + " commutative(G)=>abelian(G),)"

	       params_tabs.create_parser("#frame_before_parser");

	       // FOR input tabs:
	       
	       
	       var input_names = [self.dialect];
	       // var input_names = ["eqs", "cs_0"];
	       var input_default_contents = [];
	       if(self.dialect=="eqs"){
		   input_default_contents.push("U'=a*(D[U,{x,2}]+ D[U,{y,2}])");
	       };
	       if(self.dialect=="cs"){
		   input_default_contents.push("abelian(G) \\and subgroup(H, G,) => abelian(H)");
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
	       self.pbase.create_input_field("#"+self.parser_storage_id, "parser",
					     input_names, input_default_contents,
					     input_buttons_callbacks);
	       // END FOR
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
			       console.log(data);
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

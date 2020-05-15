console.log("log parser_base.js");


define(['jquery'],
       function($){
	   function ParserBase(net, storage_div_id, subdiv_id_name){
	       /*
		 
		 - ``div_id`` -- id for div, which be used.
		 
		 - ``subdiv_id_name`` -- name for sub id's, which be used.
		 
		*/

	       var self = this;
	       self.net = net;
	       self.storage_div_id = storage_div_id;
	       self.subdiv_id_name = subdiv_id_name;
	   };


	   ParserBase.prototype.create_input_field = function(
	       input_names, input_default_contents,
	       input_buttons_callbacks, save_entry_func){
	       /*
		 Create editable field tab for each input in ``input_names``
		 All ``input_names``, ``input_default_content``,
		 ``input_buttons_callbacks`` must have some length.
		 
		 - ``input_names`` -- list with names for each tab.
		 (ex: ["lex", "cs_0"])
		 
		 - ``input_default_contents`` -- default content of each field.
		 (ex: ["U'=a*(D[U,{x,2}]+ D[U,{y,2}])",
		 "abelian(G) \\and subgroup(H, G,) => abelian(H)"])
		 
		 - ``input_buttons_callbacks`` -- callbacks for buttons.
		 
		 Fields:
		 
		 "to_"+self.subdiv_id_name+"_div_"+ elm -- is name of div, where text will
		 be rendered.
		 
		 "edit_"+ self.subdiv_id_name +"_input" -- is name of div, where dialog
		 will be created.
		 
		 "epi_editor" -- div inside dialog, where content will be edit by user
		 
	       */
	       var self = this;

	       var board_str = 
		   ('<p class="ui-widget-header">header</p>'
		    + '<div id="tabs_input">'
		    + '<ul>');
		   
	       $.each(input_names,
		      function(elm, id){
			  board_str += ('<li><a href="#tif-'
					+ elm
					+ '">'+id+'</a></li>');});
	       board_str += '</ul>';
		       
	       $.each(input_names,
		      function(elm, id){
			  board_str += ('<div id="tif-'
					+ elm
					+ '"></div>'
				       );});
	       
	       board_str +=
	       ('</div>'
		+ '<div id="lex_out_div" class="style_editor_static"'
		+ ' title="lex out"> </div>'+'<br>'
		+ '<div id="edit_'+ self.subdiv_id_name +'_input" class="">'
		+ '<div id="epi_editor" contenteditable="true"'
		+ ' class=""></div>'
		+'</div>');
	       $("#"+self.storage_div_id).html(board_str);
	       $("#"+self.storage_div_id).addClass("above_net_left");
	       
	       $.each(input_default_contents,
		      function(elm, id){
			  var str_input =
			      ('<div id="to_'+self.subdiv_id_name
			       +'_div_'+ elm +'" title="click to edit"'
			       + ' class="style_editor_static ">'
			       + id
			       + '</div>'
			       + '<br>'
			       + '<input id="button_'+self.subdiv_id_name+ '_'+elm+'" type="button"'
			       + ' value="'+self.subdiv_id_name+'" class="ui-button">'
			       + '<input id="button_'+self.subdiv_id_name+ '_'+elm+'_save'+'" type="button"'
			       + ' value="'+'save'+'" class="ui-button"><br>'
			       +'<br>');
			  $("#tif-"+elm).html(str_input);
			  $("#to_"+self.subdiv_id_name+"_div_"+elm).tooltip();
		      });
	       
	       $("#tabs_input").tabs();
	       $("#"+self.storage_div_id).draggable({handle: "p.ui-widget-header"});
	       /// $("#to_parse_div").css("width", "350");
	       /// $("#to_parse_div").css("height", "50");
	       
	       $.each(input_default_contents,
		      function(elm, id){
			  // for editor:
			  var edit_id = "#to_"+self.subdiv_id_name+"_div_"+elm;
			  $(edit_id).on("click",
					self.get_to_parse_div_callback(self.subdiv_id_name,
								       edit_id));
			  // for parse button:
			  var but_id = "#button_"+self.subdiv_id_name+"_"+elm;
			  $(but_id).on("click",
				       input_buttons_callbacks[elm](edit_id));
			  
			  // for save entry button:
			  var but_save_id = "#button_"+self.subdiv_id_name+"_"+elm+"_save";
			  $(but_save_id).on("click", function(event){
			      save_entry_func();
			  });
		      });
	       // END FOR
	   };


	   ParserBase.prototype.get_to_parse_div_callback = function(subdiv_name, to_parse_div_id){

	       /* for input editor
		  (with contenteditable="true" attribute)
		  with use of jquery.dialog.
	       */
	       var self = this;

	       return(function(event){
		   // create dialog
		   console.log("create dialog");
		   console.log("dialog created");
		   var subdiv_id = "#edit_" + subdiv_name + "_input";
		   $(subdiv_id).dialog({
		       resizable: true,
		       height: "auto",
		       width: 400,
		       modal: true,
		       open: function(event, ui){
			   console.log("dialog opend");
			   $(subdiv_id).toggleClass("ui-widget ui-corner-all ui-widget-shadow style_editor_dinamic");
			   $("#epi_editor").toggleClass("ui-widget-content ui-corner-all");
			   
		       },
		       close: function(event, ui){
			   console.log("dialog closed");
			   $(subdiv_id).toggleClass("ui-widget ui-corner-all ui-widget-shadow style_editor_dinamic");
			   $("#epi_editor").toggleClass("ui-widget-content ui-corner-all");
			   
		       },
		       buttons: {
			   "Edit": function() {
			       console.log("dialog text");
			       var text = $("#epi_editor").text();
			       console.log(text);
			       $(to_parse_div_id).text(text);
			       // FOR save entry for table:
			       self.net.entry = {}
			       // END FOR
			       // $("#to_parse_div").text(text);
			       $( this ).dialog( "close" );
			   },
			   Cancel: function() {
			       $( this ).dialog( "close" );
			   }
		       }
		   });
		   // $("#to_parse_div").toggleClass("ui-widget ui-corner-all ui-widget-shadow");
		   // $("#epi_editor").toggleClass("ui-widget-content ui-corner-all");
		   
		   $("#epi_editor").text($(to_parse_div_id).text());
		   console.log("dialog created");
	       });
	   };
	   

	   return {
	       ParserBase: ParserBase
	   }});

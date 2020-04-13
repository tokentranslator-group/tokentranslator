console.log("log tpath.js");


define(['jquery'],
       function($){
	   function Path(path_id, path_storage_id, dialect){
	       var self = this;
	       
	       self.path_id = path_id;
	       self.path_storage_id = path_storage_id;

	       self.dialect = dialect;

	       // for selection with menu:
	       self.selected = null;

	   };

	   Path.prototype.remove = function(){
	       var self = this;
	       $("#"+self.path_id).remove();
	   };

	   Path.prototype.make_path = function(){
	       var self = this;
	       
	       var str = (
		   '<h4>path to "'+self.dialect+'" dialect db:</h4>'
		       + '<div id="'+ self.path_id + '">'
		       + '<ul id="path_dialects">'
		       + '<li><a href="#path_'+self.dialect+' dialect ">'+self.dialect+'</a></li>'
		       // + '<li><a href="#path_cs">cs</a></li>'
		       + '</ul>'
		       + ('<div id="path_'+self.dialect+'">'			       
			  + '<h5>current path for "'+self.dialect+'":</h5> <br>'
			  + '<div id="path_current_'+self.dialect+'"></div><br>'
			  + '<h5>available db for "'+self.dialect+'" dialect in that folder:</h5> <br>'
			  + ('<ul id="path_menu_'+self.dialect+'" class="ui-menu ui-widget ui-widget-content">'
			     +'</ul><br>')
			  
			  // + '<input id="update_listdir_eqs" type="button" value="update folder">'
			  + '<input id="set_up_path_'+self.dialect+'" type="button" value="set up path"><br>'
			  + '</div><br>')
		   
		       // + ('<div id="path_cs">'
		       //   + '<h5>current path cs:</h5> <br>'
		       //   + '<div id="path_current_cs"></div><br>'
			  
		       // + ('<ul id="path_menu_cs" class="ui-menu ui-widget ui-widget-content">'
		       //     +'</ul><br>')
			  
			  // + '<input id="update_listdir_cs" type="button" value="update folder">'
			  // + '<input id="set_up_path_cs" type="button" value="set up path"><br>'
			  // + '</div><br>')
		       + '</div>');
	       
	       $("#"+self.path_storage_id).html(str);

	       
	       $( '#path_menu_'+self.dialect ).menu();
	       // $( "#path_menu_cs" ).menu();
	       $("#"+self.path_id).tabs();

	       self.get_path();
	       self.set_path();		       

	   };


	   Path.prototype.get_path = function(){
	       /*
		fill ``path_current_`` value for ``cs/eqs``
		show ``os.path.listdir`` in  ``path_menu_``.
		*/

	       var self = this;

	       // FOR get path:
	       $.ajax(
		   {
		       url: 'api/tables/path',
		       method: 'GET',
		       
		       success: function (jsonResponse) {
			   
			   var objresponse = JSON.parse(jsonResponse);
			   var data = objresponse;
			   
			   console.log('path_'+self.dialect+':');
			   console.log(data[self.dialect]["path"]);
			   // console.log("path_cs:");
			   // console.log(data["cs"]["path"]);
			   
			   $("#path_current_"+self.dialect).text(data[self.dialect]["path"]);
			   // $("#path_current_cs").text(data["cs"]["path"]);
			   
			   // FOR fill menus with listdir:
			   var items = [];
			   $.each([self.dialect], function(id, elm){
			       
			       var dialect_name = elm;
			       items = [];
			       
			       console.log("dialect_name");
			       console.log(elm);
			       // ["cs", "eqs"]
			       $.each(data[dialect_name]["listdir"],
				      function(id, elm){
					  console.log(id);
					  items.push('<li class="ui-menu-item ui-widget ui-widget-content"'
						     + 'value="'+elm+'">' + elm + '</li>');
				      });
			       $("#path_menu_"+dialect_name).append(items.join(""));
			       
			       // FOR define menu events handlers:
			       // $("#path_menu_"+dialect_name).on("menufocus", function(event, ui){
			       // });
			       // $("#path_menu_"+dialect_name).on( "menublur", function( event, ui ) {
			       // });
			       $("#path_menu_"+dialect_name).on("menuselect", function(event, ui){
				   console.log("select");

				   // remove previusly selected by removing
				   // selection from all:
				   ($("#path_menu_"+dialect_name+" li")
				    .removeClass("ui-state-focus ui-state-active"));
				   
				   // to guaranty no action, if no item selected:
				   self.selected = null;
				   
				   $.each(ui, function(id, elm){
				       console.log(elm);

				       // select:
				       $(elm).addClass("ui-state-focus ui-state-active");

				       // save data:
				       self.selected = $(elm[0]).text();
				       console.log("selected:");
				       console.log(self.selected);
				       
				       //$(elm).css("background-color", "blue");
				       // $(elm[0]).css("color", "blue");
				       //elm[0].setAttribute("style", "color: blue");
				       //elm[0].style.color = "blue";
				   });
				   
			       });

			   });
			   
			   // END FOR
			   
		       },
		       
		       error: function () {
			   console.log("error to get");
		       }
		   });
	       // END FOR
	   };


	   Path.prototype.set_path = function(){
	       /*
		action for ``set_up_path_`` button.
		*/

	       var self = this;
	       // ["cs", "eqs"]
	       $.each([self.dialect], function(id, elm){
		   var dialect_name = elm;
		   $("#update_listdir_"+dialect_name).on("click", function(event){
		       // var selected_file = document.getElementById('choice_path').files[0];
		       // console.log("selected_file:");
		       // console.log(selected_file);
		       
		       console.log("tabs_path.val");
		   });
	       });
	       
	       // ["cs", "eqs"]
	       $.each([self.dialect], function(id, elm){
		   var dialect_name = elm;
		   $("#set_up_path_"+dialect_name).on("click", function(event){
		       // var selected_file = document.getElementById('choice_path').files[0];
		       // console.log("selected_file:");
		       // console.log(selected_file);
		       
		       console.log("tabs_path.val");

		       // get active tab idx:
		       var tab_idx = $("#"+self.path_id).tabs("option", "active");
		       console.log(tab_idx);

		       // get active tab name:
		       console.log($("#path_dialects li").eq(tab_idx).text());

		       // get selected file_name (with ``path_menu_``):
		       if(self.selected == null){
			   console.log("no file_name selected");
			   return				   
		       }
		       
		       // send to server:
		       var to_send = JSON.stringify({file_name: self.selected,
						     dialect_name: dialect_name});

		       $.ajax(
			   {
			       url: 'api/tables/path',
			       type: 'POST',
			       data: to_send,
			       
			       success: function(jsonResponse){
				   
				   // send
				   var objresponse = JSON.parse(jsonResponse);
				   data = objresponse;
				   console.log("\ndata");
				   console.log(data);
				   
				   // update div_path_result:
				   $("#path_current_"+dialect_name).text(data["path"]);
				   // $("#div_path_result").show();
			       },
			       
			       error: function () {
				   console.log("error to send");
			       }
			   });
		       
		   });
	       });
	       /*
		$("#set_up_path_eqs").on("click", function(event){
		// var selected_file = document.getElementById('choice_path').files[0];
		// console.log("selected_file:");
		// console.log(selected_file);
		console.log("tabs_path.val");
		var tab_idx = $("#tabs_path").tabs("option", "active");
		console.log(tab_idx);
		console.log($("#path_dialects li").eq(tab_idx).text());
		
		// get selected file:
		console.log("path_menu_eqs.val");
		console.log($("#path_menu_eqs").val());
		
		
		var path_str = $("#path_value").val();
		var dialect_name = $("#path_selector").val();
		console.log("dialect_name");
		console.log(dialect_name);
		if(path_str == ""){
		if(dialect_name == "eqs"){
		path_str = "env/equation_net/data/terms/input/demo_dialect.db";
		}
		else{
		path_str = "env/clause/data/terms/input/demo_dialect.db";
		}
		}
		console.log("selected:");
		console.log(path_str);
		$("#path_value").val(path_str);
		$("#div_path_result").text(path_str);
		
		
		var to_send = JSON.stringify({path: $("#path_value").val(),
		dialect_name: ""});
		
		
		// reinit:
		path_str = "";
		$("#path_value").val(path_str);
		console.log("to_send:")
		console.log(JSON.stringify(to_send))
		
		});
		*/
	   };

	   return {
	       Path: Path		   
	       };
       });
       

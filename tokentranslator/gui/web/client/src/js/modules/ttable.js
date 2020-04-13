console.log("log ttable.js");


//['jquery', 'jquery-ui-custom/jquery-ui'],
//
define(['require', 'jquery', 'jquery-ui-custom/jquery-ui', 'tabulator/tabulator.min',
	"modules/teditor", "modules/editor_signatures"],
       function(require, $, ui, tabulator, teditor, seditor){

	   $ = require('jquery');
	   jquery_ui = require('jquery-ui-custom/jquery-ui');
	   tabulator = require('tabulator/tabulator.min');
	   

	   function Table(div_storage_id,
			  table_type, dialect,
			  table_handler, editor_handler){
	       
	       // FOR global variables:

	       var self = this;

	       self.div_storage_id = div_storage_id;
	       self.dialect = dialect;
	       self.table_handler = table_handler;

	       if (self.dialect == "signatures"){
		   self.editor = new seditor.SEditor("div_replacer_storage",
						     editor_handler);
		   self.keys = {0: "predicate", 1: "signature"};
		   // predicate
		   // signature

	       }else{
		   self.editor = new teditor.TEditor("div_replacer_storage",
						     editor_handler);
		   self.keys = {0: "term_name", 1: "grammar_type"};
		   // term_name;
		   // grammar_type;
	       }

	       // self.editor = [];
	       // checker for test table button state:
	       this.scene_checker = 0;
	       
	       // index for using like primary key
	       // (in uniqueness rows check):
	       this.table_index = typeof table_index !== 'undefined' ? table_index : "id";  // "id";
	       
	       // name of table to wait from server:
	       this.table_type = typeof table_type !== 'undefined' ? table_type : "unnamed_table";
	       // index for selecting:
	       this.s_index = 0;
	       
	       // checker for add button state:
	       this.add_checker = 0;
	       
	       // for main and add tables:
	       // this.data = [];
	       this.data_add = [];
	       this.data_add_storage = [];
	       this.data_delete_storage = [];
	       this.columns = [];
	       this.columns_add = [];
	       // END FOR

	       // for replacer set:
	       self.row_data = "none";
	       
	       // for replacer delete:
	       self.row_data_delete = "none";
	       
	   };
	   
	
	   Table.prototype.remove_table = function(){
	       var self = this;

	       if (self.table_type == "dialect"){
		   self.editor.remove();
	       }

	       $("#controls").remove();
	       try
	       {
		   self.s_index = 0;
		   self.add_checker = 0;
		   self.data_add = [];
		   self.data = [];
		   self.columns = [];
		   self.columns_add = [];
		   
		   if($("#div_table").length){
		       $("#div_table").tabulator("destroy");
		   };
		   if($("#div_table_add").length){
		       $("#div_table_add").tabulator("destroy");
		   };
		   
	       }
	       catch(e)
	       {
		   console.log("tables div_table div_table_add not exist");
	       }	       
	   };
	   
	   
	   Table.prototype.draw = function(){
	       var self = this;
	       var str = ('<div id="div_table" style="height: 300px; overflow: auto; border-width: 3px"></div>'
			  + '<div id="controls">'
			  + '<input id="add" type="button" value="Добавить">'
			  + '<input id="delete" type="button" value="Удалить">'
			  + '<input id="save" type="button" value="Сохранить">'
			  + '</div>'
			  + '<div id="div_table_add"></div>'
			  + '<div id="div_table_log"></div>'
			  + '<div id="div_replacer_storage"></div>');

	       console.log("self.div_storage_id", self.div_storage_id);
	       $("#"+self.div_storage_id).html(str);
	       
	       if(self.table_type == "dialect"){
		   self.editor.draw();
	       };
	   };


	   Table.prototype.apply_controls = function(){
	       var self = this;

	       // FOR add button:
	       $("#add").on("click", function(){
		   if(self.add_checker == 0)
		   {
		       // create new changeable table.
		       
		       /*
			 var data_add = [{id:"3", name:"enter name"}];
			 var columns_add = [
			 {title:"id", field: "id", editor:true},
			 {title:"name", field: "name", editor:true},
			 ];
		       */
		       // for prevent clearing arrays when destroy tabular:
		       var data_add_local = self.data_add.slice();
		       var columns_add_local = self.columns_add.slice();
		       console.log("data_add"+JSON.stringify(data_add_local));
		       console.log("columns_add"+JSON.stringify(columns_add_local));
		       
		       // FOR adding table for add data:
		       $("#div_table_add").tabulator({
			   tooltips:true,
			   data: data_add_local,
			   columns: columns_add_local,
		       });
		       
		       // select first row:
		       // $("#div_table_add").tabulator("selectRow", 1);
		       // END FOR
		       
		       self.add_checker = 1;
		   }
		   else
		   {
		       // add data to main table from changeable table.
		       // after second click at add button
		       
		       // var selectedData = $("#div_table_add").tabulator("getSelectedData");
		       
		       // get new data:
		       var data_to_add = $("#div_table_add").tabulator("getData");
		       console.log("data_to_add ");
		       console.log(data_to_add);
		       
		       ////// FOR check if element exist in old data:
		       var data_old = $("#div_table").tabulator("getData");
		       
		       _exist = false;
		       console.log("data_old");
		       console.log(data_old);
		       $.each(data_old, function(id_old, entry_old){
			   
			   if(entry_old[self.table_index] == data_to_add[0][self.table_index]){
			       _exist = true;
			       console.log("self.table_index");
			       console.log(self.table_index);
			       console.log("entry_old[self.table_index]");
			       console.log(entry_old[self.table_index]);
			       console.log("data_to_add[0][self.table_index]");
			       console.log(data_to_add[0][self.table_index]);
			       // break
			       return false;
			   }
		       });
		       ////// END FOR
		       
		       if(_exist)
		       {
			   // write log:
			   console.log("alredy exist");
			   $("#div_table_log").text("значение поля "
						    + self.table_index
						    + " не уникально");
			   $("#div_table_log").show();
		       }
		       else
		       {
			   // hide log:
			   $("#div_table_log").hide();
			   
			   // add to table:
			   $("#div_table").tabulator("addRow", data_to_add[0]);
			   
			   // add to storage for saving:
			   self.data_add_storage.push(data_to_add[0]);
			   console.log("data_add_storage:")
			   console.log(JSON.stringify(self.data_add_storage))
			   
			   // remove table_add:
			   $("#div_table_add").tabulator("destroy");
			   self.add_checker = 0;
			   
			   console.log("data_add_storage:")
			   console.log("(after div_table_add destroy)")
			   console.log(JSON.stringify(self.data_add_storage))
		       }
		   }
		   console.log("add_checker " + self.add_checker);
	       });
	       // END FOR
	       
	       // FOR delete
	       $("#delete").on("click", function(){
		   
		   //get array of currently selected data
		   var selectedData = $("#div_table").tabulator("getSelectedData"); 
		   console.log("selected data " + Object.keys(selectedData[0]));
		   
		   var selectedRows = $("#div_table").tabulator("getSelectedRows"); 
		   console.log("selectedRows.row.getIndex() selectedRows.row.table.options.index");
		   console.log(selectedRows);
		   
		   // copy data to sorage
		   self.data_delete_storage = self.data_delete_storage.concat(selectedData.slice());
		   
		   self.row_data_delete = self.row_data;
		   // delete from table:
		   $("#div_table").tabulator("deleteRow", self.s_index);
	       });
	       // END FOR
	       
	       // FOR save
	       $("#save").on("click", function(){
		   
		   // FOR update:
		   succ = function (jsonResponse) {
		       
		       // rewrite data from server
		       // clear self.data_add_storage
		       
		       var objresponse = JSON.parse(jsonResponse);
		       data = objresponse['table'];
		       console.log("\ndata");
		       console.log(data);
		       
		       // copy data:
		       var data_local = data.slice();
		       
		       // update table from response:
		       $("#div_table").tabulator("setData", data_local);
		       
		       // clear data_add_storage:
		       self.data_add_storage = [];
		   }


		   action = "update";
		   if(self.data_add_storage.length > 0){
		       self.send_data_to_server(self.data_add_storage, succ, action);
		   }else{
		       var table_data = $("#div_table").tabulator("getData");
		       // self.send_data_to_server(table_data, succ, action);
		   }
		   // END FOR
		   
		   // FOR delete
		   succ = function (jsonResponse) {
		       
		       // rewrite data from server
		       // clear data_delete_storage
		       
		       var objresponse = JSON.parse(jsonResponse);
		       data = objresponse['table'];
		       console.log("\ndata");
		       console.log(data);
		       
		       // copy data:
		       var data_local = data.slice();
		       
		       // update table from response:
		       $("#div_table").tabulator("setData", data_local);
		       
		       // clear data_delete_storage:
		       self.data_delete_storage = [];
		   }

		   action = "delete";
		   if(self.data_delete_storage.length > 0){
		       self.send_data_to_server(self.data_delete_storage, succ, action);

		       // FOR replacer:
		       // self.row_data_delete was chosen
		       // at delete button click
		       // as self.row_data = self.row_data_delete:
		       var row_data = self.row_data_delete;
		       // TODO: remove that:
		       
		       // var term_name = row_data.term_name;
		       // var brackets = row_data.grammar_type;
		       // console.log(term_name);
 		       
		       // FOR remove term's replacer:
		       self.editor.remove_term(row_data[self.keys[0]], row_data[self.keys[1]]);
		       // self.editor.remove_term(term_name, brackets);
		       // END FOR
		   }
		   // END FOR
		   // console.log("\ndata ");
		   // console.log(self.data);
	       });
	   };

	   
	   Table.prototype.send_data_to_server = function(data, succ, action){
	       
	       // - ``data`` -- dict with data to be send
	       // - ``succ`` -- function, describing what to
	       // do after success.

	       var self = this;

	       var data_to_send = data;
	       
    	       console.log("\ndata_to_send");
	       console.log(data_to_send);
	       
	       console.log("\n data_to_send.length");
	       console.log(data_to_send.length);
	       
	       // FOR sending data to server:
	       if(data_to_send.length){
		   var to_send = JSON.stringify({table_type: self.table_type,
						 action: action,
						 dialect: self.dialect,
						 table: data_to_send});
		   console.log("\n sending");
		   
		   console.log(to_send);
		   
		   $.ajax(
		       {
			   url: self.table_handler, //  'api/tables/'+self.table_type,
			   type: 'POST',
			   data: to_send,
			   
			   success: succ,
			   
			   error: function () {
			       console.log("error to send");
			   }
		       });
	       }
	       else
		   console.log("\n nothing to send");
	       // END FOR
	       
	   };
	   

	   Table.prototype.make_table = function(){

	       var self = this;

	       console.log("self.table_type");
	       console.log(self.table_type);

	       var succ = function (jsonResponse) {
		   // console.log("self:");
		   // console.log(self);
		   
		   self.draw();
		   
		   var objresponse = JSON.parse(jsonResponse);
		   console.log(objresponse['table']);
		   
		   data = objresponse['table'];
		   
		   // FOR add columns and data dicts:
		   /* 
		   // columns example:
		   var columns = [
		   {title:"username", field: "username"},
		   {title:"memoryused", field: "memoryused"},
		   {title:"memorylimit", field: "memorylimit"},
		   {title:"tsused", field: "tsused"},
		   {title:"tslimit", field: "tslimit"},
		   {title:"expirydate", field: "expirydate"}		
		   ];
		   */
		   
		   var entry_data_add = {};
		   console.log("FROM make_table.get:");
		   console.log("data[0] ");
		   console.log(data[0]);
		   $.each(data[0], function(index, value){
		       // make collumns for both tables:
		       
		       var entry = {};
		       var entry_columns_add = {};
		       
		       console.log(index);
		       entry.title = index;
		       entry.field = index;

		       // don't make id editable:
		       if (index == "id"){
			   entry.editor = false;
		       }else{
			   entry.editor = true;
		       }				       
		       
		       entry_columns_add.title = index;
		       entry_columns_add.field = index;
		       
		       // make entry editable (inluding id):
		       entry_columns_add.editor = true;

		       entry_data_add[index] = value;
		       // make entry editable:
		       // entry.editor = true;
		       // console.log("entry " + Object.keys(entry));
		       
		       self.columns.push(entry);
		       self.columns_add.push(entry_columns_add);
		       
		   });
		   
		   self.data_add.push(entry_data_add);
		   console.log("columns");
		   console.log(self.columns);
		   console.log("columns_add");
		   console.log(self.columns_add);
		   console.log("data_add");
		   console.log(self.data_add);
		   // END FOR
		   
		   
		   // FOR fill table:
		   // copy data to prevent deleting:
		   var data_local = data.slice();
		   var columns_local = self.columns.slice();
		   $("#div_table").tabulator(
		       {
			   tooltips:true,
			   data: data_local,
			   columns: columns_local,
			   index: self.table_index,
			   rowClick:function(e, row){
			       self.s_index = row.getIndex();
			       console.log("from rowClick:");
			       console.log("Row " + self.s_index + " Clicked!!!!")
			       // console.log(row);
			       var row_data = row.getData();
			       console.log(row_data);

			       // TODO: remove that
			       // var term_name = row_data.term_name;
			       // var brackets = row_data.grammar_type;
			       // console.log(term_name);
 			       
			       // deselect all rows:
			       $("#div_table").tabulator("deselectRow");
			       
			       // select selected row:
			       // $("#div_table").tabulator("selectRow", self.s_index);
			       row.select();
			       // row.deselect();
	
			       // save for further use in set:
			       self.row_data = row_data;
	       
			       // FOR replacer load dialect:
			       self.editor.load_term(row_data[self.keys[0]], row_data[self.keys[1]]);
			       // self.editor.load_term(term_name, brackets);
			       // END FOR
			   },	
		       });
		   // END FOR
		   
		   // fill scene component:
		   self.apply_controls();

		   if(self.table_type == "dialect"){
		       
		       self.editor.make_editor();

		       $("#code_button").on("click", function(event){

			   if (self.row_data !== "none"){
			       console.log("from code_button.click:");
			       // TODO: remove that:
			       // var term_name = self.row_data.term_name;
			       // var brackets = self.row_data.grammar_type;

			       self.editor.on_button_click(self.row_data[self.keys[0]], self.row_data[self.keys[1]]);
			       // self.editor.on_button_click(term_name, brackets);

			   }else{
			       console.log("self.row_data is none");
			   }
		       });
		       
		       // set editor default value:
		       self.editor.set_default_value("# click at row to see replacer source\n");
		       
		       // console.log("code.text");
		       // console.log($("#code").text());
		   };
		   
		   // self.make_table(data, columns, data_add, columns_add);
		   console.log("ttables.js success");
	       };

	       // data_to_send has not be empty:
	       var data_to_send = ["tmp"];
	       self.send_data_to_server(data_to_send, succ, "load");
	       
	       /*
		 $.ajax(
		 {
		 url: 'api/tables/'+self.table_type,
		 method: 'GET',
		 
		 success: ,
		 error: function () {
		 //$("#responsefield").text("Error to load api");
		 console.log("Error to load api");
		 
		 }
		 });
	       */
	   };
		   
	   return {
	       Table: Table	 
	   }
	   
       });
    
/*
  
// usage:
$('#button_table').on('click', function(event){

    words_table = new Table();
    console.log("words_table");
    console.log(words_table);

    if(words_table.scene_checker == 0){
	
	words_table.make_table();
	words_table.scene_checker = 1;
    }
    else
    {
	clear_scene();
	words_table.scene_checker = 0;
    }	
});
*/

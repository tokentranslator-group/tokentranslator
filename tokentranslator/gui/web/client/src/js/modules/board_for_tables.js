console.log("log board_for_tables.js");

define(["jquery", "modules/ttable",
	"modules/teditor", "modules/editor_signatures", "modules/editor_tabs"],
       function($, ttable, teditor, seditor, tabseditor){
	   
	   function BoardTable(net, div_storage_id, dialect,
			       table_handler, editor_handler){
	       var self = this;
	       self.net = net;
	       self.div_storage_id = div_storage_id;

	       // check supported tables:
	       if(["eqs", "cs", "signatures", "examples_sampler",
		   "examples_parser_eqs", "examples_parser_cs"].indexOf(dialect) < 0){
		   var msg = ('dialect "'+dialect+'" not supported.'
			      + ' Supported dialect names is: "eqs", "cs", "signatures", "examples_db_sampler"'
			     + '"examples_parser_eqs", "examples_parser_cs"]');
		   alert(msg);
		   throw new Error(msg);
	       };

	       self.dialect = dialect;
	       self.table_handler = table_handler;
	       self.editor_handler = editor_handler;

	       // choice keys and editor:
	       var keys;
	       var editor;
	       if (self.dialect == "signatures"){
		   editor = new seditor.SEditor("div_replacer_storage",
						     self.editor_handler);
		   keys = {0: "predicate", 1: "signature"};
	       }else{
		   if(["examples_sampler", "examples_parser_eqs",
		       "examples_parser_cs"].indexOf(self.dialect) >= 0){
		       editor = new tabseditor.TabsEditor("div_replacer_storage",
							       self.editor_handler);
		       keys = {0: "id", 1: "id"};
		       editor.set_table_name(self.dialect);
		       
		   }else{
		       editor = new teditor.TEditor("div_replacer_storage",
							 self.editor_handler);
		       keys = {0: "term_name", 1: "grammar_type"};
		   }
	       }

	       // FOR choice table select callback:
	       // default:
	       var select_callback = function(event, row){
		   console.log("from table select callback");
	       };

	       
	       if(self.dialect == "examples_sampler"){
		   select_callback = function(event, row_data){
		       console.log("from table select callback");
		       self.net.boards["sampler"].set_default_input(row_data["input"]);
		   };
	       };
	       if(self.dialect == "examples_parser_eqs"){
		   select_callback = function(event, row_data){
		       console.log("from table select callback");
		       self.net.boards["parser_eqs"].set_default_input_eqs(row_data["input"]);
		   };
	       };
	       if(self.dialect == "examples_parser_cs"){
		   select_callback = function(event, row_data){
		       console.log("from table select callback");
		           self.net.boards["parser_cs"].set_default_input_cs(row_data["input"]);
		   };
	       };
	       // END FOR

	       // init table:
	       self.dialect_table = new ttable.Table({
		   div_storage_id: self.div_storage_id,
		   table_type: "dialect",
		   dialect: self.dialect,
		   table_handler: self.table_handler,
		   editor: editor,
		   keys: keys,
		   select_callback: select_callback
	           });
	       console.log("new Table done");

	   };
	   
	   BoardTable.prototype.init_board = function(){
	       var self = this;
	       console.log("new table begin");

	       self.dialect_table.make_table();
	       console.log("board for tables initiated");
	   };


	   BoardTable.prototype.save_entry = function(entry){
	       var self = this;
	       self.dialect_table.save_entry(entry);
	       console.log("BoardTable.save_entry");
	   };

	   BoardTable.prototype.remove = function(){
	       var self = this;
	       self.dialect_table.remove_table();
	       console.log("board for table removed");
	   };

	   return {
	       Board: BoardTable
	   };
       }
      );

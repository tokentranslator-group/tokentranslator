console.log("log board_for_tables.js");

define(["jquery", "modules/ttable"],
       function($, ttable){
	   
	   function BoardTable(div_storage_id, dialect,
			       table_handler, editor_handler){
	       var self = this;
	       self.div_storage_id = div_storage_id;
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
	   };
	   
	   BoardTable.prototype.init_board = function(){
	       var self = this;
	       console.log("new table begin");
	       
	       self.dialect_table = new ttable.Table(self.div_storage_id,
						     "dialect", self.dialect,
						     self.table_handler, self.editor_handler);
	       console.log("new Table done");
	       self.dialect_table.make_table();
	       console.log("board for tables initiated");
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

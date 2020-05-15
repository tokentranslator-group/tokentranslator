console.log("log board_for_paths.js");

define(["jquery", "modules/tpath"],
       function($, tpath){
	   function BoardPath(div_storage_id, dialect){
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
	       
	   };
	   
	   BoardPath.prototype.init_board = function(){
	       console.log("BoardPath.init_board");
	       var self = this;
	       self.path = new tpath.Path("parser_tabs_path_"+self.dialect,
					  self.div_storage_id, self.dialect);
	       self.path.make_path();
	       console.log("board for paths initiated");
	       console.log("self.div_storage_id = ", self.div_storage_id);
	   };


	   BoardPath.prototype.remove = function(){
	       var self = this;
	       self.path.remove();
	       console.log("board for paths removed");
	   };

	   return {
	       Board: BoardPath
	   };
       });

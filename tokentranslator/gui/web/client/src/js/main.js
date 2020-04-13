// For any third party dependencies, like jQuery, place them in the lib folder.

// Configure loading modules from the lib directory,
// except for 'app' ones, which are in a sibling
// directory.
requirejs.config({
    baseUrl: 'static/src/js/libs',
    paths: {
        modules: '../modules'
    },
    packages: [{
	// name: The name of the package (used for the module name/prefix mapping)
        name: "codemirror",

	// location: The location on disk. Locations are relative to the baseUrl
	// configuration value, unless they contain a protocol or start with a front slash (/).
        location: "codemirror",

	// main: The name of the module inside the package that should be used when
	// someone does a require for "packageName". The default value is "main",
	// so only specify it if it differs from the default. The value is relative to the package folder.
        main: "lib/codemirror"
    }]

});

// Start loading the main app file. Put all of
// your application logic in there.
// 
requirejs(['jquery', 'jquery-ui-custom/jquery-ui', 'modules/scene',
	   'modules/board_for_tables', 'modules/board_for_paths', 'modules/net',
	   'modules/parser', 'modules/ttree', 'modules/sampler', 'modules/board_for_welcome'],
	  function($, ui, scene, tables, tpath, net, tparser, mtree, sampler, bwelcome){

	      var self = this;
	      
	      // boards:
	      self.boards = {
		  welcome: new bwelcome.Board("div_scene"),
		  path_eqs: new tpath.Board("div_scene", "eqs"),
		  path_cs: new tpath.Board("div_scene", "cs"),
		  
		  tables_eqs: new tables.Board("div_scene", "eqs",
					       'api/tables/dialect',
					       'api/tables/replacer'),
		  tables_cs: new tables.Board("div_scene", "cs",
					      'api/tables/dialect',
					      'api/tables/replacer'),
		  tables_signatures: new tables.Board("div_scene", "signatures",
						      'api/tables/signatures',
						      'api/tables/signatures_code'),

		  parser_eqs: new tparser.Parser("eqs"),
		  parser_cs: new tparser.Parser("cs"),
		  sampler: new sampler.Sampler()
	      };
	      
	      // board for patterns:
	      self.pboard = undefined;
	      self.current_mode = undefined;
	      
	      self.update = function(mode){
		  /* Choice what board to draw in index.htm
		   mode is a key in self.boards
		   */
		  console.log("from update:");
		  console.log(self.current_mode);
		  console.log(mode);
		  if (self.current_mode != undefined){
		      if(self.current_mode == mode){
			  return;	  
		      }else{
			  console.log("current_mode: "+self.current_mode);
			  console.log("new_mode: "+mode);
			  self.boards[self.current_mode].remove();
			  self.boards[mode].init_board();
		      }
		  }else{
		      console.log("mode:", mode);
		      console.log("begin_init_board");
		      self.boards[mode].init_board();
		  }
		  self.current_mode = mode;
	      };

	      // create tree:
	      self.tree = new mtree.MTree(self, "api/tree");

	      console.log("all files loaded");
	      
	      $( document ).ready(function() {
		  self.tree.create_tree();

		  console.log("current_mode:", self.current_mode);
		  
		  //self.update("tables_eqs");
		  self.update("welcome");
		  // self.update("path_cs");
		  // self.update("path_eqs");
		  
		  console.log("dialect:", self.boards[self.current_mode].dialect);
		  
		  
		  /*
		  // FOR path
		  path.init_path();
		  // END FOR

		  // for checking what to write: sampling or parse pages:
		  var checker = $("#frame_sampling").val() != undefined;
		  console.log("checker:");
		  console.log(checker);
		  
		  if(checker){
		      // FOR sampler    
		      var board_sampler = new sampler.Sampler();
		      board_sampler.create_sampler();
		      // END FOR    
		  }else{
		      // FOR parser
		      var board_parser = new tparser.Parser();		      
		      board_parser.create_parser("eqs");
		      // board_parser.create_parser("cs");
		      // END FOR
		  };
		  
		  
		  // FOR net:
		  // net.loop_net();
		  // END FOR
		  
		  // FOR tables:
		  tables.loop_dialect_table();
		  // tables.loop_users_table();
		  // END FOR
		   */
	      });
	  });


/*
$( document ).ready(function() {

    // FOR import scripts:
    var imports = ["http://localhost:8888/static/src/js/scene.js",
		   "http://localhost:8888/static/src/js/ttable.js",
		   "http://localhost:8888/static/src/js/tables.js",
		   "http://localhost:8888/static/src/js/tpath.js",
		   "http://localhost:8888/static/src/js/path.js"];
    // "http://localhost:8888/static/src/js/net.js"
    // "http://localhost:8888/static/src/js/tree.js",
		   

    var importer = function(imports){
	*
	  DESCRIPTION:
	  Import scripts from ajax reqursivery.
	*

	if (imports.length == 0)
	    {
		console.log( "Load was performed." );
		return;
	    }
	    	
	var first = imports.shift();
	
	$.ajax({
	    url: first,
	    dataType: "script",
	    success: function( data, textStatus, jqxhr ) {
		// console.log( data ); // Data returned

		// recursion:
		importer(imports);

	    }}).fail(function( jqxhr, settings, exception ) {
		console.log( first + " fail" );
		console.log(exception);
	    });
	};
    
    
    importer(imports);
    
    // END FOR
*/    

    
//});

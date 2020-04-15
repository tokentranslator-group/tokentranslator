console.log("log board_for_welcome.js");

define(["jquery"],
       function($){
	   function BoardWelcome(div_storage_id){
	       var self = this;
	       self.div_storage_id = div_storage_id;
	       
	   };
	   
	   BoardWelcome.prototype.init_board = function(){
	       var self = this;
	       var str = ('<div id="welcome_id">'
			  +'<h4>choose available option </h4>'
		       + '</div>');

	       $("#"+self.div_storage_id).html(str);
	       console.log("board for welcome initiated");
	   };


	   BoardWelcome.prototype.remove = function(){
	       var self = this;
	       $("#welcome_id").remove();
	       console.log("board for welcome removed");
	   };

	   return {
	       Board: BoardWelcome
	   };
       });

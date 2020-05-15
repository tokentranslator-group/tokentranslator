console.log("log ttree.js");


define(['require', 'jquery', 'jquery-ui-custom/jquery-ui', 'fancytree/modules/jquery.fancytree'],
       function(require, $, ui, fancytree){

	   jquery_ui = require('jquery-ui-custom/jquery-ui');
	   fancytree = require('fancytree/modules/jquery.fancytree');

	   function MTree(net, url){
	       var self = this;
	       self.net = net;
	       self.url = url;
	   };
	   
	   
	   MTree.prototype.create_tree = function create_tree(){
	       var self = this;
	       
	       $("#tree").fancytree({
		   
		   source: [
		       {title: "available", key: "1", folder: true, children: [
			   {title: "eqs parser", folder:true, key: "2",
			    children: [
				{title: "tokens path", key: "5"},
				{title: "tokens", key: "6"},
				{title: "play space", key: "7"},
				{title: "db path", key: "8"},
				{title: "db", key: "9"}]},

			   {title: "cs parser", folder:true, key: "3",
			    children: [
				{title: "tokens path", key: "10"},
				{title: "tokens", key: "11"},
				{title: "play space", key: "12"},
				{title: "db path", key: "13"},
				{title: "db", key: "14"}]},

			   {title: "sampler", folder:true, key: "4",
			    children: [
				{title: "signatures path", key: "15"},
				{title: "signatures", key: "16"},
				{title: "play space", key: "17"},
				{title: "db path", key: "18"},
				{title: "db", key: "19"}]},
		       ]}
		   ],

		   activate: function(event, data){

		       if(!data.node.isFolder()){
			   var node = data.node;

			   // A node was activated: display its title:
			   console.log(node.title);

			   if (data.node.parent.title == "eqs parser"){
			       if (data.node.title == "tokens path"){
				   self.net.update("path_eqs");
				   console.log("path activated");
				   // window.open("/", "_self");
				   // $("_self").load("/");
			       }
			       if (data.node.title=="tokens"){
				   self.net.update("tables_eqs");
				   console.log("tokens activated");
			       }
			       if (data.node.title=="play space"){

				   self.net.update("parser_eqs");
				   console.log("play space activated");
			       }
			       if (data.node.title=="db path"){
				   self.net.update("path_exs_eqs");
				   console.log("db path activated");
			       }
			       if (data.node.title=="db"){
				   self.net.update("tables_db_eqs");

				   console.log("db activated");
			       }
			   }

			   if (data.node.parent.title == "cs parser"){
			       if (data.node.title == "tokens path"){
				   self.net.update("path_cs");
				   // window.open("/", "_self");
				   // $("_self").load("/");
			       }
			       if (data.node.title=="tokens"){
				   self.net.update("tables_cs");
				   console.log("tokens activated");
			       }
			       if (data.node.title=="play space"){
				   
				   self.net.update("parser_cs");
				   console.log("play space activated");
			       }
			       if (data.node.title=="db path"){
				   self.net.update("path_exs_cs");				   
				   console.log("db path activated");
			       }
			       if (data.node.title=="db"){
				   self.net.update("tables_db_cs");
				   
				   console.log("db activated");
			       }
			   }


			   if (data.node.parent.title == "sampler"){
			       if (data.node.title == "signatures path"){
				   console.log("signatures path activated");
				   self.net.update("path_signatures");
				   // window.open("/", "_self");
				   // $("_self").load("/");
			       }
			       if (data.node.title=="signatures"){
				   self.net.update("tables_signatures");
				   console.log("signatures activated");
			       }
			       if (data.node.title=="play space"){
				   
				   self.net.update("sampler");
				   console.log("play space activated");
			       }
			       if (data.node.title=="db path"){
				   self.net.update("path_exs_s");
				   console.log("db path activated");
			       }
			       if (data.node.title=="db"){
				   self.net.update("tables_db_sampler");
				   console.log("db activated");
			       }
			   }

		       }
		   },
	       });
	   }
	   return {
	       MTree: MTree
	   }});
       

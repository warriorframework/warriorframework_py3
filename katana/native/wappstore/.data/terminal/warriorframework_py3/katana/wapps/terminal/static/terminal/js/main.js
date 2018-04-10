var terminal = {
	container: '',
	tabDiv: '<div class="cmd-tab"></div>',
	navTabText: '<i class="fa fa-times" katana-click="terminal.closeTerminal"></i>',

	init: function(){
		console.log('terminal launched');
		terminal.container = this;
		terminal.addTerminal( terminal.container );
	},

	startTerminal: function( $tabBody, tabName ){
		jQuery(function($, undefined) {
			$tabBody.terminal(function(command, term) {
				if (command !== '') {
					term.pause();
					katana.templateAPI.post( '/katana/terminal/terminal-stream', terminal.container.find('.csrf-container').text(), command, function( reply ){
						term.set_prompt( reply.location + '>' );
						term.echo( reply.output.trim() ).resume();
					});
				}
				else
			 		this.echo('');
			}, {
					greetings: 'Device Screen',
					name: tabName,
					prompt: '>',
					onInit: function(term){
						term.echo( 'Establishing Connection' );
						term.pause();
						var command = { 'instance': 'terminal' }
						katana.templateAPI.post( '/katana/terminal/terminal-stream', terminal.container.find('.csrf-container').text(), JSON.stringify(command), function( reply ){
							term.echo( 'Connected' );
							term.set_prompt( reply.location + '>' );
							term.echo( '' ).resume();
						});
					}
			});
		});
	},

	addTerminal: function( $elem ){
		var $elem = $elem ? $elem : this;
		terminal.addTerminalTab( $elem );
	},

	addTerminalTab: function( $elem ){
		var topLevel = terminal.container;
		var contentTab = $( terminal.tabDiv ).appendTo( topLevel.find('.page-content > .content') );
		terminal.startTerminal( contentTab, 'terminal' );
	},

	swichTab: function( $tab ){
		var $tab = $tab ? $tab : this;
		var tabs = $tab.closest('.page-content').find('.cmd-tab');
		tabs.removeClass('active');
		$tab.addClass('active');
		$tab.data().addClass('active');
	},


};

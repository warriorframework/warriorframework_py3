 var satya = {

//	closeSatya: function(){
//		katana.closeSubApp();
//	},
//
//	emailSatya: {
//		generalBody: '',
//
//		init: function () {
//			console.log('test auto init of app');
//			Satya.emailCases.generalBody = $(this);
//		},
//	},


	showSatyaApp: function(){
//	    alert("asdfsdaf");
//		katana.templateAPI.post.call( katana.$activeTab.find('.to-save'), null, null, katana.toJSON(), function( data ) {
//			console.log('saved', data);
//		});
        var stack = new katana.utils.Stack();
        alert(stack.length());
        stack.push("satya");
        stack.push("narayana");
        alert(stack.length());
        stack.pop();
        alert(stack.length());
        alert(stack.hasOwnProperty("push"));
        alert(stack.hasOwnProperty("s"));
	},
};

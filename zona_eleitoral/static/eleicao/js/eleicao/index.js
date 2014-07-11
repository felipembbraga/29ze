$(document).ready(function(){
   $('.delete').click(function(event){
	   $.modal.confirm('Você confirma a exclusão do questionário?', 
   			function() { // onConfirme
   				alert('ok!');
   			},
   			function() { // onCancel
   			},
   			
   			{
   				buttonsLowPadding: true,
   				actions: {}
   			}
   		);
   });
});



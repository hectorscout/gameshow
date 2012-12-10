<script type="text/javascript">
    $(document).ready(function() {
	ko.applyBindings(new PlayerViewModel());
	$('button').button();
    });


function PlayerViewModel() {
    var self = this;

    self.name = ko.observable('{{name}}');
    self.id = ko.observable('{{id}}');
    self.waiting = ko.observable(false);

    self.register = function() {
	self.waiting(true);
	self.name($("#nameInput").val());
	$.post("register",
               {name:self.name()},
               function(response) {
		   if (response.error) {
		       self.name('');
		       alert(response.error);
		   }
		   else
		       self.id(response.id);
		   self.waiting(false);
               }, 'json');
    }

    self.buzz = function() {
	self.waiting(true);
	$.post("buzz",
               {name:self.name()});
	setTimeout(function(){self.waiting(false)}, 5000);
    }

    self.logout = function() {
	$.post("logout",
               {id:self.id()});
	self.id('');
	self.name('');
    }
    
}


</script>

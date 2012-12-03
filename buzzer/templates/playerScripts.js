<script type="text/javascript">
    $(document).ready(function() {
	ko.applyBindings(new PlayerViewModel());
    });


function PlayerViewModel() {
    var self = this;

    self.name = ko.observable('');
    self.id = ko.observable('');
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
               {id:self.id()});
	setTimeout(function(){self.waiting(false)}, 5000);
    }
    
}


</script>

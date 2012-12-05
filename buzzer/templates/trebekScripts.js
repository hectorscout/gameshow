<script type="text/javascript">
    $(document).ready(function() {
	ko.applyBindings(new TrebekViewModel());
    });


function Player(data) {
    var self = this;
    
    self.name = ko.observable(data.name);
    self.score = ko.observable(data.score);
}

function TrebekViewModel() {
    var self = this;

    self.status = ko.observable('Closed')
    self.players = ko.observableArray([]);
    self.buzzes = ko.observableArray([]);

    function getPlayers() {
	$.get("players",
	      function(response) {
		  var mappedPlayers = $.map(response, function(data){ return new Player(data) });
		  self.players(mappedPlayers);
		  setTimeout(getPlayers, 5000);
	      },"json");

    }
    
    function getBuzzes() {
	$.ajax({url:"getBuzzes",
		success:function(response) {
		    self.buzzes(response);
		},
		complete:function() {
		    setTimeout(getBuzzes, 2000); 
		},
		dataType: 'json'
	       });
    }
    
    getPlayers();
    getBuzzes();

    self.clearBuzzes = function() {
	$.post("clearBuzzes");
    }

    self.setStatus = function(newStatus) {
	self.status(newStatus);
	$.post("setStatus",
	       {'status':newStatus});

	if(newStatus == 'Clear')
	    self.buzzes([]);
    }

}


</script>

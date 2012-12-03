<script type="text/javascript">
    $(document).ready(function() {
	ko.applyBindings(new BoardViewModel());
    });


function BoardViewModel() {
    var self = this;
    function getPlayers() {
	$.get("players",
	      function(response) {
		  console.log(response);
		  self.players(response);
	      },"json");
    }
    
    self.players = ko.observableArray([]);
    
    getPlayers();
    
}


</script>

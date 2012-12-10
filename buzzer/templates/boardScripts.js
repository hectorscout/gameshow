<script type="text/javascript">
    var buzzSound;
    $(document).ready(function() {
	ko.applyBindings(new BoardViewModel());
	buzzSound = document.createElement('audio');
	buzzSound.setAttribute('src', 'http://www.mariomayhem.com/downloads/sounds/super_mario_bros/smb_jumpsmall.wav');
    });


function Player(data) {
    var self = this;
    
    self.name = ko.observable(data.name);
    self.score = ko.observable(data.score);
}

function BoardViewModel() {
    var self = this;
    function getPlayers() {
	$.get("players",
	      function(response) {
		  var mappedPlayers = $.map(response, function(data){ return new Player(data) });
		  self.players(mappedPlayers);
		  setTimeout(getPlayers, 5000);
	      },"json");

    }
    self.players = ko.observableArray([]);

    function getBuzz() {
	$.ajax({url:"getBuzz",
		success:function(response) {
		    if (response) {
			self.buzzes.push(response);
			if (self.buzzes.length == 1)
			    buzzSound.play();
		    }
		    
		},
		complete:function() {
		    getBuzz();
		},
		dataType: 'json'
	       });
    }
    self.buzzes = ko.observableArray([]);
    
    function getStatus() {
	$.ajax({url:"getStatus",
		data:{currentStatus: self.status()},
		success:function(response) {
		    self.status(response);
		},
		complete:function() {
		   // getStatus();
		    
		},
		dataType: 'json'
	       });
    }
    self.status = ko.observable('Closed');

    self.status.subscribe(function(newValue) {
	if(newValue == 'Clear')
	    self.buzzes([]);
    });

    getPlayers();
    getBuzz();
    getStatus();
}


</script>

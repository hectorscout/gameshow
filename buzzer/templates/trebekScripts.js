<script type="text/javascript">
    $(document).ready(function() {
	ko.applyBindings(new TrebekViewModel());
	$('button').button();
	$('#gameSettings').dialog({'autoOpen': false,
				   'title': 'Game Settings',
				   'width': '400px'});
	$('#editPlayer').dialog({'autoOpen': false,
				 'title': 'Edit Player',
				 'width': '400px'});
    });


function Player(data) {
    var self = this;
    
    self.name = ko.observable(data.name);
    self.score = ko.observable(data.score);

    self.updateServer = function() {
	$.post("updatePlayer",
	       {'name':self.name(),
		'score':self.score()});
    }
    
    self.addToScore = function(value) {
	self.score(self.score() + value);
    }

    self.score.subscribe(function(newScore) {
	self.updateServer();
    });

    self.displayString = ko.computed(function() {
	return self.name() + ': ' + self.score();
    });

}

function Settings() {
    var self = this;

    self.status = ko.observable('');
    self.answerTimeout = ko.observable('');
    self.buzzMode = ko.observable('');

    $.get("getSettings",
	  function(response) {
	      self.status(response.status);
	      self.answerTimeout(response.answerTimeout);
	      self.buzzMode(response.buzzMode);
	  },"json");
        
    self.setSetting = function(name, value) {
	$.post("setSetting",
	       {'name':name,
		'value':value});
    }

    self.status.subscribe(function(newStatus){
	self.setSetting('status', newStatus);
    });

    self.answerTimeout.subscribe(function(newAnswerTimeout){
	self.setSetting('answerTimeout', newAnswerTimeout);
    });

    self.buzzMode.subscribe(function(newBuzzMode){
	self.setSetting('buzzMode', newBuzzMode);
    });

}

function TrebekViewModel() {
    var self = this;

    self.players = ko.observableArray([]);
    self.selectedPlayer = ko.observable('');
    self.buzzes = ko.observableArray([]);
    self.settings = new Settings();

    self.settings.status.subscribe(function(newStatus) {
	if(newStatus == 'Clear') {
	    self.buzzes([]);
	    $.post("clearBuzzes");
	}
    });

    function getPlayers() {
	$.get("players",
	      function(response) {
		  var mappedPlayers = $.map(response, function(data){ return new Player(data) });
		  self.players(mappedPlayers);
		  setTimeout(getPlayers, 5000);
	      },"json");

    }

    self.editPlayer = function(player) {
	self.selectedPlayer(player);
	$('#editPlayer').dialog('open');
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

    self.editSettings = function() {
	$('#gameSettings').dialog('open');
    }

    getPlayers();
    getBuzzes();
}


</script>

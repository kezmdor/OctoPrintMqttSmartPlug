$(function() {
    function MqttsmartplugViewModel(parameters) {
        var self = this;

        self.loginState = parameters[1];
        self.currentState = ko.observable(undefined);
        self.plug_indicator = undefined;
        self.poweroff_dialog = undefined;

        self.onAfterBinding = function() {
            self.plug_indicator = $("#plugcontrol_indicator");
            self.plug_indicator.css('color', '#808080');
            if (self.loginState.isUser()) {
                self.getPlugState();                
            }
            self.poweroff_dialog = $("#plug_poweroff_confirmation_dialog");
        };

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "mqttsmartplug") {
                return;
            }
			self.currentState(data.currentState);
			switch(self.currentState()) {
				case "on":
                    self.plug_indicator.css('color', '#00E000');
                    break;
				case "off":
                    self.plug_indicator.css('color', '#E00000');
					break;
				default:
                    self.plug_indicator.css('color', '#808080');
			}          
        };

        self.getPlugState = function() {
            $.ajax({
                url: API_BASEURL + "plugin/mqttsmartplug",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "getState"
                }),
                contentType: "application/json; charset=UTF-8"
            })
        };

        self.togglePlug = function () {
            if (self.currentState() == "on") {
                self.poweroff_dialog.modal("show");
            }else{
                self.turnPlugOn();
            }
        }

        self.turnPlugOn = function() {
            $.ajax({
                url: API_BASEURL + "plugin/mqttsmartplug",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "turnOn"
                }),
                contentType: "application/json; charset=UTF-8"
            })
        };

        self.turnPlugOff = function() {
            $.ajax({
                url: API_BASEURL + "plugin/mqttsmartplug",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "turnOff"
                }),
                contentType: "application/json; charset=UTF-8"
            })
            self.poweroff_dialog.modal("hide");            
        };

    }


    ADDITIONAL_VIEWMODELS.push([
        MqttsmartplugViewModel,
        ["settingsViewModel", "loginStateViewModel"],
        ["#navbar_plugin_mqttsmartplug"]
    ]);
});
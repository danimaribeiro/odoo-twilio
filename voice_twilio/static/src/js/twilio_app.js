odoo.define('twilio_base', function (require) {
    "use strict";

var core = require('web.core');
var base_bus = require('bus.bus');
var Dialog = require('web.Dialog');
var Model = require('web.Model');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var WebClient = require('web.WebClient');
var Notification = require('web.notification').Notification;

var QWeb = core.qweb;
var _t = core._t;


var TwilioCallNotification = Notification.extend({
    template: "TwilioCallNotification",

    init: function(parent, title, text, callId) {
        this._super(parent, title, text, true);
        this.callId = callId;

        this.events = _.extend(this.events || {}, {
            'click .link2answer': function() {
                var self = this;
                session.rpc("/twilio/token", {}).then(function (data) {
                    Twilio.Device.setup(data);
                    Twilio.Device.incoming(function(connection) {
                        connection.accept();
                    });
                    Twilio.Device.ready(function (device) {
                        var params = {
                            To: 'queue'
                        };
                        Twilio.Device.connect(params);
                        self.destroy(true);
                    });
                });
            },

            'click .link2reject': function() {
                this.destroy(true);
            },
        });
    },
});

WebClient.include({
    show_application: function() {
        this.start_polling_calls();
        return this._super();
    },
    on_logout: function() {
        var self = this;
        base_bus.bus.off('notification', this, this.bus_notification);
        this._super();
    },
    start_polling_calls: function() {
        this.channel_twilio_call = 'notify_twilio_call_' + this.session.uid;
        base_bus.bus.add_channel(this.channel_twilio_call);
        base_bus.bus.on('notification', this, this.twilio_call_notification);
        base_bus.bus.start_polling();
    },
    twilio_call_notification: function(notifications) {
        var self = this;
        _.each(notifications, function (notification) {
            var channel = notification[0];
            var message = notification[1];
            if (channel == self.channel_twilio_call) {
                self.on_message_new_call(message);
            }
        });
    },
    on_message_new_call: function(message){
        if(this.notification_manager) {
            var notification = new TwilioCallNotification(this.notification_manager, message.title, message.message, message.call_id);
            this.notification_manager.display(notification);
        }
    }
});


    var OpenDialer = Widget.extend({
        template: 'twilio_base.phone.dial',
        start: function() {
            session.rpc("/twilio/token", {}).then(function (data) {
                Twilio.Device.setup(data);
                Twilio.Device.incoming(function(connection) {
                    connection.accept();
                });
            });
        },
        events: {
            'click .num': 'on_link_analytics_settings',
            'click .btn-twilio-call': 'on_click_make_call',
            'click .btn-twilio-hangup': 'on_click_disconnect',
        },
        on_link_analytics_settings: function(ev) {
            var self = this;
            var $target = $(ev.currentTarget);
            var num = $target.data('num');
            this.$('#dial-twilio-number').val(this.$('#dial-twilio-number').val() + num);
        },
        on_click_make_call: function(e){
            var params = {
                To: this.$('#dial-twilio-number').val()
            };
            console.log('Calling ' + params.To + '...');
            Twilio.Device.connect(params);
        },
        on_click_disconnect: function(e){
            Twilio.Device.disconnectAll();
        },
    });

    core.action_registry.add('twilio_base.open_dialer', OpenDialer);
});

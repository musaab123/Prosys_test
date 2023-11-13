odoo.define('setu.customer.score', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var field_registry = require('web.field_registry');
var field_utils = require('web.field_utils');

var QWeb = core.qweb;
var _t = core._t;

var ShowScoreRuleWidget = AbstractField.extend({
    events: _.extend({
        'click .outstanding_credit_assign': '_onOutstandingCreditAssign',
    }, AbstractField.prototype.events),
    supportedFieldTypes: ['char'],

    isSet: function() {
        return true;
    },

    _render: function() {
        var self = this;
        var info = JSON.parse(this.value);
        if (!info) {
            this.$el.html('');
            return;
        }
        this.$el.html(QWeb.render('SetuCustomerScoreRule', {
            lines: info.content,
            title: info.title,
            is_rating: info.is_rating
        }));
        _.each(this.$('.js_customer_score_rule'), function (k, v){
            var isRTL = _t.database.parameters.direction === "rtl";
            var content = info.content;
            var options = {
                content: function () {
                    var $content = $(QWeb.render('SetuCustomerScoreRulePopOver', {content: content,is_rating: info.is_rating}));
                    return $content;
                },
                html: true,
                placement: 'right',
                title: 'Rule Information',
                trigger: 'focus',
                delay: { "show": 0, "hide": 100 },
                container: $(k).parent(),
            };
            $(k).popover(options);
        });
    }
});

field_registry.add('customer_rating_show_rule', ShowScoreRuleWidget);

return {
    ShowScoreRuleWidget: ShowScoreRuleWidget
};

});

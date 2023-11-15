odoo.define('kg_document_expiry.documentexpiry', function (require) {
'use strict';

const DocumentsInspector = require('documents.DocumentsInspector');

const documentexpiry = DocumentsInspector.include({

 _renderFields: function () {
        const options = {mode: 'edit'};
        const proms = [];
        if (this.records.length === 1) {
            proms.push(this._renderField('name', options));
            proms.push(this._renderField('expiry_date', options));
            proms.push(this._renderField('notify_before', options));


            if (this.records[0].data.type === 'url') {
                proms.push(this._renderField('url', options));
            }
            proms.push(this._renderField('partner_id', options));
        }
        if (this.records.length > 0) {
            proms.push(this._renderField('owner_id', options));

            proms.push(this._renderField('folder_id', {
                icon: 'fa fa-folder o_documents_folder_color',
                mode: 'edit',
            }));
        }
        return Promise.all(proms);
    },
});

return documentexpiry;



});

odoo.define("stock_scan_frontend.action_start_scanning", function(require) {
console.log("begin");
    "use strict";
    var core = require("web.core");
    var Widget = require("web.Widget");
    var _t = core._t;
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
var AbstractAction = require('web.AbstractAction');
    var ScanningModel = Backbone.Model.extend({
        initialize: function (session, attributes) {
        console.log("x");

            var self = this;
            this.active_id = this.get_stock_id();
            this.ready = this.load_stock_data();
            this.data = {};
            this.quantsData = {};
            this.products = {};
            this.codeProducts = {}
            this.scan_lines = {}
            this.addedScansObj = {};
            this.totalQty = 0;
            this.createdScansObj = {};
            this.type_of_scaning = '';
            this.pickin_Typ_code = '';
        },
        get_stock_id: function () {
        console.log("2");
            var lochash = location.hash.substr(1);
            var activeid = lochash.substr(lochash.indexOf('id='))
                    .split('&')[0]
                    .split('=')[1];
            return activeid;
        },
        load_stock_data: function () {
        console.log("3a");
            var loaded = new $.Deferred();
            console.log("3b"+loaded);
            var self = this;
            console.log("3c");
            var stock_picking = rpc.query({
                model:'stock.picking',
                method: 'get_stock_lot_scan_data',
                args: [self.active_id],
            }).then(function (result) {
            console.log("4");
                result = JSON.parse(result);
                console.log("5");
                self.scan_lines = result.scan_lines;
console.log("6a");
                self.data = result.data;
                console.log(result);
                console.log("7a");
                self.products = result.products;
                console.log("8a");
                self.codeProducts = result.productsCodeData;
                console.log("9a");
                self.type_of_scaning = result.type_of_scaning;
                console.log("10a");
                self.pickin_Typ_code = result.pickin_Typ_code;
                console.log("11a");
                self.res_id = result.res_id;
                console.log("12a");

                loaded.resolve();
                console.log("13a");

            });
                console.log("14a");
        return loaded;
        }
    });


    var Scanning = AbstractAction.extend({
        template: "Scanning",
 xmlDependencies: ['/stock_scan_frontend/static/src/xml/stock.xml'],

        events: {
            "click .cancel_button": "cancel_button",
            "click .deleteScan": "deleteScan",
            "change .qty": "calculateTotalQty",
            "keyup .qty": "calculateTotalQty",
            "change #default_code": function () {
            console.log("5x");
                var self = this;
                var modalShown = false;
                $("div[id$=Modal]").each(function () {
                    if (($(this).data('bs.modal') || {}).isShown) {
                        document.getElementById('audio').play();
                        $('#default_code').val('').blur().focus();
                        modalShown = true;
                    }
                });
                if (modalShown == false) {
                    var default_code = $('#default_code').val();
                    if (default_code.trim() != '') {
                        if (self.stock_data.codeProducts[default_code]) {
                            $('input#scan_box').focus();
                        } else {
                            document.getElementById('audio').play();
                            $('#default_code').val('').blur().focus();
                            $("#productNotFoundModal").modal();
                        }
                    }
                }
            },
            "change #scan_box": "search_product",
            "click .selectLine": "selectLine",
            "change #expiration_date": "search_product_third",
            "click .save_button": function () {
                var self = this;

console.log("6");
                var stock_picking = rpc.query({
                    model:'stock.picking',
                    method: 'scan_from_ui',
                    args: [self.stock_data.res_id, self.stock_data.createdScansObj, self.stock_data.addedScansObj],
                }).then(function (server_ids) {

                    self.do_action({
                        type: 'ir.actions.act_window',
                        res_model: 'stock.picking',
                        res_id: parseInt(self.stock_data.active_id),
                        views: [[false, 'form']],
                        target: 'main',
                    });
                });
            }
        },
        init: function(parent, options) {
            this._super.apply(this, arguments);
            console.log("1");
            this.stock_data = new ScanningModel(require);
            console.log("7x");
            //this.start();
        },

        start: function () {
        console.log("8aaaaaaaaa");
            var sup = this._super();
            var self = this;
            this._super.apply(this, arguments);
            console.log(this.xmlDependencies);
            

            return this.stock_data.ready.done(function () {
               // self.$el.prepend();
                setTimeout(function () {
                    $('input#scan_box').focus();
                    if (self.stock_data.type_of_scaning == 'third_group') {
                        $('input#default_code').show().focus();
                        $('input#expiration_date').show();
                    } else {
                        $('input#default_code').remove();
                        $('input#expiration_date').remove();
                        $('input#scan_box').attr('style', '');
                    }

                    var scan_lines_count = Object.keys(self.stock_data.scan_lines).length;
                    if (scan_lines_count > 0) {
                        for (var i = 0; i < scan_lines_count; i++) {
                            var scan_box = self.stock_data.scan_lines[i]['serial'];
                            if (!self.stock_data.addedScansObj[scan_box]) {
                                self.stock_data.addedScansObj[scan_box] = {};
                            }
                            var encoded = CryptoJS.MD5(scan_box);
                            var qty = parseInt(self.stock_data.scan_lines[i]['qty']);
                            var product_id = self.stock_data.scan_lines[i]['product_id'];
                            var product = self.stock_data.products[product_id]
                            var lot_name = self.stock_data.scan_lines[i]['lot_name'];
                            var date = new Date(self.stock_data.scan_lines[i]['expiration_date']);
                            self.stock_data.addedScansObj[scan_box][product_id] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': product['id'], 'product_uom_qty': qty, 'lot_no': scan_box, 'lot_name': lot_name, 'expiration_date': self.stock_data.scan_lines[i]['expiration_date']};
                            var html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + product['id'] + '" />' + product['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                            $('table tbody').append(html);
                            self.stock_data.totalQty += qty;
                        }
                        $('span.totalQty').html(self.stock_data.totalQty);
                    }
                }, 1000);
            });
        },
        selectLine: function (e) {
        console.log("9");
            var self = this;
            var el = e.target;
            var scan_box = $(el).attr('id');
            var encoded = CryptoJS.MD5(scan_box);
            var product_id = $(el).val();
            var product = self.stock_data.products[product_id];
            var found = false;
            var input = false;
            $("input.lineProductId").each(function () {
                if ($(this).val() == product_id && $(this).parent('td').parent('tr').attr('id') == encoded) {
                    found = true;
                    input = $(this);
                    return false;
                }
            });
            if (found == true) {
                var tRow = $(input).parent('td').parent('tr');
                var qtyInput = tRow.find('input.qty');
                var qty = parseInt(qtyInput.val()) + 1;
                qtyInput.val(qty);
            } else {
                var scan = false;
                var countProducts = Object.keys(self.stock_data.data[scan_box]).length;
                for (var i = 0; i < countProducts; i++) {
                    var line = self.stock_data.data[scan_box][i];
                    var line_product = self.stock_data.products[line['product_id']];
                    if (line_product['id'] == product_id) {
                        scan = line;
                        break;
                    }
                }
                var lot_name = scan['lot_name'];
                var expiration_date = scan['expiration_date'];
                var date = new Date(expiration_date);
                var today = new Date();
                var qty = 1;
                var html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + product['id'] + '" />' + product['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                if (date < today) {
                    html = '<tr id="' + encoded + '" style="background:red"><td><input type="hidden" class="lineProductId" value="' + product['id'] + '" />' + product['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                    $('.expiredLotSerialSpan').html(scan_box);
                    document.getElementById('audio').play();
                    $("#expiredModal").modal();
                }
                $('table tbody').append(html);
            }
            if (!self.stock_data.addedScansObj[scan_box]) {
                self.stock_data.addedScansObj[scan_box] = {};
            }
            if (!self.stock_data.addedScansObj[scan_box][product_id]) {
                self.stock_data.addedScansObj[scan_box][product_id] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': product['id'], 'product_uom_qty': 1, 'lot_no': scan_box, 'lot_name': lot_name, 'expiration_date': expiration_date};
            } else {
                self.stock_data.addedScansObj[scan_box][product_id].product_uom_qty += 1;
            }
            $('#productCode').html(product['default_code']);
            $('#productName').html(product['name']);
            $('#productSerial').html(scan_box);
            $('#productsList').html();
            $('#productsList').hide();
            $('input#scan_box').val('').blur().focus();
            self.stock_data.totalQty += 1;
            $('span.totalQty').html(self.stock_data.totalQty);
        },
        calculateTotalQty: function (e) {
        console.log("10");
            var self = this;
            var el = e.target;
            var newQty = 0;
            var tRow = $(el).parent('td').parent('tr');
            var qtyInput = tRow.find('input.qty');
            var qty = tRow.find('input.qty').val();
            if (qty == '')
                qty = 0;
            var scan_box = tRow.find('span.scan_box_line').html();
            var product_id = tRow.find('input.lineProductId').val();
            var countProducts = Object.keys(self.stock_data.data[scan_box]).length;
            for (var i = 0; i < countProducts; i++) {
                var line = self.stock_data.data[scan_box][i];
                if (line['product_id'] == product_id) {
                    var scan = line;
                    break;
                }
            }

            if(scan.product_qty !== -1 && scan.product_qty < qty){
                // quantity limit reached
                qtyInput.val(scan.product_qty);
                qty = scan.product_qty;
                document.getElementById('audio').play();
                $("#limitReachedModal").modal();
            }
            if (self.stock_data.createdScansObj[scan_box] && self.stock_data.createdScansObj[scan_box][product_id]) {
                self.stock_data.createdScansObj[scan_box][product_id].product_uom_qty = qty;
            }
            self.stock_data.addedScansObj[scan_box][product_id].product_uom_qty = qty;
            $('.qty').each(function (el) {
                var value = $(this).val();
                if ($(this).val() == '')
                    value = 0;
                newQty += parseInt(value);
            });
            self.stock_data.totalQty = newQty;
            $('span.totalQty').html(self.stock_data.totalQty);

        },
        deleteScan: function (e) {
        console.log("11");
            var self = this;
            var el = e.target;
            if (el.nodeName != 'TD') {
                el = $(el).parent();
            }
            var tRow = $(el).parent('tr');
            var qty = tRow.find('input.qty').val();
            var scan_box = tRow.find('span.scan_box_line').html();
            var product_id = tRow.find('input.lineProductId').val();
            if (self.stock_data.createdScansObj[scan_box] && self.stock_data.createdScansObj[scan_box][product_id]) {
                delete self.stock_data.createdScansObj[scan_box][product_id];
            }
            delete self.stock_data.addedScansObj[scan_box][product_id];
            self.stock_data.totalQty -= parseInt(qty);
            $('span.totalQty').html(self.stock_data.totalQty);
            tRow.remove();
            $('#productCode').html('');
            $('#productName').html('');
            $('#productSerial').html('');
            if ($('input#default_code').length > 0) {
                $('table').focus();
                $('#default_code').val('').focus();
            } else {
                $('table').focus();
                $('input#scan_box').focus();
            }
        },
        search_product_third: function (e) {
        console.log("12");
            var self = this;
            var expiration_date = $('input#expiration_date').val();
            if (expiration_date.trim() != '') {
                var dateArray = expiration_date.split('-');
                var dateCheck = new Date(expiration_date);
                if ((dateArray.length != 3 && dateArray.length != 2)) {
                    document.getElementById('audio').play();
                    $('#expiration_date').val('').blur().focus();
                    $("#invalidDateModal").modal();
                } else {
                    if (dateArray.length == 2) {
                        expiration_date = expiration_date + "-01";
                    }
                    var dateCheck = new Date(expiration_date);
                    if (isNaN(dateCheck.valueOf())) {
                        document.getElementById('audio').play();
                        $('#expiration_date').val('').blur().focus();
                        $("#invalidDateModal").modal();
                    } else {
                        var scan_box = $('input#scan_box').val();
                        var default_code = $('input#default_code').val();
                        if (self.stock_data.addedScansObj[scan_box] == undefined)
                            self.stock_data.addedScansObj[scan_box] = {};
                        if (self.stock_data.createdScansObj[scan_box] == undefined)
                            self.stock_data.createdScansObj[scan_box] = {};
                        if (self.stock_data.data[scan_box]) {
                            var scan = false;
                            var countProducts = Object.keys(self.stock_data.data[scan_box]).length;
                            for (var i = 0; i < countProducts; i++) {
                                var line = self.stock_data.data[scan_box][i];
                                var product = self.stock_data.products[line['product_id']];
                                if (product['default_code'] == default_code) {
                                    scan = line;
                                    break;
                                }
                            }
                            if (scan == false) {
                                var encoded = CryptoJS.MD5(scan_box);
                                var codeProduct = self.stock_data.codeProducts[default_code];
                                var date = new Date(expiration_date);
                                var qty = 1;
                                var html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + codeProduct['id'] + '" />' + codeProduct['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + scan_box + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                                $('table tbody').append(html);
                                self.stock_data.addedScansObj[scan_box][codeProduct['id']] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': codeProduct['id'], 'product_uom_qty': 1, 'lot_no': scan_box, 'lot_name': scan_box, 'expiration_date': expiration_date};
                                self.stock_data.createdScansObj[scan_box][codeProduct['id']] = {'product_id': codeProduct['id'], 'product_qty': 1, 'lot_no': codeProduct['name'], 'lot_name': scan_box, 'name': scan_box, 'expiration_date': expiration_date, 'ref': default_code};
                                self.stock_data.data[scan_box][Object.keys(self.stock_data.data[scan_box]).length] = {
                                    'product_id': codeProduct['id'],
                                    'lot_no': scan_box,
                                    'lot_name': scan_box,
                                    'expiration_date': expiration_date,
                                    'product_qty': -1
                                };
                                $('#productCode').html(codeProduct['default_code']);
                                $('#productName').html(codeProduct['name']);
                                $('#productSerial').html(scan_box);
                                self.stock_data.totalQty += 1;
                                $('span.totalQty').html(self.stock_data.totalQty);
                                $('table').show();
                            } else {
                                var encoded = CryptoJS.MD5(scan_box);
                                var product_id = scan['product_id'];
                                var lot_name = scan['lot_name'];
                                if (self.stock_data.addedScansObj[scan_box][product_id]) {
                                    var tr = $('#' + encoded);
                                    var qtyInput = tr.find('.qty');
                                    qty = parseInt(qtyInput.val());
                                    if(scan.product_qty === -1 || scan.product_qty > qty){
                                        qtyInput.val(qty + 1);
                                        if (self.stock_data.createdScansObj[scan_box][product_id]) {
                                            self.stock_data.createdScansObj[scan_box][product_id].product_qty = qty + 1;
                                        }
                                        self.stock_data.addedScansObj[scan_box][product_id].product_uom_qty = qty + 1;
                                        self.stock_data.addedScansObj[scan_box][product_id].product_uom_qty = qty + 1;
                                        $('#productCode').html(self.stock_data.products[product_id]['default_code']);
                                        $('#productName').html(self.stock_data.products[product_id]['name']);
                                        $('#productSerial').html(scan_box);
                                        self.stock_data.totalQty += 1;
                                        $('span.totalQty').html(self.stock_data.totalQty);
                                        $('table').show();
                                    }else{
                                        // quantity limit reached
                                        document.getElementById('audio').play();
                                        $('#default_code').val('').blur().focus();
                                        $("#limitReachedModal").modal();
                                    }
                                } else {
                                    if(scan.product_qty === -1 || scan.product_qty > qty){
                                        var product = self.stock_data.products[product_id]
                                        var date = new Date(expiration_date);
                                        var today = new Date();
                                        var qty = 1;
                                        html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + product['id'] + '" />' + product['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                                        if (date < today) {
                                            html = '<tr id="' + encoded + '" style="background:red"><td><input type="hidden" class="lineProductId" value="' + product['id'] + '" />' + product['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                                            document.getElementById('audio').play();
                                            $('#expiration_date').val('').blur().focus();
                                            $("#expiredLotSerialSpan").modal();
                                        }
                                        $('table tbody').append(html);
                                        self.stock_data.addedScansObj[scan_box][product['id']] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': product['id'], 'product_uom_qty': 1, 'lot_no': scan_box, 'lot_name': lot_name, 'expiration_date': expiration_date};
                                        $('#productCode').html(product['default_code']);
                                        $('#productName').html(product['name']);
                                        $('#productSerial').html(scan_box);
                                        self.stock_data.totalQty += 1;
                                        $('span.totalQty').html(self.stock_data.totalQty);
                                        $('table').show();
                                    }else{
                                        // product not in location
                                        document.getElementById('audio').play();
                                        $('#scan_box').val('').blur().focus();
                                        $("#ProductNotAvailableModal").modal();
                                    }
                                }
                            }
                        } else {
                            var encoded = CryptoJS.MD5(scan_box);
                            var codeProduct = self.stock_data.codeProducts[default_code];
                            var date = new Date(expiration_date);
                            var qty = 1;
                            html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + codeProduct['id'] + '" />' + codeProduct['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + scan_box + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                            $('table tbody').append(html);
                            self.stock_data.addedScansObj[scan_box][codeProduct['id']] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': codeProduct['id'], 'product_uom_qty': 1, 'lot_no': scan_box, 'lot_name': scan_box, 'expiration_date': expiration_date};
                            self.stock_data.createdScansObj[scan_box][codeProduct['id']] = {'product_id': codeProduct['id'], 'product_qty': 1, 'lot_no': codeProduct['name'], 'lot_name': scan_box, 'name': scan_box, 'expiration_date': expiration_date, 'ref': default_code};
                            self.stock_data.data[scan_box] = [{
                                'product_id': codeProduct['id'],
                                'lot_no': scan_box,
                                'lot_name': scan_box,
                                'expiration_date': expiration_date,
                                'product_qty': -1
                            }];
                            $('#productCode').html(codeProduct['default_code']);
                            $('#productName').html(codeProduct['name']);
                            $('#productSerial').html(scan_box);
                            self.stock_data.totalQty += 1;
                            $('span.totalQty').html(self.stock_data.totalQty);
                        }
                        $('input#default_code').val('');
                        $('input#scan_box').val('');
                        $('input#expiration_date').val('');
                        $('input#default_code').focus();
                    }
                }
            }
        },
        search_product: function (e) {
        console.log("13");
            var self = this;
            if (self.stock_data.type_of_scaning != 'third_group') {
                var scan_box = $('#scan_box').val();
                if (scan_box.trim() != '') {
                    var modalShown = false;
                    $("div[id$=Modal]").each(function () {
                        if (($(this).data('bs.modal') || {}).isShown) {
                            document.getElementById('audio').play();
                            $('#scan_box').val('').blur().focus();
                            modalShown = true;
                        }
                    });
                    if ($('#productsList').css('display') !== 'none') {
                        document.getElementById('audio').play();
                        modalShown = true;
                    }
                    if (modalShown == false) {
                        var encoded = CryptoJS.MD5(scan_box);
                        if (self.stock_data.data[scan_box] != undefined) {
                            var countProducts = Object.keys(self.stock_data.data[scan_box]).length;
                            if (countProducts == 1) {
                                var scan = self.stock_data.data[scan_box][0];
                                var product_id = scan.product_id;
                                var product = self.stock_data.products[product_id];
                                var lot_name = scan.lot_name;
                                var expiration_date = scan.expiration_date;
                                var qty = 1;
                                if (!self.stock_data.createdScansObj[scan_box]) {
                                    self.stock_data.createdScansObj[scan_box] = {};
                                }
                                if (!self.stock_data.addedScansObj[scan_box]) {
                                    self.stock_data.addedScansObj[scan_box] = {};
                                }
                                if (self.stock_data.addedScansObj[scan_box][product_id]) {
                                    var tr = $('#' + encoded);
                                    var qtyInput = tr.find('.qty');
                                    qty = parseInt(tr.find('.qty').val());
                                    if(scan.product_qty === -1 || scan.product_qty > qty){
                                        qtyInput.val(qty + 1);
                                        if (self.stock_data.createdScansObj[scan_box][product_id]) {
                                            self.stock_data.createdScansObj[scan_box][product_id].product_qty = qty + 1;
                                        }
                                        self.stock_data.addedScansObj[scan_box][product_id].product_uom_qty = qty + 1;
                                        $('#productCode').html(self.stock_data.products[product_id]['default_code']);
                                        $('#productName').html(self.stock_data.products[product_id]['name']);
                                        $('#productSerial').html(scan_box);
                                        self.stock_data.totalQty += 1;
                                        $('span.totalQty').html(self.stock_data.totalQty);
                                    }else{
                                        // quantity limit reached
                                        document.getElementById('audio').play();
                                        $('#scan_box').val('').blur().focus();
                                        $("#limitReachedModal").modal();
                                    }
                                } else {
                                    if(scan.product_qty === -1 || scan.product_qty >= qty){
                                        var product = self.stock_data.products[product_id];
                                        var date = new Date(expiration_date);
                                        var today = new Date();
                                        var html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + product['id'] + '" />' + product['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                                        if (date < today) {
                                            html = '<tr id="' + encoded + '" style="background:red"><td><input type="hidden" class="lineProductId" value="' + product['id'] + '" />' + product['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                                            $('.expiredLotSerialSpan').html(scan_box);
                                            document.getElementById('audio').play();
                                            $('#scan_box').val('').blur().focus();
                                            $("#expiredModal").modal();
                                        }
                                        $('table.o_list_view tbody').append(html);
                                        self.stock_data.addedScansObj[scan_box][product_id] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': product['id'], 'product_uom_qty': 1, 'lot_no': scan_box, 'lot_name': lot_name, 'expiration_date': expiration_date};
                                        $('#productCode').html(product['default_code']);
                                        $('#productName').html(product['name']);
                                        $('#productSerial').html(scan_box);
                                        self.stock_data.totalQty += 1;
                                        $('span.totalQty').html(self.stock_data.totalQty);
                                    }else{
                                        // product not in location
                                        document.getElementById('audio').play();
                                        $('#scan_box').val('').blur().focus();
                                        $("#ProductNotAvailableModal").modal();
                                    }
                                }
                            } else {
                                var linesHtml = 'Please select a product from the list:<br /><br />';
                                var anyLineFound = false;
                                for (var i = 0; i < countProducts; i++) {
                                    var line = self.stock_data.data[scan_box][i];
                                    var product = self.stock_data.products[line['product_id']];
                                    if(line.product_qty > 0){
                                        anyLineFound = true;
                                    }
                                    qty = 1;
                                    if (self.stock_data.addedScansObj[scan_box][product['id']]) {
                                        var tr = $('#' + encoded);
                                        var qtyInput = tr.find('.qty');
                                        qty = parseInt(tr.find('.qty').val());
                                    }
                                    if(line.product_qty === -1 || line.product_qty > qty){
                                        linesHtml += '<input type="radio" value="' + product['id'] + '" class="selectLine" id="' + scan_box + '" /> [' + product['default_code'] + '] ' + product['name'] + '<br />';
                                    }
                                }
                                document.getElementById('audio').play();
                                if(linesHtml != 'Please select a product from the list:<br /><br />'){
                                    $('#productsList').html(linesHtml);
                                    $('#productsList').show();//.focus();
                                }else{
                                    if(anyLineFound){
                                        // quantity limit reached
                                        $('#scan_box').val('').blur().focus();
                                        $("#limitReachedModal").modal();
                                    }else{
                                        // product not in location
                                        document.getElementById('audio').play();
                                        $('#scan_box').val('').blur().focus();
                                        $("#ProductNotAvailableModal").modal();
                                    }
                                }
                            }
                        } else {
                            if (self.stock_data.pickin_Typ_code != 'incoming') {
                                document.getElementById('audio').play();
                                $('#scan_box').val('').blur().focus();
                                $("#warningModal").modal();
                            } else {
                                var qty = 1;
                                var extracted_lot = scan_box.split('/')[0].slice(5, -1);
                                var extracted_lot2 = extracted_lot.replace(/^['0']*/, "");
                                if (!self.stock_data.codeProducts[extracted_lot] && !self.stock_data.codeProducts[extracted_lot2]) {
                                    document.getElementById('audio').play();
                                    $('#scan_box').val('').blur().focus();
                                    $("#productNotFoundModal").modal();
                                } else {
                                    if (self.stock_data.codeProducts[extracted_lot]) {
                                        var codeProduct = self.stock_data.codeProducts[extracted_lot];
                                    } else if (self.stock_data.codeProducts[extracted_lot2]) {
                                        var codeProduct = self.stock_data.codeProducts[extracted_lot2];
                                    }
                                    var extracted_dateString = scan_box.slice(scan_box.indexOf("/") + 1).split(" ")[0];
                                    var extracted_year = extracted_dateString.slice(0, 2);
                                    if (extracted_year == 'Fa') {
                                        extracted_year = 11;
                                    }
                                    extracted_year = '20' + extracted_year;
                                    var month = extracted_dateString.slice(2, 5);
                                    month = Math.round(parseInt(month) / 30);

                                    var ex_date = extracted_year + "-" + month + "-" + '01';
//                                    lot_name = scan_box.split('/')[1].slice(5, -4);
                                    lot_name = scan_box.slice(scan_box.indexOf('/') + 1).slice(5, -4);
                                    var date = new Date(ex_date);
                                    self.stock_data.data[scan_box] = {};
                                    if (!self.stock_data.createdScansObj[scan_box]) {
                                        self.stock_data.createdScansObj[scan_box] = {};
                                    }
                                    if (!self.stock_data.addedScansObj[scan_box]) {
                                        self.stock_data.addedScansObj[scan_box] = {};
                                    }
                                    if (self.stock_data.type_of_scaning == 'first_group') {
                                        html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + codeProduct['id'] + '" />' + codeProduct['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                                        $('table tbody').append(html);
                                        self.stock_data.addedScansObj[scan_box][codeProduct['id']] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': codeProduct['id'], 'product_uom_qty': 1, 'lot_no': scan_box, 'lot_name': lot_name, 'expiration_date': ex_date};
                                        self.stock_data.createdScansObj[scan_box][codeProduct['id']] = {'product_id': codeProduct['id'], 'product_qty': 1, 'lot_no': codeProduct['name'], 'lot_name': lot_name, 'name': scan_box, 'expiration_date': ex_date, 'ref': codeProduct['default_code']};
                                        self.stock_data.data[scan_box][0] = {
                                            'product_id': codeProduct['id'],
                                            'lot_no': scan_box,
                                            'lot_name': lot_name,
                                            'expiration_date': ex_date,
                                            'product_qty': -1
                                        };
                                    } else if (self.stock_data.type_of_scaning == 'second_group') {
                                        var lot_no = codeProduct['default_code'];
                                        html = '<tr id="' + encoded + '"><td><input type="hidden" class="lineProductId" value="' + codeProduct['id'] + '" />' + codeProduct['name'] + '</td><td><input type="number" class="qty" value="' + qty + '"/></td><td><span class="scan_box_line">' + scan_box + '</span></td><td>' + lot_name + '</td><td>' + $.datepicker.formatDate("mm/dd/yy", date) + '</td><td style="cursor:pointer;" class="deleteScan"><span class="fa fa-trash-o" name="delete"></span></td></tr>';
                                        $('table tbody').append(html);
                                        self.stock_data.addedScansObj[scan_box][codeProduct['id']] = {'stock_picking_id': parseInt(self.stock_data.res_id), 'product_id': codeProduct['id'], 'product_uom_qty': 1, 'lot_no': lot_no, 'lot_name': lot_name, 'expiration_date': ex_date};
                                        self.stock_data.createdScansObj[scan_box][codeProduct['id']] = {'product_id': codeProduct['id'], 'product_qty': 1, 'lot_no': codeProduct['name'], 'lot_name': lot_name, 'name': codeProduct['default_code'], 'expiration_date': ex_date, 'ref': codeProduct['default_code']};
                                        self.stock_data.data[scan_box][0] = {
                                            'product_id': codeProduct['id'],
                                            'lot_no': scan_box,
                                            'lot_name': lot_name,
                                            'expiration_date': ex_date,
                                            'product_qty': -1
                                        };
                                    }
                                    $('#productCode').html(codeProduct['default_code']);
                                    $('#productName').html(codeProduct['name']);
                                    $('#productSerial').html(scan_box);
                                    self.stock_data.totalQty += 1;
                                    $('span.totalQty').html(self.stock_data.totalQty);
                                }
                            }
                        }
                    }
                    $('#scan_box').val('').blur().focus();
                }
            } else {
                var scan_box = $('#scan_box').val();
                var dateArray = scan_box.split('-');
                if (dateArray.length > 1) {
                    document.getElementById('audio').play();
                    $('#scan_box').val('').blur().focus();
                    $("#invalidLotModal").modal();
                } else {
                    $('input#expiration_date').focus();
                }
            }
        },
        cancel_button: function (e) {
        console.log("14");
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: 'stock.picking',
                res_id: parseInt(self.stock_data.active_id),
                views: [[false, 'form']],
                target: 'main',
            });
        }
    });
  //  instance.web.client_actions.add('stock.scan', 'instance.stock_scan_frontend.Scanning');
    core.action_registry.add("stock.scan", Scanning);
return Scanning;
});
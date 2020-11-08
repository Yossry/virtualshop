jQuery(document).ready(function () {

    window.newWindow = null
});
function openScanWindow(loadedStockLotScanData, type, type_of_scaning) {
console.log("2b");

    if (window.newWindow != null) {
        window.newWindow.close();
        window.newWindow = null;
    }
    window.newWindow = window.open("", "mywindow", 'screenX=1,screenY=1,left=1,top=1,scrollbars=1,menubar=0,location=0,resizable=1,width=' + screen.availWidth + ',height=' + screen.availHeight);
    var interval = setInterval(checkNewWindow, 1000);
    function checkNewWindow() {
        if (window.newWindow != null) {

            clearInterval(interval);
            var closeInterval = setInterval(checkNewWindowClosed, 1000);
            function checkNewWindowClosed() {
                if ((window.newWindow == null) || (window.newWindow.closed)) {
                    clearInterval(closeInterval);
                    window.location.reload();
                }
            }
console.log("1b");

            var result = JSON.parse(loadedStockLotScanData);
            var url = result.scanUrl;
            var input = (type == 'in') ? '<input type="hidden" name="incoming" id="incoming" value="in" />' : '<input type="hidden" name="incoming" id="incoming" value="out" />';
            var type_of_scaning_input = (type_of_scaning == 'third') ? '<input type="hidden" name="type_of_scaning" id="type_of_scaning" value="third" />' : '<input type="hidden" name="type_of_scaning" id="type_of_scaning" value="other" />';
            jQuery(window.newWindow.document.body).html('<form method="post" action="' + url + '"><input type="hidden" name="result" id="result" />' + input + type_of_scaning_input + '</form>');
            var inputResult = jQuery(window.newWindow.document.body).find("input#result");
            inputResult.val(loadedStockLotScanData);
            var form = jQuery(window.newWindow.document.body).find("form");
            form.submit();
        }
    }


}

function getScanWindowData(type, type_of_scaning) {
 console.log("1ax");
    jQuery('button:contains("Start Scan")').hide();
    odoo.define('stock_lot_scan.load_lot_data', function (require) {
    console.log("1a");
        "use restrict";
        jQuery("span:contains('savebeforescanbutton')").parent('button').click(function () {
            var Model = require('web.Model');
            var stock_pecking_model = new Model('stock.picking');
            var interval = setInterval(checkId, 1000);
            function checkId() {
console.log("2a");
                var hashtag = window.location.hash.substr(1);
                var vars = hashtag.split("&");
                var id = 0;
                for (var i = 0; i < vars.length; i++) {
                    params = vars[i].split("=");
                    if (params[0] == 'id') {
                        id = params[1];
                    }
                }
                if (id != 0) {
                    clearInterval(interval);
                    stock_pecking_model.call('get_stock_lot_scan_data', [id]).then(function (loadedStockLotScanData) {
                        openScanWindow(loadedStockLotScanData, type, type_of_scaning);
                    });
                }
            }
        });
        jQuery("span:contains('savebeforescanbutton')").parent('button').click();
    });
}

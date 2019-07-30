$('#lntipModal').ready(function () {
        
    ajaxCall = "https://api.coindesk.com/v1/bpi/currentprice/USD.json";
        
        getPrice(ajaxCall);

          var auto_refresh = setInterval(function () {
              getPrice(ajaxCall);
          } , 30000); // Every 30 seconds        

    });

    function getPrice(url) {
        $.getJSON(url, function (data) {
            var items = [];
            
            $.each(data, function (key, val) {
                if (key == "bpi") {
                    $.each(val, function (key1, val1) {
                        if (key1 == 'USD') {
                            $.each(val1, function (key2, val2) {
                                if (key2 == "rate") {
                                    price = val2;
                                    price = price.replace(/\,/g,'')
                                    // price = parseInt(price,10);
                                    price = Math.round(price * 100) / 100;
                                    dollarSatoshi = price / 100000000; 
                                    satoshiDollar = 1000 / price * 100000;
                                    satoshiDollar = parseInt(satoshiDollar);
                                    satoshiDollar = satoshiDollar.toString();
                                    dollarSatoshi = dollarSatoshi.toString();
                                    price = price.toString();
                                    if($('#oneDollarBitcoin:empty').length) {
                                        $('#oneDollarBitcoin').html('');
                                    }
                                    if($('#oneDollarSatoshi:empty').length) {
                                        $('#oneDollarSatoshi').html('');
                                    }
                                    if($('#oneDollar:empty').length) {
                                        $('#oneDollar').html('');
                                    }
                                    $("#oneDollarBitcoin").html(dollarSatoshi);
                                    $("#oneDollarSatoshi").html(price);
                                    $("#oneDollar").html(satoshiDollar);
                                    }

                                });
                            }
                        });

                    if (key == "time") {
                        $.each(val, function (key1, val1) {
                            if (key1 == "updated")
                                $('#timeStamp').html(val1);
                        });
                    }
                }
             });
        });
    }


function scanner(){
    //Prepare
    var done = function(err, status){
      if(err){
        console.error(err._message);
      } else {
        console.log('QRScanner is initialized. Status:');
        console.log(status);
      }
    };

    QRScanner.prepare(done);

    //Scan
    var callback = function(err, contents){
      if(err){
        console.error(err._message);
      }
      alert('The QR Code contains: ' + contents);
    };

    QRScanner.scan(callback);

    //Cancel
    QRScanner.cancelScan(function(status){
      console.log(status);
    });

    //Show
    QRScanner.show(function(status){
      console.log(status);
    });

    //Hide
    QRScanner.hide(function(status){
      console.log(status);
    });

    //Lighting
    QRScanner.enableLight(function(err, status){
      err && console.error(err);
      console.log(status);
    });

    //Disable light
    QRScanner.disableLight(function(err, status){
      err && console.error(err);
      console.log(status);
    });

    //Camera Reversal
    QRScanner.useFrontCamera(function(err, status){
      err && console.error(err);
      console.log(status);
    });

    QRScanner.useBackCamera(function(err, status){
      err && console.error(err);
      console.log(status);
    });

    var back = 0; // default camera on plugin initialization
    var front = 1;
    QRScanner.useCamera(front, function(err, status){
      err && console.error(err);
      console.log(status);
    });
}
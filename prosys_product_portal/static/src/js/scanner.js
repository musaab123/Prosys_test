// let html5QrcodeScanners = {};
//new Html5QrcodeScanner(
//         "reader", { fps: 500, qrbox: { width: 950, height: 950 },rememberLastUsedCamera: true,aspectRatio: 1.7777778, facingMode: "environment" });
var html5QrcodeScanners;
var quagga;
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("myModal");
    const scanButton = document.getElementById("scanButton");
    
    // Open the modal and initialize scanner when the button is clicked
    scanButton.addEventListener("click", function() {
        modal.style.display = "block";

        const qrBoxWidthPercentage = 60; // Adjust this value as needed
        const qrBoxHeightPercentage = 60; // Adjust this value as needed

        const qrBoxWidth = (qrBoxWidthPercentage / 100) * window.innerWidth;
        const qrBoxHeight = (qrBoxHeightPercentage / 100) * window.innerHeight;

        // html5QrcodeScanners = new Html5QrcodeScanner(
        // "reader", { fps: 60, qrbox: { width: qrBoxWidth, height: qrBoxWidth },rememberLastUsedCamera: true,aspectRatio: 1.7777778, facingMode: "environment" }
        // );
        
        // html5QrcodeScanners.render(onScanSuccess, onScanError);
        quagga = Quagga;
        quagga.init({
            inputStream : {
              name : "Live",
              type : "LiveStream",
              constraints: {
                width: 800,
                height: 600,
                facingMode: "environment",
                // deviceId: "7832475934759384534"
              },
            //   area: { // defines rectangle of the detection/localization area
            //     top: "0%",    // top offset
            //     right: "0%",  // right offset
            //     left: "0%",   // left offset
            //     bottom: "0%"  // bottom offset
            //   }, 
            // locate: true,   
              target: document.querySelector('#reader')    // Or '#yourElement' (optional)
            },
            decoder : {
              readers : ["ean_reader"]
            },
            locator : {
                patchSize: 'medium'
            },
            debug: {
                drawBoundingBox: true,
                showFrequency: true,
                drawScanline: true,
                showPattern: true
            }
          }, function(err) {
              if (err) {
                  console.log(err);
                  return
              }
              console.log("Initialization finished. Ready to start");
              quagga.start();
          });
          quagga.onDetected(onScanSuccess);
    });

    // Close the modal when the user clicks outside of it
    window.onclick = function(event) {
        if (event.target === modal) {
        // html5QrcodeScanners.clear();
        quagga.stop();
        modal.style.display = "none";
        }
    };
});


function onScanSuccess(result) {
    const resultDiv = document.getElementById("barcode");
    resultDiv.value = result.codeResult.code;
    console.log(result.codeResult.code);
    console.log(`Scan result: ${result.codeResult.code}`, result.codeResult.code);
    if (result.codeResult.code != null){
        // console.log("REACHED :: !" + html5QrcodeScanners.getState());
        // console.log(html5QrcodeScanners.getState());
        // html5QrcodeScanners.clear();;
        quagga.stop();
        closeModal();
        
    }
    // html5QrcodeScanners.clear();
    // html5QrcodeScanners.stop();
    
    
}



function onScanError(errorMessage) {
    console.log(errorMessage);
// Handle scan error
    // closeModal(); // Close the modal after error
}

function closeModal() {
    const modal = document.getElementById("myModal");
    modal.style.display = "none";
    
}
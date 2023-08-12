function uploadImage() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
  
    if (file) {
      var formData = new FormData();
      formData.append('image', file);
  
      fetch('http://pic.mlsd-pic.svc:8000/predict', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          var resultDiv = document.getElementById('result');
          resultDiv.innerText = data.class;
        })
        .catch(error => console.error('Error:', error));
    } else {
      console.error('No file selected');
    }
  }
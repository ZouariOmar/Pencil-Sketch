document
  .getElementById("fileInput")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const preview = document.getElementById("imagePreview");
        preview.src = e.target.result;
        preview.style.display = "block";
      };
      reader.readAsDataURL(file);

      // Hide "Choose Image" btn and show the submit btn
      const uploadMessage = document.querySelector("#header");
      const submitBtn = document.querySelector("#sbt");
      if (uploadMessage)
        uploadMessage.style.display = "none";
        submitBtn.style.display = "flex";
    }
  });

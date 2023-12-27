postImg.addEventListener('change', function() {
    
    const file = this.files[0];
    const reader = new FileReader();
  
    reader.onload = function(e) {
        document.querySelector(".picture").style.display = "none";
        document.querySelector(".create_post_upload_text").style.display = "none";
        let imgBlock = document.querySelector(".create_post_upload_button");
        imgBlock.style.backgroundImage = `url('${e.target.result}')`;
        imgBlock.classList.add("uploaded_img");

    };
  
    reader.readAsDataURL(file);
});
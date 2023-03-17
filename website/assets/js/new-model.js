/* Import all the needed modules */
import * as modelPreviewManagement from "./model-preview.js";

function saveModelImage() {
  const canvas = document.getElementById("model_preview");
  const dataURL = canvas.toDataURL("image/png");
  return dataURL;
}

function alertBanner(message) {
  $("#alert-details").text(message);
  $(".alert").show();
  setTimeout(function () {
    $(".alert").hide();
  }, 3000);
}

$("#modelFile").change(function () {
  const modelFile = $("#modelFile")[0].files[0];
  if (modelFile.name.split(".").pop() !== "obj") {
    alertBanner("The model file must have an obj extension");
    $("#modelFile").val("");
    return;
  }
  /* Get file url */
  const url = URL.createObjectURL(modelFile);
  $(".model-preview").show();
  $(".model-preview > canvas").hide();
  $(".model-preview > img").show();
  load_obj_model_preview(url);
});

$(document).ready(function () {
  $("#upload").click(function () {
    /* Get all the inputs */
    const modelName = $("#modelName").val();
    const modelFile = $("#modelFile")[0].files[0];
    const textureInputMethod = $("#selectTextureInputMethod").val();
    const mtlFile = $("#mtlFile")[0].files[0];
    const image = $("#image")[0].files[0];
    const color = $("#color").val();

    /* Verify that the model name has been inserted */
    if (modelName === "") {
      alertBanner("Please insert the model name");
      return;
    }

    /* Make all the checks for the model file */
    if (modelFile === undefined) {
      alertBanner("Please upload the model file");
      return;
    }

    /* Make all the checks for the texture input method */
    if (textureInputMethod.val() === "default") {
      alertBanner("Please select the texture input method");
      return;
    }

    /* Make all the checks for the mtl file */
    if (
      textureInputMethod.val() === "mtl_file" &&
      $("#mtlFile")[0].files[0] === undefined
    ) {
      alertBanner("Please upload the mtl file");
      return;
    } else {
      if (mtlFile.name.split(".")[1] !== "mtl") {
        alertBanner("The mtl file must be an mtl file");
        return;
      }
    }

    if (
      textureInputMethod.val() === "image" &&
      $("#image")[0].files[0] === undefined
    ) {
      alertBanner("Please upload the image file");
      return;
    } else {
      if (
        imageFile.name.split(".")[1] !== "png" &&
        imageFile.name.split(".")[1] !== "jpg" &&
        imageFile.name.split(".")[1] !== "jpeg"
      ) {
        alertBanner("The image file must be a png, jpg or jpeg file");
        return;
      }
    }

    /* Create the form data */
    const formData = new FormData();
    formData.append("modelName", modelName);
    formData.append("modelFile", modelFile);
    formData.append("textureInputMethod", textureInputMethod);
    formData.append("texture", texture);
    formData.append("modelPreviewImage", saveModelImage());

    /* Send the request */
    $.ajax({
      url: "upload_model.php",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (data) {
        console.log(data);
      },
      error: function (data) {
        console.log(data);
      },
    });
  });

  /* Show texture input methods based on the selected input method */
  $("#selectTextureInputMethod").change(function () {
    const selectedValue = $(this).val();
    $(".texture-input-method").hide();
    if (selectedValue === "mtl_file") {
      $("#mtlFile").parent().show();
    } else if (selectedValue === "image") {
      $("#image").parent().show();
    } else if (selectedValue === "color") {
      $("#color").parent().show();
    }
  });

  $(".return").click(function () {
    window.location.href = "index.html";
  });
});

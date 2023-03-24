const API_URL = "http://127.0.0.1:5000";
const MODELS_FOLDER = "models/";

let selectedElement = {
  modelID: null,
  textureID: null
}

$(document).ready(function () {
  let models = [];
  let dataLoaded = false;

  let isSelected = function(modelID, textureID) {
    return selectedElement.modelID === modelID && selectedElement.textureID === textureID;
  }

  let selectElement = function(modelID, textureID) {
    unsetSelected();
    selectedElement.modelID = modelID;
    selectedElement.textureID = textureID;
    $(`.models > .row > div[data-model_id="${modelID}"]`).addClass("active");
    let model = models.find((item) => item.IDModel === modelID);
    let texture = model.textures.find((item) => item.textureID === textureID);
    imgUrl = MODELS_FOLDER + modelID + "/" + texture.textureID + "." + texture.textureExtension;
    previewImgUrl = MODELS_FOLDER + modelID + "/" + texture.textureID + "-preview.jpg";
    $(`.models > .row > div[data-model_id="${modelID}"] > .card > .active-model-texture-img`).attr("src", imgUrl);
    $(`.models > .row > div[data-model_id="${modelID}"] > .card > .model-img`).attr("src", previewImgUrl);
  }

  let unsetSelected = function() {
    $(".models > .row > div").removeClass("active");
    selectedElement.modelID = null;
    selectedElement.textureID = null;
  }

  var deleteTexture = function(textureID) {
    $.ajax({
      url: API_URL+"/texture/"+textureID,
      type: "DELETE",
      success: function (data) {
        console.log(data);
      },
      error: function (error) {
        console.log(error)
      }
    });
  }

  var addTextureDOM = function (modelID, order) {
    let model = models.find((item) => item.IDModel === modelID);
    let texture = model.textures[order];
    console.log(texture);
    imgUrl = MODELS_FOLDER + modelID + "/" + texture.textureID + "." + texture.textureExtension;
    $(".banner .body > .title").after(`
      <div class="col-6 mb-3 texture ${isSelected(modelID, texture.textureID) ? 'active' : ''}" data-id_texture="${texture.textureID}">
        <span class="badge bg-secondary">Active</span>
        <i class="fa-solid fa-trash-can"></i>
        <img src="${imgUrl}">
      </div>
    `)
    $(".banner .body .texture > i:last").click(function () {
      let textureID = $(this).parent().data("id_texture");
      requestConfirm(
        `Are you sure you want to delete the texture?`,
        deleteTexture,
        textureID
      );
    });
    $(".banner .body .texture > img:last").click(function () {
      if ($(this).parent().hasClass("active")) {
        $(this).parent().removeClass("active");
        unsetSelected();
      } else {
        $(this).parent().addClass("active");
        selectElement(modelID, $(this).parent().data("id_texture"));
      }
    });
  };

  $("#selectTextureInputMethod").change(function () {
    if ($(this).val() === "image") {
      $("#textureInputMethodImage").removeClass("d-none");
      $("#textureInputMethodColor").addClass("d-none");
    } else if ($(this).val() === "color") {
      $("#textureInputMethodImage").addClass("d-none");
      $("#textureInputMethodColor").removeClass("d-none");
    }
  });

  $("#textureInputMethodColor").change(function () {
    /* Get the modelID from the banner element */
    let modelID = $(".banner").data("model_id");
    isInputValidColor("#textureInputMethodColor", 'The selected color ');
    console.log("HELLO");
  });

  (function () {
    /* Call only when the data from the server have been loaded */
    $(".models").append('<div class="row mt-4"></div>');
    $.ajax({
      url: API_URL+"/models",
      type: "GET",
      success: function (data) {
        models = JSON.parse(data);
        dataLoaded = true;
        console.log(models)
        models.forEach((element, index) => {
          addModelToDom(index);
        });
      },
      error: function (error) {
        console.log("Error: " + error)
      }
    });
  })();


  /* Model management */

  var addModelToDom = function (order) {
    if (dataLoaded) {
      if (order > models.length - 1) {
        console.error("Order is out of range");
        return;
      }
      imgSrc = MODELS_FOLDER + models[order].IDModel + "/" + models[order].defaultTexture.textureID + "-preview.jpg";
      /* order is the index in of the model in the data array */
      $(".models > .row").append(
        `<div class="col-12 col-sm-6 col-lg-4 col-xl-3 mb-4" data-order="${order}" data-model_id="${models[order].IDModel}" data-model_name="${models[order].modelName}">
                      <div class="card">
                          <img src="${imgSrc}" class="model-img" alt="Image Model ${models[order].modelName}">
                          <img src="assets/img/texture.jpg" class="active-model-texture-img" alt="Active Texture Image"> 
                          <span>${models[order].modelName}</span>
                      </div>
                  </div>
              `
      );
      /* Add the event only to the last created element */
      $(".models .card:last").click(function () {
        openLeftBanner(
          $(this).parent().data("model_id")
        ); /* Open the left banner */
      });
    } else {
      console.error("Data not loaded");
    }
  };
  
  /*** Delete model management ***/
  var removeModelFromDom = (modelID) => { $(`.models > .row > div[data-model_id="${modelID}"]`).remove()};
  
  $(".delete-model button").click(function () {
    let modelID = $(".banner").data("model_id");
    requestConfirm(
      `Are you sure you want to delete the model?`,
      deleteModel,
      modelID
    );
  });

  let deleteModel = function (modelID) {
    $.ajax({
      url: API_URL + "/model/" + modelID,
      type: 'DELETE',
      success: function (data) {
        removeModelFromDom(modelID);
        closeLeftBanner();
      },
      error: function (error) {
        console.log("Error: " + error)
      }
    });
  };

  /*** Search bar management ***/
  $(".search-bar input").keyup((e) => {
    $(".models > div > div")
      .show()
      .filter(function () {
        return (
          $(this)
            .data("model_name")
            .toLowerCase()
            .indexOf($(".search-bar input").val().toLowerCase()) != 0
        );
      })
      .hide();
  });

  /*** Left banner management ***/
  function openLeftBanner(modelID) {
    /* Get selectedModel from modelID */
    let selectedModel = models.find((item) => item.IDModel === modelID);  
  
    /* Create banner content */
    $(".banner .body .texture").remove();
    for (let order = 0; order < selectedModel.textures.length; addTextureDOM(selectedModel.IDModel, order++));     
    $(".banner .header .title").html(selectedModel.modelName);

    /* Show the banner */
    $(".banner").data("model_id",selectedModel.IDModel).addClass("active");
    $(".banner-overlay").addClass("active");
    $(".banner-overlay, .close-banner").on("click", () => {closeLeftBanner()});
  }

  function closeLeftBanner() {
    $(".banner").removeClass("active");
    $(".banner-overlay").removeClass("active");
    $(".banner-overlay, .close-banner").off("click");
  }

  /*** Navigation functions ***/
  $(".new-model").click(() => { window.location.href = "new-model.html" });

  /*** Confirm actions functions ***/
  function requestConfirm(message, callback, args) {
    $("#confirmModal .modal-body").html(message);
    /* Toogle a bootstrap modal */
    $("#confirmModal").modal("toggle");     
    $("#confirmModal .confirmButton").click(() => {
      callback(args);
      $("#confirmModal").modal("toggle");
    });
  }
});
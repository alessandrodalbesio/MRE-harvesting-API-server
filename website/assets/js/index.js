const API_URL = "http://127.0.0.1:5000";
const MODELS_FOLDER = "models/";

$(document).ready(function () {
  let models = [];
  let dataLoaded = false;

  let isSelected = function(modelID, textureID) {
    return false;
  }

  var addTextureDOM = function (modelID, order) {
    let texture = models.find((item) => item.IDModel === modelID).textures[order];
    imgUrl = MODELS_FOLDER + modelID + "/" + texture + "-preview.jpg";
    $(".banner .body > .title").after(`
                <div class="col-6 mb-3 texture ${isSelected(modelID, texture) ? "active" : ""
      }" data-id_texture="${texture.id}">
                    <span class="badge bg-secondary">Active</span>
                    <i class="fa-solid fa-trash-can"></i>
                    <img src="${imgUrl}">
                </div>
            `);
    $(".banner .body .texture > i:last").click(function () {
      let modelID = $(".banner").data("model_id");
      let textureID = $(this).parent().data("id_texture");
      requestConfirm(
        `Are you sure you want to delete the texture?`,
        deleteTexture,
        { modelID: modelID, textureID: textureID }
      );
    });
    $(".banner .body .texture > img:last").click(function () {
      if ($(this).parent().hasClass("active")) {
        $(this).parent().removeClass("active");
        unselect();
      } else {
        $(this).parent().addClass("active");
        setSelected(modelID, $(this).parent().data("id_texture"));
      }
    });
  };


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
      imgSrc = MODELS_FOLDER + models[order].IDModel + "/" + models[order].defaultTexture + "-preview.jpg";
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
    for (let order = 0; order < selectedModel.textures.length; addTextureDOM(selectedModel.IDModel, order++));     
    $(".banner .header .title").html(selectedModel.modelName);
    $(".banner .body .texture").remove();

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


$(document).ready(function () {
  var data = [
    {
      id: 1,
      name: "Strawberry",
      imgSrc: "assets/img/test.jpg",
      textures: [
        {
          id: 1,
          imgUrl: "assets/img/texture.jpg",
        },
      ],
    },
    {
      id: 2,
      name: "Apple",
      imgSrc: "assets/img/test.jpg",
      textures: [
        {
          id: 1,
          imgUrl: "assets/img/texture.jpg",
        },
      ],
    },
  ];

  /*** MODEL AND TEXTURE SELECTION ***/
  var selected = { modelID: "", textureID: "" };
  function setSelected(modelID, textureID, internalOrigin = true) {
    selected.modelID = modelID;
    selected.textureID = textureID;
    let selectedElement = $('[data-model_id="' + selected.modelID + '"]');
    if (internalOrigin) {
      /* ...send the selection to the server... */
    } else {
      /* if bannerLeft open on the modelID selected than switch*/
    }
    /* Add the active class to the selected element and put it as the first element */
    $(selectedElement).addClass("active");
    if ($(selectedElement).data("order") != 0)
      $(selectedElement).insertBefore($('[data-order="0"]'));
  }
  function isSelected(modelID, textureID) {
    return selected.modelID == modelID && selected.textureID == textureID;
  }
  function getSelected() {
    return {
      modelID: selected.modelID,
      textureID: selected.textureID,
    };
  }
  function unselect() {
    let selectedElement = $('[data-model_id="' + selected.modelID + '"]');
    if ($(selectedElement).data("order") != 0)
      $(selectedElement).insertAfter(
        $('[data-order="' + ($(selectedElement).data("order") - 1) + '"]')
      );
    $(selectedElement).removeClass("active");
    setSelected("", "");
  }

  /*** MODELS MANAGEMENT ***/


  /* Delete a model (possible only if the model is not currently selected) */
  var deleteModel = function (parameters, internalOrigin = true) {
    data.splice(
      data.findIndex((obj) => obj.id === parameters.modelID),
      1
    );
    $(
      '[data-model_id="' + parameters.modelID + '"]'
    ).remove(); /* Remove the element from the DOM */
    if (internalOrigin) {
      /* ... Send data to server ... */
      closeLeftBanner();
    } else {
      /* ... Notify the user that the model has been deleted ... */
    }
  };


  /*** TEXTURE MANAGEMENT ***/

  var addTexture = function (modelID, id, imgUrl) {
    data
      .find((item) => item.id === modelID)
      .textures.push({
        id: id,
        imgUrl: imgUrl,
      });
  };

  var deleteTexture = function (parameters, internalOrigin = true) {
    let index = data.findIndex((item) => item.id === parameters.modelID);
    data[index].textures.splice(
      data[index].textures.findIndex((item) => item.id === parameters.textureID)
    );
    /* Remove it from the view */
  };

});

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
  /* Add the model DOM to the page */
  var addModelDOM = function (order) {
    /* order is the index in of the model in the data array */
    $(".models > .row").append(
      `<div class="col-12 col-sm-6 col-lg-4 col-xl-3" data-order="${order}" data-model_id="${data[order].id}" data-model_name="${data[order].name}">
                    <div class="card">
                        <img src="${data[order].imgSrc}" class="model-img" alt="Image Model ${data[order].name}">
                        <img src="assets/img/texture.jpg" class="active-model-texture-img" alt="Active Texture Image"> 
                        <span>${data[order].name}</span>
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
  };

  /* Use this function only when an external user has created a new model */
  var addModel = function (id, name, imgSrc, textures) {
    data.push({ id: id, name: name, imgSrc: imgSrc, textures: textures });
    addModelDOM(data.length - 1);
  };

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
      closeBanner();
    } else {
      /* ... Notify the user that the model has been deleted ... */
    }
  };
  $(".banner .delete-model button").click(function () {
    let { modelID, textureID } = getSelected();
    let selectedModel = data.find(
      (item) => item.id === $(".banner").data("model_id")
    );
    if (selectedModel.id != modelID) {
      requestConfirm(
        `Are you sure you want to delete the model <b>${selectedModel.name}</b>?`,
        deleteModel,
        { modelID: selectedModel.id }
      );
    } else {
      $(".banner .header .alert")
        .html("You cannot delete a model that is currently active")
        .show();
      setTimeout(function () {
        $(".banner .header .alert").hide();
      }, 3000);
    }
  });

  var loadPage = function () {
    /* Call only when the data from the server have been loaded */
    $(".models").append('<div class="row mt-4"></div>');
    for (let order = 0; order < data.length; addModelDOM(order++));
  };
  loadPage();

  /*** TEXTURE MANAGEMENT ***/
  var addTextureDOM = function (modelID, order) {
    let texture = data.find((item) => item.id === modelID).textures[order];
    $(".banner .body > .title").after(`
                <div class="col-6 texture ${
                  isSelected(modelID, texture.id) ? "active" : ""
                }" data-id_texture="${texture.id}">
                    <span class="badge bg-secondary">Active</span>
                    <i class="fa-solid fa-trash-can"></i>
                    <img src="${texture.imgUrl}">
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

  /*** GENERAL MANAGEMENT ***/
  /* Navigation */
  $(".new-model").click(() => {
    window.location.href = "new-model.html";
  });

  /* Search filter */
  $(".search-bar input").keyup((e) => {
    /* First show all models and then hide the ones that doesn't match the input value*/
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

  /* Left banner management*/
  function closeBanner() {
    $(".banner").removeClass("active");
    $(".banner-overlay").removeClass("active");
    $(".banner-overlay, .close-banner").off("click");
    $(".banner .body .texture").remove();
  }
  function openLeftBanner(modelID) {
    /* Get selected model id*/
    let selectedModel = data.find(
      (item) => item.id === modelID
    ); /* Get all informations about the selected model */
    $(".banner").data(
      "model_id",
      selectedModel.id
    ); /* Add the selected model ID to the banner */

    /* Set banner header */
    $(".banner .header .title").html(selectedModel.name); /* Set banner title */

    /* Set banner body */
    for (
      let order = 0;
      order < selectedModel.textures.length;
      addTextureDOM(selectedModel.id, order++)
    ); /* Add the textures of the selected model */
    $(".banner").addClass("active");
    $(".banner-overlay").addClass("active");
    $(".banner-overlay, .close-banner").on("click", () => {
      closeBanner();
    });
  }

  /* Request action confirm */
  function requestConfirm(text, confirmFunction, confirmFunctionParameters) {
    $("#confirmModal .modal-body").html(text);
    $("#confirmModal").modal("show");
    $("#confirmModal .confirmButton")
      .off("click")
      .on("click", () => {
        confirmFunction(confirmFunctionParameters);
        $("#confirmModal").modal("hide");
      });
  }
});

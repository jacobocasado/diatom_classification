//========================================================================
// Archivo para configurar la insercion de la imagen en la web.
// Diseniado por Jacobo Casado de Gracia.
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Listeners de los eventos principales
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // Evitamos el comportamiento por defecto.
  // Copiadas de tutorial de JavaScript.
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // Manejar la seleccion de archivos.
  // Copiadas de tutorial de JavaScript
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

//========================================================================
// Elementos de la pagina web que se van a modificar.
//========================================================================

var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");

//========================================================================
// Eventos que ocurren cuando se pulsan los botones
//========================================================================

function submitImage() {
  // Accion cuando se le da a predecir.
  console.log("submit");

  if (!imageDisplay.src || !imageDisplay.src.startsWith("data")) {
    window.alert("Select an image before sending the data.");
    return;
  }


  // Llamamos a la funcion predict que hemos declarado en app.py 
  // con la imagen del usuario.
  predictImage(imageDisplay.src);
}

function clearImage() {
  // Reseteamos los archivos que hay en la box.
  fileSelect.value = "";

  // Borramos las imagenes y las escondemos de la vista.
  imagePreview.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  show(uploadCaption);

  imageDisplay.classList.remove("loading");
}

function previewFile(file) {
  // Cargamos la preview de la imagen.
  // No se usa al final. Se deja por si se desea usar en el futuro.
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // Reseteamos. Copiado de tutorial de JavaScript
    predResult.innerHTML = "";
    // imageDisplay.classList.remove("loading");
    
    displayImage(reader.result, "image-display");
  };
}

//========================================================================
// Funciones de ayuda. Copiadas de tutorial de Flask y JavaScript.
//========================================================================

function predictImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error happened", err.message);
      window.alert("Something unexpected happened. Try it again.");
    });
    show(loader)
}

// Mostrar imagen dado un id de imagen.
function displayImage(image, id) {
  let display = document.getElementById(id);
  display.src = image;
  // show(display);
}

// Mostrar un resultado (data) que esta oculto.
function displayResult(data) {
  // imageDisplay.classList.remove("loading");
  hide(loader);
  predResult.innerHTML = data.result;
  show(predResult);
}

// Ocultar un elemento
function hide(el) {
  el.classList.add("hidden");
}

// Mostrar un elemento
function show(el) {
  el.classList.remove("hidden");
}
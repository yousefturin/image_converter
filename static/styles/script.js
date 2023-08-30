function toggleRotation() {
  const rotationTag = document.getElementById("rotation_tag");
  rotationTag.classList.add("rotating");
}
function untoggleRotation() {
  const rotationTag = document.getElementById("rotation_tag");
  const convertImageBtnLable = document.getElementById(
    "convert_image_btn_lable"
  );
  convertImageBtnLable.style.visibility = "hidden";
  rotationTag.classList.remove("rotating");
}
function untoggleRotationOnly() {
    const rotationTag = document.getElementById('rotation_tag');
    rotationTag.classList.remove('rotating');
}

function displayDownloadBtn() {
  const downloadBtnLable = document.getElementById("download_sector_display");
  downloadBtnLable.style.display = "flex";
}




$(document).ready(function () {
  // Store the selected file format
  var selectedFileFormat = null;

  // Update the selected file format when a file is selected
  $("#file").on("change", function () {
    var fileExtension = getFileExtension(this.value);
    selectedFileFormat = "." + fileExtension;
    updateFormatSelector();
  });

  // Update the format selector list
  function updateFormatSelector() {
    // Enable all options initially
    $(".options li[data-value]").removeClass("disabled");
    $(".options li[data-value]").show();

    // Disable or hide the option matching the selected file format
    if (selectedFileFormat) {
      $(".options li[data-value='" + selectedFileFormat + "']").addClass(
        "disabled"
      );
      $(".options li[data-value='" + selectedFileFormat + "']").hide();
    }
  }
  $("#form_open").submit(function (e) {
    e.preventDefault();

    var fileInput = $("#file")[0]; // Get the file input element
    var file = fileInput.files[0]; // Get the selected file

    if (!file) {
      displayErrorMessage("Please select a file.");
      untoggleRotationOnly();
      return;
    }

    var fileExtension = getFileExtension(file.name);
    if (!isValidFormat(fileExtension)) {
      displayErrorMessage("Please select a valid image format.");
      untoggleRotationOnly();
      return;
    }
    var selectedFormat = $("#format_hidden_select").val();
    if (selectedFormat === ".default" || selectedFormat === null) {
      displayErrorMessage("Please select a format.");
      untoggleRotationOnly();
      return;
    }
    // Clear any previous error messages
    clearErrorMessage();

    var formData = new FormData(this);
    formData.append("file", file);

    var selectedFormat = $("#format_hidden_select").val();
    formData.append("selected_format", selectedFormat);
    // Add rotating animation class
    $("#rotating-icon").addClass("rotating-icon");
    $.ajax({
      url: "/upload_image",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        if (response.success) {
          untoggleRotation();
          displayDownloadBtn();
          updateHiddenInputWithImageName();
        }
      },
      error: function (xhr, status, error) {
        // Handle the error if the request fails
        console.error(error);
      },
    });
  });
  updateFormatSelector();
});

document
  .getElementById("downloadform")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    var image_name = document.getElementById("image_name").value;

    var requestData = {
      image_name: image_name,
    };

    fetch("/download_file", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Handle success, e.g., download the PDF
          var _base64 = data.data;
          // Perform your download logic here
        } else {
          // Handle error
          console.error(data.error);
        }
      })
      .catch((error) => {
        console.error("An error occurred:", error);
      });
  });

function getFileExtension(filename) {
  var regex = /(?:\.([^.]+))?$/;
  return regex.exec(filename)[1];
}

function isValidFormat(fileExtension) {
  var allowedFormats = [
    ".png",
    ".jpeg",
    ".jpg",
    ".gif",
    ".tiff",
    ".pdf",
    ".heic",
    ".bmp",
    ".svg",
    ".ico",
  ];
  return allowedFormats.includes("." + fileExtension.toLowerCase());
}
function displayErrorMessage(message) {
  var errorMessageContainer = $("#error_message");
  errorMessageContainer.text(message);
  errorMessageContainer.fadeIn(500, function () {
    setTimeout(function () {
      errorMessageContainer.fadeOut(500, function () {
        errorMessageContainer.empty();
      });
    }, 2000); // Wait for 2 seconds before fading out
  });
}

function clearErrorMessage() {
  var errorMessageContainer = $("#error_message");
  errorMessageContainer.fadeOut(500, function () {
    errorMessageContainer.empty();
  });
}
document.addEventListener('DOMContentLoaded', function () {
    const label = document.querySelector('.file-label');

    if (label) {
        label.addEventListener('click', function () {
            label.classList.toggle('clicked');
        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    const customSelect = document.getElementById('format_selector');
    const selectedOption = customSelect.querySelector('.selected-option');
    const optionsList = customSelect.querySelector('.options');
    const hiddenSelect = customSelect.querySelector('#format_hidden_select');

    selectedOption.addEventListener('click', function () {
        optionsList.style.display = optionsList.style.display === 'block' ? 'none' : 'block';
    });

    optionsList.addEventListener('click', function (e) {
        if (e.target.tagName === 'LI') {
            const selectedValue = e.target.getAttribute('data-value');
            selectedOption.textContent = e.target.textContent;
            optionsList.style.display = 'none';
            hiddenSelect.value = selectedValue;
        }
    });
});
function updateLoadingBar(percentage) {
  const loadingBar = document.getElementById("loading_bar");
  loadingBar.style.width = `${percentage}%`;
}

// Your existing code for drag and drop events
const dropZone = document.getElementById("drop_zone");

dropZone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", (event) => {
  event.preventDefault();
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropZone.classList.remove("dragover");
  const file = event.dataTransfer.files[0];
  const fileInput = document.getElementById("file");
  fileInput.files = event.dataTransfer.files;

  // New code to handle file upload and show/hide elements
  const formatSelector = document.getElementById("format_selector");
  const convertBtnLable = document.getElementById("convert_image_btn_lable");
  const downloadBtnLable = document.getElementById("download_sector_display");
  const textToText = document.getElementById("text_to_text");
  const fileNameDisplay = document.getElementById("file_name_display");
  const fileNameExtentionDisplay = document.getElementById(
    "file_name_extention_display"
  );

  if (file) {
    dropZone.classList.add("file-uploaded");
    formatSelector.style.display = "flex";
    convertBtnLable.style.display = "flex";
    textToText.style.display = "flex";
    fileNameDisplay.textContent = `Uploaded File: ${file.name}`;
    fileNameDisplay.style.display = "flex";
    fileNameExtentionDisplay.style.display = "flex";
  } else {
    dropZone.classList.remove("file-uploaded");
    formatSelector.style.display = "none";
    convertBtnLable.style.display = "none";
    downloadBtnLable.style.display = "none";
    textToText.style.display = "none";
    fileNameDisplay.style.display = "none";
    fileNameExtentionDisplay.style.display = "none";
    dropZone.querySelector("label").style.display = "flex"; // Show the label
  }
});

// New code to handle file input change event
const fileInput = document.getElementById("file");
const formatSelector = document.getElementById("format_selector");
const convertBtnLable = document.getElementById("convert_image_btn_lable");
const downloadBtnLable = document.getElementById("download_sector_display");
const fileNameDisplay = document.getElementById("file_name_display");
const textToText = document.getElementById("text_to_text");
const fileNameExtentionDisplay = document.getElementById(
  "file_name_extention_display"
);
const cancelBtn = document.getElementById("cancel_button");
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    dropZone.classList.add("file-uploaded");
    formatSelector.style.display = "flex";
    convertBtnLable.style.display = "flex";
    cancelBtn.style.display = "flex";
    textToText.style.display = "flex";
    const fileNameWithoutExtension = file.name.replace(/\.[^/.]+$/, "");
    fileNameDisplay.textContent = `${fileNameWithoutExtension}`;
    fileNameDisplay.style.display = "flex";
    const fileExtension = file.name.split(".").pop();
    fileNameExtentionDisplay.textContent = `${fileExtension}`;
    fileNameExtentionDisplay.style.display = "flex";
  } else {
    dropZone.classList.remove("file-uploaded");
    formatSelector.style.display = "none";
    convertBtnLable.style.display = "none";
    downloadBtnLable.style.display = "none";
    textToText.style.display = "none";
    cancelBtn.style.display = "none";
    fileNameDisplay.style.display = "none";
    fileNameExtentionDisplay.style.display = "none";
    dropZone.querySelector("label").style.display = "flex"; // Show the label
  }
});
cancelBtn.addEventListener("click", () => {
  // Reset the file input and hide the cancel button
  fileInput.value = "";
  cancelBtn.style.display = "none";
  formatSelector.style.display = "none";
  convertBtnLable.style.display = "none";
  downloadBtnLable.style.display = "none";
  textToText.style.display = "none";
  cancelBtn.style.display = "none";
  fileNameDisplay.style.display = "none";
  fileNameExtentionDisplay.style.display = "none";
  dropZone.classList.remove("file-uploaded");
});

// get the filename from the "src" attribute of the "image-canvas" element on first
// page load so the user if uploaded image and did nothing to it and presses download it will get the original image
const fileName = document.getElementById("file");
const formatSelectorType = document.getElementById("format_hidden_select");

function updateHiddenInputWithImageName() {
    const fileInput = document.getElementById("file");
    const formatSelector = document.getElementById("format_hidden_select");

    if (fileInput && fileInput.files.length > 0) {
        const selectedFile = fileInput.files[0];
        const imageNameWithExtension = selectedFile.name;
        const extension = imageNameWithExtension.split('.').pop();
        const imageNameWithoutExtension = imageNameWithExtension.replace('.' + extension, '');
        const formatSelectorValue = formatSelector.value;
        const fullFilename = imageNameWithoutExtension + formatSelectorValue;

        console.log(fullFilename);

        document.getElementById("image_name").value = fullFilename;
    } else {
        console.log("No file selected");
    }
}

$(document).ready(function () {
    $("#download_image_btn").click(function () {
        var imageName = $("#image_name").val();
        var downloadUrl = "/download/" + imageName;

        $.ajax({
            url: downloadUrl,
            type: "POST",
            dataType: "json",
            success: function (response) {
                if (response.success) {
                    // Decode and download the base64-encoded PDF
                    var binary = atob(response.data);
                    var array = new Uint8Array(binary.length);
                    for (var i = 0; i < binary.length; i++) {
                        array[i] = binary.charCodeAt(i);
                    }
                    var blob = new Blob([array], { type: "application/pdf" });
                    var url = window.URL.createObjectURL(blob);
                    var link = document.createElement("a");
                    link.href = url;
                    link.download = imageName;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error initiating download:", error);
            }
        });
    });
});
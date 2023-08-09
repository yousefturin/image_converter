        
        function updateLoadingBar(percentage) {
            const loadingBar = document.getElementById('loading_bar');
            loadingBar.style.width = `${percentage}%`;
        }
        
        
        // Your existing code for drag and drop events
        const dropZone = document.getElementById('drop_zone');

        dropZone.addEventListener('dragover', (event) => {
            event.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', (event) => {
            event.preventDefault();
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (event) => {
            event.preventDefault();
            dropZone.classList.remove('dragover');
            const file = event.dataTransfer.files[0];
            const fileInput = document.getElementById('file');
            fileInput.files = event.dataTransfer.files;

            // New code to handle file upload and show/hide elements
            const formatSelector = document.getElementById('format_selector');
            const convertBtnLable = document.getElementById('convert_image_btn_lable');
            const textToText = document.getElementById('text_to_text');
            
            const fileNameDisplay = document.getElementById('file_name_display');

            if (file) {
                dropZone.classList.add('file-uploaded');
                formatSelector.style.display = 'flex';
                convertBtnLable.style.display = 'flex';
                textToText.style.display = 'flex';
                fileNameDisplay.textContent = `Uploaded File: ${file.name}`;
                fileNameDisplay.style.display = 'flex';
            } else {
                dropZone.classList.remove('file-uploaded');
                formatSelector.style.display = 'none';
                convertBtnLable.style.display = 'none';
                textToText.style.display = 'none';
                fileNameDisplay.style.display = 'none';
                dropZone.querySelector('label').style.display = 'flex'; // Show the label
            }
        });

        // New code to handle file input change event
        const fileInput = document.getElementById('file');
        const formatSelector = document.getElementById('format_selector');
        const convertBtnLable = document.getElementById('convert_image_btn_lable');
        const fileNameDisplay = document.getElementById('file_name_display');
        const textToText = document.getElementById('text_to_text');
        const fileNameExtentionDisplay = document.getElementById('file_name_extention_display');

        fileInput.addEventListener('change', () => {
            const file = fileInput.files[0];
            if (file) {
                dropZone.classList.add('file-uploaded');
                formatSelector.style.display = 'flex';
                convertBtnLable.style.display = 'flex';
                textToText.style.display = 'flex';

                const fileNameWithoutExtension = file.name.replace(/\.[^/.]+$/, '');
                fileNameDisplay.textContent = `${fileNameWithoutExtension}`;
                fileNameDisplay.style.display = 'flex';
                
                const fileExtension = file.name.split('.').pop();
                fileNameExtentionDisplay.textContent = `${fileExtension}`;
                fileNameExtentionDisplay.style.display = 'flex';
            } else {
                dropZone.classList.remove('file-uploaded');
                formatSelector.style.display = 'none';
                convertBtnLable.style.display = 'none';
                textToText.style.display = 'none';
                fileNameDisplay.style.display = 'none';
                fileNameExtentionDisplay.style.display = 'none';
                dropZone.querySelector('label').style.display = 'flex'; // Show the label
            }
        });
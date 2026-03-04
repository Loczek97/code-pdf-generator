const API_BASE = 'http://localhost:8000/api';

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('code-blocks-container');
    const addBtn = document.getElementById('add-block-btn');
    const generateBtn = document.getElementById('generate-btn');
    const themeToggle = document.getElementById('theme-toggle');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const aiToggle = document.getElementById('ai-description-toggle');
    const template = document.getElementById('code-block-template');

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        document.body.classList.add('light-mode');
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }

    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        document.body.classList.toggle('light-mode');
        const isDark = document.body.classList.contains('dark-mode');
        themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    // Add Block
    addBtn.addEventListener('click', () => createBlock());

    // File Input
    dropZone.addEventListener('click', (e) => {
        if (e.target !== addBtn) fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
        fileInput.value = '';
    });

    // Drag & Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary-color)';
        dropZone.style.background = 'rgba(49, 130, 206, 0.05)';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-color)';
        dropZone.style.background = 'transparent';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-color)';
        dropZone.style.background = 'transparent';
        handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                createBlock(file.name, e.target.result);
            };
            reader.readAsText(file);
        });
    }

    function createBlock(filename = '', content = '') {
        const clone = template.content.cloneNode(true);
        const block = clone.querySelector('.code-block');
        const removeBtn = clone.querySelector('.remove-block-btn');
        const filenameInput = clone.querySelector('.filename-input');
        const editor = clone.querySelector('.code-editor');
        const langSelect = clone.querySelector('.language-select');
        const charCount = clone.querySelector('.char-count');
        const aiPreviewBtn = clone.querySelector('.ai-preview-btn');

        if (filename) filenameInput.value = filename;
        if (content) {
            editor.value = content;
            detectLanguage(content, langSelect);
            updateCharCount(editor, charCount);
        }

        removeBtn.addEventListener('click', () => {
            block.remove();
        });

        editor.addEventListener('input', () => {
            updateCharCount(editor, charCount);
        });

        editor.addEventListener('paste', (e) => {
            // Wait for paste to complete
            setTimeout(() => detectLanguage(editor.value, langSelect), 100);
        });

        if (aiToggle.checked && content) {
            // Optionally trigger AI fetch here if needed, but we do it on generate
        }

        container.appendChild(block);
    }

    function updateCharCount(editor, display) {
        display.textContent = `${editor.value.length} chars`;
    }

    async function detectLanguage(code, selectElement) {
        if (!code.trim()) return;
        try {
            const res = await fetch(`${API_BASE}/detect-language`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            const data = await res.json();
            if (data.language) {
                // Try to set the select value if it exists, otherwise Default to Text or best match
                // We rely on backend returning proper Pygments name, we might need mapping if select options differ.
                // For simplicity, we assume Pygments returns standard names like 'Python', 'Java'.
                // If not found, we keep Auto or previous.

                // Let's iterate options to find a match (case-insensitive)
                const options = Array.from(selectElement.options);
                const match = options.find(opt => opt.value.toLowerCase() === data.language.toLowerCase());
                if (match) {
                    selectElement.value = match.value;
                }
            }
        } catch (err) {
            console.error('Detection failed', err);
        }
    }

    // Generate PDF
    generateBtn.addEventListener('click', async () => {
        const blocks = document.querySelectorAll('.code-block');
        if (blocks.length === 0) {
            alert('Please add at least one code snippet.');
            return;
        }

        const items = [];
        const useAI = aiToggle.checked;
        const title = document.getElementById('doc-title').value;

        // Visual feedback
        const originalText = generateBtn.innerHTML;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        generateBtn.disabled = true;

        for (const block of blocks) {
            const filename = block.querySelector('.filename-input').value || 'Untitled';
            const code = block.querySelector('.code-editor').value;
            const language = block.querySelector('.language-select').value;

            let description = null;
            if (useAI && code.trim()) {
                try {
                    const res = await fetch(`${API_BASE}/ai-describe`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ code })
                    });
                    const data = await res.json();
                    description = data.description;
                } catch (e) {
                    console.error("AI failed", e);
                }
            }

            items.push({ filename, code, language, description });
        }

        try {
            const res = await fetch(`${API_BASE}/generate-pdf`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ items, title })
            });

            if (res.ok) {
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `code_document_${new Date().getTime()}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
            } else {
                alert('Failed to generate PDF');
            }
        } catch (err) {
            console.error(err);
            alert('Error generating PDF');
        } finally {
            generateBtn.innerHTML = originalText;
            generateBtn.disabled = false;
        }
    });

    // Start with one empty block
});

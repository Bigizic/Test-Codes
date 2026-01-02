/**
 * File Explorer JavaScript
 * Handles menu interactions, preview functionality, and keyboard shortcuts
 */

let currentPreviewPath = '';
let currentPreviewIsImage = false;

// ==================== NOTIFICATION SYSTEM ====================

/**
 * Show a Windows-style notification
 * @param {string} message - The message to display
 * @param {string} type - 'info', 'success', 'error' (default: 'info')
 * @param {number} duration - Auto-close duration in ms (0 = no auto-close, default: 5000)
 */
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const header = document.createElement('div');
    header.className = 'notification-header';
    
    const title = document.createElement('div');
    title.className = 'notification-title';
    title.textContent = type === 'error' ? 'Error' : type === 'success' ? 'Success' : 'Information';
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'notification-close';
    closeBtn.innerHTML = '×';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.onclick = () => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    };
    
    header.appendChild(title);
    header.appendChild(closeBtn);
    
    const body = document.createElement('div');
    body.className = 'notification-body';
    body.textContent = message;
    
    notification.appendChild(header);
    notification.appendChild(body);
    container.appendChild(notification);
    
    // Auto-close after duration
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    }
}

/**
 * Show a progress notification with progress bar
 * @param {string} message - The message to display
 * @param {string} operation - 'upload' or 'paste'
 * @returns {Object} - Object with updateProgress and close methods
 */
function showProgressNotification(message, operation = 'upload') {
    const container = document.getElementById('notification-container');
    if (!container) return null;
    
    const notification = document.createElement('div');
    notification.className = `notification progress ${operation}`;
    
    const header = document.createElement('div');
    header.className = 'notification-header';
    
    const title = document.createElement('div');
    title.className = 'notification-title';
    title.textContent = operation === 'upload' ? 'Uploading...' : 'Pasting...';
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'notification-close';
    closeBtn.innerHTML = '×';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.onclick = () => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    };
    
    header.appendChild(title);
    header.appendChild(closeBtn);
    
    const body = document.createElement('div');
    body.className = 'notification-body';
    body.textContent = message;
    
    const progressContainer = document.createElement('div');
    progressContainer.className = `progress-bar-container ${operation}`;
    
    const progressFill = document.createElement('div');
    progressFill.className = 'progress-bar-fill';
    progressFill.style.width = '0%';
    progressFill.textContent = '0%';
    
    const progressText = document.createElement('div');
    progressText.className = 'progress-bar-text';
    progressText.textContent = 'Starting...';
    
    progressContainer.appendChild(progressFill);
    body.appendChild(progressContainer);
    body.appendChild(progressText);
    
    notification.appendChild(header);
    notification.appendChild(body);
    container.appendChild(notification);
    
    return {
        updateProgress: (percent, statusText = '') => {
            const percentValue = Math.min(100, Math.max(0, percent));
            progressFill.style.width = percentValue + '%';
            progressFill.textContent = Math.round(percentValue) + '%';
            if (statusText) {
                progressText.textContent = statusText;
            }
        },
        close: () => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        },
        complete: (message, isSuccess = true) => {
            title.textContent = isSuccess ? 'Complete' : 'Error';
            header.className = `notification-header ${isSuccess ? 'success' : 'error'}`;
            progressFill.style.width = '100%';
            progressFill.textContent = '100%';
            progressText.textContent = message || (isSuccess ? 'Completed' : 'Failed');
            if (isSuccess) {
                setTimeout(() => {
                    notification.style.animation = 'slideOut 0.3s ease-out';
                    setTimeout(() => notification.remove(), 300);
                }, 2000);
            }
        }
    };
}

// Add slideOut animation to CSS dynamically
if (!document.getElementById('notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = `
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

document.addEventListener('DOMContentLoaded', function() {
    initializeMenus();
    initializeKeyboardShortcuts();
    initializeFileItems();
});

/**
 * Initialize menu dropdown functionality
 */
function initializeMenus() {
    const menuButtons = document.querySelectorAll('.menu-button');
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const menuItem = this.closest('.menu-item');
            const isActive = menuItem.classList.contains('active');
            
            // Close all menus
            menuItems.forEach(item => {
                item.classList.remove('active');
            });
            
            // Toggle current menu
            if (!isActive) {
                menuItem.classList.add('active');
            }
        });
    });
    
    // Close menus when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.menu-item')) {
            menuItems.forEach(item => {
                item.classList.remove('active');
            });
        }
    });
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Close modals/preview with Escape
        if (e.key === 'Escape') {
            closePreview();
            closeModal('about-modal');
            closeModal('shortcuts-modal');
            // Close menu dropdowns
            document.querySelectorAll('.menu-item').forEach(item => {
                item.classList.remove('active');
            });
        }
        
        // Go to parent folder with Backspace
        if (e.key === 'Backspace' && !e.target.matches('input, textarea')) {
            e.preventDefault();
            const currentPath = window.location.pathname;
            if (currentPath !== '/' && currentPath !== '/explorer' && currentPath !== '/explorer/') {
                const pathParts = currentPath.split('/').filter(p => p);
                if (pathParts.length > 1) {
                    pathParts.pop(); // Remove last part
                    window.location.href = '/explorer/' + pathParts.join('/');
                } else {
                    window.location.href = '/explorer';
                }
            }
        }
        
        // Go home with Home key
        if (e.key === 'Home' && !e.target.matches('input, textarea')) {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Refresh with F5
        if (e.key === 'F5') {
            e.preventDefault();
            window.location.reload();
        }
    });
}

/**
 * Initialize file item interactions
 */
function initializeFileItems() {
    const fileItems = document.querySelectorAll('.file-item');
    
    fileItems.forEach((item, index) => {
        // Add Enter key support for file items
        item.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const path = this.dataset.path;
                const isDir = this.dataset.isDir === 'true';
                const isMedia = this.dataset.isMedia === 'true';
                handleFileClick(e, path, isDir, isMedia);
            }
        });
        
        // Make items focusable for keyboard navigation
        item.setAttribute('tabindex', '0');
    });
    
    // Prevent text selection on double-click
    document.addEventListener('mousedown', function(e) {
        if (e.detail > 1) {
            e.preventDefault();
        }
    });
    
    // Add visual feedback for selected items
    let selectedItem = null;
    fileItems.forEach(item => {
        item.addEventListener('focus', function() {
            if (selectedItem) {
                selectedItem.classList.remove('selected');
            }
            this.classList.add('selected');
            selectedItem = this;
        });
    });
}

/**
 * Handle file/folder click
 */
function handleFileClick(event, path, isDir, isMedia) {
    if (isDir) {
        window.location.href = '/explorer/' + encodeURIComponent(path);
    } else {
        // For media files, show preview; for others, download
        if (isMedia) {
            const isImage = path.match(/\.(jpg|jpeg|png|gif|bmp|webp|svg|ico|tiff|tif)$/i);
            const isVideo = path.match(/\.(mp4|avi|mov|wmv|flv|webm|mkv|m4v|3gp|ogv)$/i);
            previewFile(path, !!isImage, !!isVideo);
        } else {
            window.location.href = '/download/' + encodeURIComponent(path);
        }
    }
}

/**
 * Preview an image or video file
 */
function previewFile(filepath, isImage, isVideo) {
    // Prevent multiple previews
    if (currentPreviewPath === filepath) {
        return;
    }
    
    currentPreviewPath = filepath;
    currentPreviewIsImage = isImage;
    
    const modal = document.getElementById('preview-modal');
    const previewImage = document.getElementById('preview-image');
    const previewVideo = document.getElementById('preview-video');
    const previewTitle = document.getElementById('preview-title');
    
    // Get filename for title
    const filename = filepath.split('/').pop();
    previewTitle.textContent = 'Preview: ' + filename;
    
    // Hide both initially
    previewImage.style.display = 'none';
    previewVideo.style.display = 'none';
    
    // Remove previous error handlers to prevent loops
    previewImage.onerror = null;
    previewVideo.onerror = null;
    
    // Show appropriate preview
    if (isImage) {
        previewImage.src = '/preview/' + encodeURIComponent(filepath);
        previewImage.style.display = 'block';
        previewImage.onerror = function() {
            // Only handle error once
            this.onerror = null;
            showNotification('Failed to load image preview: ' + filename, 'error');
            closePreview();
        };
    } else if (isVideo) {
        previewVideo.src = '/preview/' + encodeURIComponent(filepath);
        previewVideo.style.display = 'block';
        previewVideo.load();
        previewVideo.onerror = function() {
            // Only handle error once
            this.onerror = null;
            showNotification('Failed to load video preview: ' + filename, 'error');
            closePreview();
        };
    }
    
    modal.classList.add('show');
}

/**
 * Close preview modal
 */
function closePreview() {
    const modal = document.getElementById('preview-modal');
    const previewImage = document.getElementById('preview-image');
    const previewVideo = document.getElementById('preview-video');
    
    modal.classList.remove('show');
    previewImage.src = '';
    previewVideo.src = '';
    previewVideo.pause();
    currentPreviewPath = '';
}

/**
 * Download the currently previewed file
 */
function downloadPreview() {
    if (currentPreviewPath) {
        window.location.href = '/download/' + encodeURIComponent(currentPreviewPath);
    }
}

/**
 * Close a modal by ID
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

/**
 * Menu functions
 */

function selectAll() {
    // Select all file items (visual feedback)
    const fileItems = document.querySelectorAll('.file-item');
    fileItems.forEach(item => {
        item.classList.add('selected');
    });
    // Close menu
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
}

function copyPath() {
    const currentPath = window.location.pathname;
    let pathToCopy = '';
    
    if (currentPath === '/' || currentPath === '/browse' || currentPath === '/browse/') {
        pathToCopy = window.location.origin + '/';
    } else {
        pathToCopy = window.location.href;
    }
    
    // Try to copy to clipboard
    if (navigator.clipboard) {
        navigator.clipboard.writeText(pathToCopy).then(() => {
            // No notification for copy operations as per requirements
        }).catch(() => {
            // Fallback for older browsers
            prompt('Copy this path:', pathToCopy);
        });
    } else {
        // Fallback
        prompt('Copy this path:', pathToCopy);
    }
    
    // Close menu
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
}

function setViewMode(mode) {
    const listView = document.getElementById('list-view');
    const gridView = document.getElementById('grid-view');
    const listOption = document.getElementById('view-list-option');
    const gridOption = document.getElementById('view-grid-option');
    
    if (mode === 'grid') {
        if (listView) listView.style.display = 'none';
        if (gridView) gridView.style.display = 'grid';
        if (listOption) listOption.classList.remove('active');
        if (gridOption) gridOption.classList.add('active');
        localStorage.setItem('fileViewMode', 'grid');
    } else {
        if (listView) listView.style.display = 'table';
        if (gridView) gridView.style.display = 'none';
        if (listOption) listOption.classList.add('active');
        if (gridOption) gridOption.classList.remove('active');
        localStorage.setItem('fileViewMode', 'list');
    }
    
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
}

function closeApplication() {
    // Navigate to home and replace history
    window.location.replace('/');
}

// Load saved view mode on page load
document.addEventListener('DOMContentLoaded', function() {
    // Only set view mode if we're on the file explorer page
    const listView = document.getElementById('list-view');
    if (listView) {
        const savedViewMode = localStorage.getItem('fileViewMode') || 'list';
        setViewMode(savedViewMode);
        
        // Add right-click support for grid items
        const gridItems = document.querySelectorAll('.grid-item');
        gridItems.forEach(item => {
            item.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const path = this.dataset.path;
                const isDir = this.dataset.isDir === 'true';
                showContextMenu(e, path, isDir);
            });
        });
    }
});

function showHiddenFiles() {
    // This would require backend changes to show hidden files
    showNotification('Hidden files feature - modify app.py to show files starting with "."', 'info');
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
}

function showAbout() {
    const modal = document.getElementById('about-modal');
    modal.classList.add('show');
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
}

function showShortcuts() {
    const modal = document.getElementById('shortcuts-modal');
    modal.classList.add('show');
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
}

// Close modals when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        closePreview();
        closeModal('about-modal');
        closeModal('shortcuts-modal');
        closeModal('upload-modal');
        closeModal('create-file-modal');
        closeModal('create-folder-modal');
    }
});

// ==================== CONTEXT MENU ====================

let contextMenu = null;
let contextMenuTarget = null;
let currentContextPath = '';

document.addEventListener('DOMContentLoaded', function() {
    contextMenu = document.getElementById('context-menu');
    
    // Right-click on file list container
    const fileListContainer = document.getElementById('file-list-container');
    if (fileListContainer) {
        fileListContainer.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            showContextMenu(e, '', true);
        });
    }
    
    // Right-click on file items
    document.addEventListener('contextmenu', function(e) {
        const fileItem = e.target.closest('.file-item');
        if (fileItem) {
            e.preventDefault();
            const path = fileItem.dataset.path;
            const isDir = fileItem.dataset.isDir === 'true';
            showContextMenu(e, path, isDir);
        }
    });
    
    // Hide context menu on click
    document.addEventListener('click', function() {
        hideContextMenu();
    });
    
    // Context menu actions
    document.getElementById('ctx-upload-file').addEventListener('click', function() {
        showUploadModal();
        hideContextMenu();
    });
    
    document.getElementById('ctx-create-file').addEventListener('click', function() {
        showCreateFileModal();
        hideContextMenu();
    });
    
    document.getElementById('ctx-create-folder').addEventListener('click', function() {
        showCreateFolderModal();
        hideContextMenu();
    });
    
    document.getElementById('ctx-delete').addEventListener('click', function() {
        deleteFileOrFolder(currentContextPath);
        hideContextMenu();
    });
    
    // Form submissions
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleUpload);
    }
    
    const createFileForm = document.getElementById('create-file-form');
    if (createFileForm) {
        createFileForm.addEventListener('submit', handleCreateFile);
    }
    
    const createFolderForm = document.getElementById('create-folder-form');
    if (createFolderForm) {
        createFolderForm.addEventListener('submit', handleCreateFolder);
    }
});

function showContextMenu(e, path, isDir) {
    if (!contextMenu) return;
    
    currentContextPath = path;
    const deleteOption = document.getElementById('ctx-delete');
    const pasteOption = document.getElementById('ctx-paste');
    const clipboard = getClipboard();
    
    // Show/hide delete option based on whether an item is selected
    if (path) {
        if (deleteOption) deleteOption.style.display = 'block';
    } else {
        if (deleteOption) deleteOption.style.display = 'none';
    }
    
    // Show/hide paste option based on clipboard
    if (pasteOption) {
        pasteOption.style.display = clipboard ? 'block' : 'none';
    }
    
    // Position context menu
    contextMenu.style.display = 'block';
    contextMenu.style.left = e.pageX + 'px';
    contextMenu.style.top = e.pageY + 'px';
    
    // Keep menu within viewport
    const rect = contextMenu.getBoundingClientRect();
    if (rect.right > window.innerWidth) {
        contextMenu.style.left = (e.pageX - rect.width) + 'px';
    }
    if (rect.bottom > window.innerHeight) {
        contextMenu.style.top = (e.pageY - rect.height) + 'px';
    }
}

function hideContextMenu() {
    if (contextMenu) {
        contextMenu.style.display = 'none';
    }
}

function showUploadModal() {
    const modal = document.getElementById('upload-modal');
    const container = document.getElementById('file-list-container');
    const currentPath = container ? container.dataset.currentPath || '' : '';
    document.getElementById('upload-directory').value = currentPath;
    modal.classList.add('show');
}

function showCreateFileModal() {
    const modal = document.getElementById('create-file-modal');
    const container = document.getElementById('file-list-container');
    const currentPath = container ? container.dataset.currentPath || '' : '';
    document.getElementById('create-file-directory').value = currentPath;
    document.getElementById('filename-input').value = '';
    document.getElementById('file-content-input').value = '';
    modal.classList.add('show');
}

function showCreateFolderModal() {
    const modal = document.getElementById('create-folder-modal');
    const container = document.getElementById('file-list-container');
    const currentPath = container ? container.dataset.currentPath || '' : '';
    document.getElementById('create-folder-directory').value = currentPath;
    document.getElementById('foldername-input').value = '';
    modal.classList.add('show');
}

function handleUpload(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const fileInput = form.querySelector('#file-input');
    const file = fileInput ? fileInput.files[0] : null;
    
    if (!file) {
        showNotification('No file selected', 'error');
        return;
    }
    
    const progressNotif = showProgressNotification(`Uploading: ${file.name}`, 'upload');
    if (!progressNotif) {
        showNotification('Failed to initialize progress notification', 'error');
        return;
    }
    
    const xhr = new XMLHttpRequest();
    
    // Track upload progress
    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percent = (e.loaded / e.total) * 100;
            progressNotif.updateProgress(percent, `Uploading: ${Math.round(percent)}%`);
        }
    });
    
    xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
            try {
                const data = JSON.parse(xhr.responseText);
                if (data.success) {
                    progressNotif.complete(data.message, true);
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    progressNotif.complete('Error: ' + data.error, false);
                }
            } catch (error) {
                progressNotif.complete('Error parsing response: ' + error, false);
            }
        } else {
            progressNotif.complete('Upload failed with status: ' + xhr.status, false);
        }
    });
    
    xhr.addEventListener('error', () => {
        progressNotif.complete('Error uploading file', false);
    });
    
    xhr.addEventListener('abort', () => {
        progressNotif.complete('Upload cancelled', false);
    });
    
    xhr.open('POST', '/upload');
    xhr.send(formData);
}

function handleCreateFile(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    fetch('/create_file', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            closeModal('create-file-modal');
            window.location.reload();
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        showNotification('Error creating file: ' + error, 'error');
    });
}

function handleCreateFolder(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    fetch('/create_folder', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            closeModal('create-folder-modal');
            window.location.reload();
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        showNotification('Error creating folder: ' + error, 'error');
    });
}

function deleteFileOrFolder(path) {
    if (!path) return;
    
    const itemName = path.split('/').pop();
    if (!confirm(`Are you sure you want to delete "${itemName}"?`)) {
        return;
    }
    
    const formData = new FormData();
    formData.append('filepath', path);
    
    fetch('/delete', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            window.location.reload();
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    })
    .catch(error => {
        showNotification('Error deleting: ' + error, 'error');
    });
}

// ==================== FILE OPTIONS MENU ====================

let currentFileOptionsPath = '';
let currentFileOptionsIsDir = false;

function showFileOptions(event, path, isDir) {
    event.stopPropagation();
    currentFileOptionsPath = path;
    currentFileOptionsIsDir = isDir;
    
    const menu = document.getElementById('file-options-menu');
    if (!menu) return;
    
    // Show/hide paste option based on clipboard
    const pasteOption = document.getElementById('opt-paste');
    const clipboard = getClipboard();
    if (pasteOption) {
        pasteOption.style.display = clipboard ? 'block' : 'none';
    }
    
    // Position menu
    menu.style.display = 'block';
    menu.style.left = event.pageX + 'px';
    menu.style.top = event.pageY + 'px';
    
    // Keep menu within viewport
    const rect = menu.getBoundingClientRect();
    if (rect.right > window.innerWidth) {
        menu.style.left = (event.pageX - rect.width) + 'px';
    }
    if (rect.bottom > window.innerHeight) {
        menu.style.top = (event.pageY - rect.height) + 'px';
    }
}

function hideFileOptionsMenu() {
    const menu = document.getElementById('file-options-menu');
    if (menu) {
        menu.style.display = 'none';
    }
}

// Clipboard management
function getClipboard() {
    const data = sessionStorage.getItem('fileClipboard');
    return data ? JSON.parse(data) : null;
}

function setClipboard(filepath, operation) {
    const data = { filepath, operation, timestamp: Date.now() };
    sessionStorage.setItem('fileClipboard', JSON.stringify(data));
    updateClipboardIndicator();
}

function clearClipboard() {
    sessionStorage.removeItem('fileClipboard');
    updateClipboardIndicator();
}

function updateClipboardIndicator() {
    const indicator = document.getElementById('clipboard-indicator');
    const text = document.getElementById('clipboard-text');
    const clipboard = getClipboard();
    
    if (clipboard && indicator && text) {
        const itemName = clipboard.filepath.split('/').pop();
        const operation = clipboard.operation === 'cut' ? 'Cut' : 'Copied';
        text.textContent = `${operation}: ${itemName}`;
        indicator.style.display = 'flex';
    } else if (indicator) {
        indicator.style.display = 'none';
    }
}

// File operations
function renameFile(path) {
    const itemName = path.split('/').pop();
    const modal = document.getElementById('rename-modal');
    const input = document.getElementById('rename-input');
    const filepathInput = document.getElementById('rename-filepath');
    
    if (modal && input && filepathInput) {
        filepathInput.value = path;
        input.value = itemName;
        input.select();
        modal.classList.add('show');
    }
    hideFileOptionsMenu();
}

function copyFile(path) {
    setClipboard(path, 'copy');
    hideFileOptionsMenu();
    // No notification for copy operations as per requirements
}

function cutFile(path) {
    setClipboard(path, 'cut');
    hideFileOptionsMenu();
    // No notification for cut operations as per requirements
}

function pasteFile(targetDir) {
    const clipboard = getClipboard();
    if (!clipboard) {
        showNotification('Nothing in clipboard', 'error');
        return;
    }
    
    const itemName = clipboard.filepath.split('/').pop();
    const operation = clipboard.operation === 'cut' ? 'Moving' : 'Copying';
    const progressNotif = showProgressNotification(`${operation}: ${itemName}`, 'paste');
    
    if (!progressNotif) {
        showNotification('Failed to initialize progress notification', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('source_path', clipboard.filepath);
    formData.append('target_dir', targetDir || '');
    formData.append('operation', clipboard.operation);
    
    // Simulate progress for paste operation
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress < 90) {
            progressNotif.updateProgress(progress, `${operation} files...`);
        }
    }, 200);
    
    fetch('/paste', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        if (data.success) {
            progressNotif.complete(data.message, true);
            if (clipboard.operation === 'cut') {
                clearClipboard();
            }
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            progressNotif.complete('Error: ' + data.error, false);
        }
    })
    .catch(error => {
        clearInterval(progressInterval);
        progressNotif.complete('Error pasting: ' + error, false);
    });
    hideFileOptionsMenu();
}

function moveFile(path) {
    const modal = document.getElementById('move-modal');
    const filepathInput = document.getElementById('move-filepath');
    const targetInput = document.getElementById('move-target-input');
    
    if (modal && filepathInput && targetInput) {
        filepathInput.value = path;
        targetInput.value = '';
        modal.classList.add('show');
    }
    hideFileOptionsMenu();
}

// Initialize file options menu
document.addEventListener('DOMContentLoaded', function() {
    // File options menu handlers
    const optRename = document.getElementById('opt-rename');
    const optCopy = document.getElementById('opt-copy');
    const optCut = document.getElementById('opt-cut');
    const optPaste = document.getElementById('opt-paste');
    const optMove = document.getElementById('opt-move');
    const optDelete = document.getElementById('opt-delete');
    
    if (optRename) {
        optRename.addEventListener('click', function() {
            renameFile(currentFileOptionsPath);
        });
    }
    
    if (optCopy) {
        optCopy.addEventListener('click', function() {
            copyFile(currentFileOptionsPath);
        });
    }
    
    if (optCut) {
        optCut.addEventListener('click', function() {
            cutFile(currentFileOptionsPath);
        });
    }
    
    if (optPaste) {
        optPaste.addEventListener('click', function() {
            const container = document.getElementById('file-list-container');
            const currentPath = container ? container.dataset.currentPath || '' : '';
            pasteFile(currentPath);
        });
    }
    
    if (optMove) {
        optMove.addEventListener('click', function() {
            moveFile(currentFileOptionsPath);
        });
    }
    
    if (optDelete) {
        optDelete.addEventListener('click', function() {
            deleteFileOrFolder(currentFileOptionsPath);
            hideFileOptionsMenu();
        });
    }
    
    // Hide menu on click outside
    document.addEventListener('click', function() {
        hideFileOptionsMenu();
    });
    
    // Rename form handler
    const renameForm = document.getElementById('rename-form');
    if (renameForm) {
        renameForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(renameForm);
            
            fetch('/rename', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    closeModal('rename-modal');
                    window.location.reload();
                } else {
                    showNotification('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showNotification('Error renaming: ' + error, 'error');
            });
        });
    }
    
    // Move form handler
    const moveForm = document.getElementById('move-form');
    if (moveForm) {
        moveForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(moveForm);
            
            fetch('/move', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(data.message, 'success');
                    closeModal('move-modal');
                    window.location.reload();
                } else {
                    showNotification('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showNotification('Error moving: ' + error, 'error');
            });
        });
    }
    
    // Update clipboard indicator on load
    updateClipboardIndicator();
    
    // Add paste option to context menu
    const ctxPaste = document.getElementById('ctx-paste');
    if (ctxPaste) {
        ctxPaste.addEventListener('click', function() {
            const container = document.getElementById('file-list-container');
            const currentPath = container ? container.dataset.currentPath || '' : '';
            pasteFile(currentPath);
        });
    }
    
    // Update context menu paste visibility
    const updateContextMenu = function() {
        const clipboard = getClipboard();
        if (ctxPaste) {
            ctxPaste.style.display = clipboard ? 'block' : 'none';
        }
    };
    updateContextMenu();
    setInterval(updateContextMenu, 500);
});

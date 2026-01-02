#!/usr/bin/env python3
"""
Flask File Explorer Web App
A simple, offline file browser with retro UI styling.
"""

import os
import urllib.parse
import mimetypes
from datetime import datetime
from flask import Flask, render_template, send_file, abort, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import shutil
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load MySQL configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_NAME = os.getenv('DB_NAME', 'file_explorer_db')
DB_USER = os.getenv('DB_USER', 'file_explorer_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'PASSWORD_password_0000')


def get_db_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Configuration: Set the root directory for browsing
# Change this to the directory you want to browse
ROOT_DIRECTORY = os.path.expanduser("~")  # Default: user's home directory

# Allowed file extensions for direct viewing (optional - can be expanded)
VIEWABLE_EXTENSIONS = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.log'}

# Image and video extensions for preview
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif'}
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.3gp', '.ogv'}


def is_safe_path(basedir, path):
    """
    Security check to prevent directory traversal attacks.
    Ensures the requested path is within the allowed root directory.
    """
    # Resolve both paths to absolute paths
    basedir = os.path.abspath(basedir)
    path = os.path.abspath(path)
    
    # Check if the resolved path starts with the base directory
    return path.startswith(basedir)


def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_file_info(file_path):
    """Get file information (name, type, size, modified date)."""
    stat = os.stat(file_path)
    
    file_ext = os.path.splitext(file_path)[1].lower()
    is_image = file_ext in IMAGE_EXTENSIONS
    is_video = file_ext in VIDEO_EXTENSIONS
    is_media = is_image or is_video
    
    info = {
        'name': os.path.basename(file_path),
        'is_dir': os.path.isdir(file_path),
        'size': format_file_size(stat.st_size) if os.path.isfile(file_path) else '-',
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'path': file_path,
        'extension': file_ext,
        'is_image': is_image,
        'is_video': is_video,
        'is_media': is_media
    }
    
    return info


@app.route('/')
def index():
    """Homepage with File Explorer and Notes options."""
    return render_template('home.html')


@app.route('/explorer')
@app.route('/explorer/')
@app.route('/explorer/<path:subpath>')
def explorer(subpath=''):
    """
    Browse a directory. Shows files and folders.
    Security: Validates path to prevent directory traversal.
    """
    # Decode the path
    if subpath:
        # Remove leading slash if present
        subpath = subpath.lstrip('/')
        # Decode URL-encoded path
        subpath = urllib.parse.unquote(subpath)
    
    # Construct the full path
    if subpath:
        full_path = os.path.join(ROOT_DIRECTORY, subpath)
    else:
        full_path = ROOT_DIRECTORY
    
    # Security check: ensure path is within allowed root
    if not is_safe_path(ROOT_DIRECTORY, full_path):
        abort(403)  # Forbidden
    
    # Check if path exists
    if not os.path.exists(full_path):
        abort(404)  # Not found
    
    # Check if it's a directory
    if not os.path.isdir(full_path):
        # If it's a file, redirect to download
        return download(subpath)
    
    # Get directory contents
    try:
        items = []
        entries = sorted(os.listdir(full_path), key=lambda x: (not os.path.isdir(os.path.join(full_path, x)), x.lower()))
        
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            # Skip hidden files/folders (optional - remove if you want to show them)
            if entry.startswith('.'):
                continue
            
            item_info = get_file_info(entry_path)
            # Calculate relative path from root for navigation
            if subpath:
                item_info['relative_path'] = os.path.join(subpath, entry).replace('\\', '/')
            else:
                item_info['relative_path'] = entry
            items.append(item_info)
        
        # Build breadcrumb navigation
        breadcrumbs = [{'name': 'Home', 'path': ''}]
        if subpath:
            parts = subpath.split(os.sep)
            current_path = ''
            for part in parts:
                if part:
                    current_path = os.path.join(current_path, part) if current_path else part
                    breadcrumbs.append({
                        'name': part,
                        'path': current_path.replace('\\', '/')  # Use forward slashes for URLs
                    })
        
        return render_template('index.html', 
                             items=items, 
                             current_path=subpath,
                             breadcrumbs=breadcrumbs,
                             root_dir=ROOT_DIRECTORY)
    
    except PermissionError:
        abort(403)  # Forbidden - no permission to read directory
    except Exception as e:
        abort(500)  # Internal server error


# Alias route for backward compatibility
@app.route('/browse')
@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse(subpath=''):
    """Alias route for /explorer for backward compatibility."""
    return explorer(subpath)


@app.route('/preview')
@app.route('/preview/<path:filepath>')
def preview(filepath=''):
    """
    Preview an image or video file.
    Security: Validates path to prevent directory traversal.
    """
    if not filepath:
        abort(400)  # Bad request
    
    # Decode URL-encoded path
    filepath = urllib.parse.unquote(filepath)
    
    # Construct the full path
    full_path = os.path.join(ROOT_DIRECTORY, filepath)
    
    # Security check: ensure path is within allowed root
    if not is_safe_path(ROOT_DIRECTORY, full_path):
        abort(403)  # Forbidden
    
    # Check if file exists
    if not os.path.exists(full_path):
        abort(404)  # Not found
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(full_path):
        abort(400)  # Bad request - not a file
    
    # Check if it's a media file
    file_ext = os.path.splitext(full_path)[1].lower()
    if file_ext not in IMAGE_EXTENSIONS and file_ext not in VIDEO_EXTENSIONS:
        abort(400)  # Bad request - not a previewable media file
    
    try:
        # Detect MIME type automatically
        mimetype, _ = mimetypes.guess_type(full_path)
        if not mimetype:
            # Fallback MIME types
            if file_ext in IMAGE_EXTENSIONS:
                mimetype = 'image/jpeg' if file_ext in ['.jpg', '.jpeg'] else f'image/{file_ext[1:]}'
            elif file_ext in VIDEO_EXTENSIONS:
                mimetype = 'video/mp4' if file_ext == '.mp4' else f'video/{file_ext[1:]}'
        
        return send_file(full_path, mimetype=mimetype)
    except Exception as e:
        abort(500)  # Internal server error


@app.route('/download')
@app.route('/download/<path:filepath>')
def download(filepath=''):
    """
    Download a file.
    Security: Validates path to prevent directory traversal.
    """
    if not filepath:
        abort(400)  # Bad request
    
    # Decode URL-encoded path
    filepath = urllib.parse.unquote(filepath)
    
    # Construct the full path
    full_path = os.path.join(ROOT_DIRECTORY, filepath)
    
    # Security check: ensure path is within allowed root
    if not is_safe_path(ROOT_DIRECTORY, full_path):
        abort(403)  # Forbidden
    
    # Check if file exists
    if not os.path.exists(full_path):
        abort(404)  # Not found
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(full_path):
        abort(400)  # Bad request - not a file
    
    try:
        return send_file(full_path, as_attachment=True)
    except Exception as e:
        abort(500)  # Internal server error


# ==================== FILE OPERATIONS ====================

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to the current directory."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    target_dir = request.form.get('directory', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Construct target directory path
    if target_dir:
        target_dir = urllib.parse.unquote(target_dir)
        target_path = os.path.join(ROOT_DIRECTORY, target_dir)
    else:
        target_path = ROOT_DIRECTORY
    
    # Security check
    if not is_safe_path(ROOT_DIRECTORY, target_path):
        return jsonify({'error': 'Invalid directory'}), 403
    
    # Check if target is a directory
    if not os.path.isdir(target_path):
        return jsonify({'error': 'Target is not a directory'}), 400
    
    try:
        # Secure filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(target_path, filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            return jsonify({'error': 'File already exists'}), 400
        
        # Save file
        file.save(file_path)
        return jsonify({'success': True, 'message': f'File {filename} uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create_file', methods=['POST'])
def create_file():
    """Create a new empty file."""
    filename = request.form.get('filename', '').strip()
    target_dir = request.form.get('directory', '')
    content = request.form.get('content', '')
    
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400
    
    # Construct target directory path
    if target_dir:
        target_dir = urllib.parse.unquote(target_dir)
        target_path = os.path.join(ROOT_DIRECTORY, target_dir)
    else:
        target_path = ROOT_DIRECTORY
    
    # Security check
    if not is_safe_path(ROOT_DIRECTORY, target_path):
        return jsonify({'error': 'Invalid directory'}), 403
    
    # Check if target is a directory
    if not os.path.isdir(target_path):
        return jsonify({'error': 'Target is not a directory'}), 400
    
    try:
        # Secure filename
        filename = secure_filename(filename)
        file_path = os.path.join(target_path, filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            return jsonify({'error': 'File already exists'}), 400
        
        # Create file with content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({'success': True, 'message': f'File {filename} created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create_folder', methods=['POST'])
def create_folder():
    """Create a new folder."""
    foldername = request.form.get('foldername', '').strip()
    target_dir = request.form.get('directory', '')
    
    if not foldername:
        return jsonify({'error': 'Folder name is required'}), 400
    
    # Construct target directory path
    if target_dir:
        target_dir = urllib.parse.unquote(target_dir)
        target_path = os.path.join(ROOT_DIRECTORY, target_dir)
    else:
        target_path = ROOT_DIRECTORY
    
    # Security check
    if not is_safe_path(ROOT_DIRECTORY, target_path):
        return jsonify({'error': 'Invalid directory'}), 403
    
    # Check if target is a directory
    if not os.path.isdir(target_path):
        return jsonify({'error': 'Target is not a directory'}), 400
    
    try:
        # Secure foldername
        foldername = secure_filename(foldername)
        folder_path = os.path.join(target_path, foldername)
        
        # Check if folder already exists
        if os.path.exists(folder_path):
            return jsonify({'error': 'Folder already exists'}), 400
        
        # Create folder
        os.makedirs(folder_path, exist_ok=False)
        
        return jsonify({'success': True, 'message': f'Folder {foldername} created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete', methods=['POST'])
def delete_file():
    """Delete a file or folder."""
    filepath = request.form.get('filepath', '')
    
    if not filepath:
        return jsonify({'error': 'File path is required'}), 400
    
    # Decode URL-encoded path
    filepath = urllib.parse.unquote(filepath)
    
    # Construct full path
    full_path = os.path.join(ROOT_DIRECTORY, filepath)
    
    # Security check
    if not is_safe_path(ROOT_DIRECTORY, full_path):
        return jsonify({'error': 'Invalid path'}), 403
    
    # Check if path exists
    if not os.path.exists(full_path):
        return jsonify({'error': 'File or folder does not exist'}), 404
    
    try:
        if os.path.isdir(full_path):
            # Delete folder recursively
            shutil.rmtree(full_path)
            return jsonify({'success': True, 'message': 'Folder deleted successfully'})
        else:
            # Delete file
            os.remove(full_path)
            return jsonify({'success': True, 'message': 'File deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors."""
    return render_template('error.html', 
                         error_code=403, 
                         error_message="Access Forbidden"), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="File or Directory Not Found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal Server Error"), 500


# ==================== NOTES ROUTES ====================

@app.route('/notes')
def notes_list():
    """Display all notes."""
    connection = get_db_connection()
    if not connection:
        return render_template('notes.html', notes=[], error="Database connection failed")
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
        notes = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('notes.html', notes=notes, error=None)
    except Error as e:
        if connection:
            connection.close()
        return render_template('notes.html', notes=[], error=f"Error fetching notes: {str(e)}")


@app.route('/notes/create', methods=['GET', 'POST'])
def create_note():
    """Create a new note."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO notes (title, content) VALUES (%s, %s)",
                (title, content)
            )
            connection.commit()
            note_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return redirect(url_for('notes_list'))
        except Error as e:
            if connection:
                connection.close()
            return jsonify({'error': str(e)}), 500
    
    return render_template('note_edit.html', note=None)


@app.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    """Edit an existing note."""
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', 
                             error_code=500, 
                             error_message="Database connection failed"), 500
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE notes SET title = %s, content = %s WHERE id = %s",
                (title, content, note_id)
            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('notes_list'))
        except Error as e:
            if connection:
                connection.close()
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message=f"Error updating note: {str(e)}"), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
        note = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not note:
            abort(404)
        
        return render_template('note_edit.html', note=note)
    except Error as e:
        if connection:
            connection.close()
        return render_template('error.html', 
                             error_code=500, 
                             error_message=f"Error fetching note: {str(e)}"), 500


@app.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """Delete a note."""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('notes_list'))
    except Error as e:
        if connection:
            connection.close()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Load server configuration from environment variables
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("Flask File Explorer")
    print("=" * 60)
    print(f"Root directory: {ROOT_DIRECTORY}")
    print(f"Database: {DB_NAME} @ {DB_HOST}:{DB_PORT}")
    print(f"Server starting on http://{SERVER_HOST}:{SERVER_PORT}")
    print("\nTo access from another device:")
    print("1. Find your machine's IP address: hostname -I")
    print(f"2. Open http://<your-ip>:{SERVER_PORT} in a browser")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the Flask app
    # Bind to 0.0.0.0 to allow access from other devices on the network
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=FLASK_DEBUG)


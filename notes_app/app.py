#!/usr/bin/env python3
"""
Flask File Explorer Web App
A simple, offline file browser with retro UI styling.
"""

import os
import urllib.parse
import mimetypes
import stat
import platform
from datetime import datetime
from flask import Flask, render_template, send_file, abort, request, jsonify, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import shutil
import json
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Session configuration for authentication
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24).hex())

# Check if we're in production mode
FLASK_ENV = os.getenv('FLASK_ENV', 'development').lower()
IS_PRODUCTION = FLASK_ENV == 'production'

# Authentication password from .env
AUTH_PASSWORD = os.getenv('AUTH_PASSWORD', '')

# Passkey authentication mode
USE_PASS_KEY = os.getenv('USE_PASS_KEY', 'false').lower() == 'true'

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


def ensure_users_table():
    """Ensure the users table exists in the database."""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                passkey VARCHAR(255) NOT NULL,
                has_passkey BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_username (username),
                INDEX idx_has_passkey (has_passkey)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error creating users table: {e}")
        if connection:
            connection.close()
        return False

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


# ==================== AUTHENTICATION GUARD ====================

def is_authenticated():
    """Check if user is authenticated."""
    return session.get('authenticated', False) == True


def has_users_with_passkey():
    """Check if any users with passkey exist in the database."""
    if not USE_PASS_KEY:
        return False
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE has_passkey = TRUE")
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count > 0
    except Error as e:
        print(f"Error checking users with passkey: {e}")
        if connection:
            connection.close()
        return False


def verify_passkey(username, passkey):
    """Verify passkey for a user."""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND has_passkey = TRUE",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if user and user['passkey'] == passkey:
            return True
        return False
    except Error as e:
        print(f"Error verifying passkey: {e}")
        if connection:
            connection.close()
        return False


def create_user_with_passkey(username, passkey):
    """Create a new user with passkey (SSO signup)."""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, passkey, has_passkey) VALUES (%s, %s, TRUE)",
            (username, passkey)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error creating user: {e}")
        if connection:
            connection.close()
        return False


def require_auth(f):
    """Decorator to require authentication in production mode."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if IS_PRODUCTION and not is_authenticated():
            # Allow access to login and static files
            if request.endpoint in ['login', 'static', 'authenticate']:
                return f(*args, **kwargs)
            # Redirect to login for all other routes
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def authenticate_guard():
    """Guard that checks authentication before every request in production."""
    if IS_PRODUCTION:
        # Allow access to login, authenticate, logout, sso_signup, sso_create, and static files without authentication
        if request.endpoint in ['login', 'authenticate', 'logout', 'sso_signup', 'sso_create', 'static']:
            return None
        
        # Check if user is authenticated
        if not is_authenticated():
            # Redirect to login page, preserving the intended destination
            return redirect(url_for('login', next=request.url))


@app.route('/login')
def login():
    """Login page."""
    # If already authenticated, redirect to home
    if is_authenticated():
        next_url = request.args.get('next', url_for('index'))
        return redirect(next_url)
    
    # Check if passkey mode is enabled
    use_passkey = USE_PASS_KEY
    has_users = has_users_with_passkey() if use_passkey else False
    
    return render_template('login.html', 
                         next_url=request.args.get('next', url_for('index')),
                         use_passkey=use_passkey,
                         has_users=has_users)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Handle authentication."""
    next_url = request.form.get('next', url_for('index'))
    
    # Check if passkey mode is enabled
    if USE_PASS_KEY:
        username = request.form.get('username', '').strip()
        passkey = request.form.get('passkey', '')
        
        if not username or not passkey:
            flash('Username and passkey are required.', 'error')
            return redirect(url_for('login', next=next_url))
        
        # Verify passkey
        if verify_passkey(username, passkey):
            session['authenticated'] = True
            session['username'] = username
            return redirect(next_url)
        else:
            flash('Invalid username or passkey. Please try again.', 'error')
            return redirect(url_for('login', next=next_url))
    else:
        # Traditional password authentication
        password = request.form.get('password', '')
        
        if password == AUTH_PASSWORD and AUTH_PASSWORD:
            session['authenticated'] = True
            return redirect(next_url)
        else:
            flash('Invalid password. Please try again.', 'error')
            return redirect(url_for('login', next=next_url))


@app.route('/sso_signup')
def sso_signup():
    """SSO signup page for creating the first user with passkey."""
    # Only allow if passkey mode is enabled and no users exist
    if not USE_PASS_KEY:
        return redirect(url_for('login'))
    
    if has_users_with_passkey():
        flash('Users already exist. Please login instead.', 'error')
        return redirect(url_for('login'))
    
    return render_template('sso_signup.html')


@app.route('/sso_create', methods=['POST'])
def sso_create():
    """Create first user with passkey (SSO signup)."""
    if not USE_PASS_KEY:
        return redirect(url_for('login'))
    
    if has_users_with_passkey():
        flash('Users already exist. Please login instead.', 'error')
        return redirect(url_for('login'))
    
    username = request.form.get('username', '').strip()
    passkey = request.form.get('passkey', '')
    confirm_passkey = request.form.get('confirm_passkey', '')
    
    # Validation
    if not username:
        flash('Username is required.', 'error')
        return redirect(url_for('sso_signup'))
    
    if not passkey or len(passkey) < 6:
        flash('Passkey must be at least 6 characters long.', 'error')
        return redirect(url_for('sso_signup'))
    
    if passkey != confirm_passkey:
        flash('Passkeys do not match.', 'error')
        return redirect(url_for('sso_signup'))
    
    # Create user
    if create_user_with_passkey(username, passkey):
        session['authenticated'] = True
        session['username'] = username
        flash('Account created successfully!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Error creating account. Please try again.', 'error')
        return redirect(url_for('sso_signup'))


@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.pop('authenticated', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/')
@require_auth
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
@require_auth
def browse(subpath=''):
    """Alias route for /explorer for backward compatibility."""
    return explorer(subpath)


@app.route('/preview')
@app.route('/preview/<path:filepath>')
@require_auth
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
@require_auth
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
@require_auth
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
@require_auth
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
@require_auth
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
@require_auth
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


@app.route('/rename', methods=['POST'])
@require_auth
def rename_file():
    """Rename a file or folder."""
    filepath = request.form.get('filepath', '')
    new_name = request.form.get('new_name', '').strip()
    
    if not filepath or not new_name:
        return jsonify({'error': 'File path and new name are required'}), 400
    
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
        # Get parent directory
        parent_dir = os.path.dirname(full_path)
        new_path = os.path.join(parent_dir, secure_filename(new_name))
        
        # Check if new name already exists
        if os.path.exists(new_path):
            return jsonify({'error': 'A file or folder with that name already exists'}), 400
        
        # Rename
        os.rename(full_path, new_path)
        return jsonify({'success': True, 'message': 'Renamed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/copy', methods=['POST'])
@require_auth
def copy_file():
    """Copy a file or folder to clipboard (store in session)."""
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
    
    # Store in session (we'll use a simple in-memory store for this)
    # In production, you might want to use Flask sessions
    return jsonify({
        'success': True, 
        'message': 'Copied to clipboard',
        'filepath': filepath,
        'operation': 'copy'
    })


@app.route('/cut', methods=['POST'])
@require_auth
def cut_file():
    """Cut a file or folder to clipboard (store in session)."""
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
    
    return jsonify({
        'success': True, 
        'message': 'Cut to clipboard',
        'filepath': filepath,
        'operation': 'cut'
    })


@app.route('/paste', methods=['POST'])
@require_auth
def paste_file():
    """Paste a copied or cut file/folder to target directory."""
    source_path = request.form.get('source_path', '')
    target_dir = request.form.get('target_dir', '')
    operation = request.form.get('operation', 'copy')  # 'copy' or 'cut'
    
    if not source_path:
        return jsonify({'error': 'Source path is required'}), 400
    
    # Decode URL-encoded paths
    source_path = urllib.parse.unquote(source_path)
    if target_dir:
        target_dir = urllib.parse.unquote(target_dir)
    
    # Construct paths
    source_full = os.path.join(ROOT_DIRECTORY, source_path)
    if target_dir:
        target_full = os.path.join(ROOT_DIRECTORY, target_dir)
    else:
        target_full = ROOT_DIRECTORY
    
    # Security checks
    if not is_safe_path(ROOT_DIRECTORY, source_full):
        return jsonify({'error': 'Invalid source path'}), 403
    if not is_safe_path(ROOT_DIRECTORY, target_full):
        return jsonify({'error': 'Invalid target directory'}), 403
    
    # Check if source exists
    if not os.path.exists(source_full):
        return jsonify({'error': 'Source file or folder does not exist'}), 404
    
    # Check if target is a directory
    if not os.path.isdir(target_full):
        return jsonify({'error': 'Target is not a directory'}), 400
    
    try:
        # Get filename/foldername
        item_name = os.path.basename(source_full)
        dest_path = os.path.join(target_full, item_name)
        
        # Check if destination already exists
        if os.path.exists(dest_path):
            return jsonify({'error': 'A file or folder with that name already exists in the destination'}), 400
        
        if operation == 'cut':
            # Move (rename)
            shutil.move(source_full, dest_path)
            return jsonify({'success': True, 'message': 'Moved successfully'})
        else:
            # Copy
            if os.path.isdir(source_full):
                shutil.copytree(source_full, dest_path)
            else:
                shutil.copy2(source_full, dest_path)
            return jsonify({'success': True, 'message': 'Copied successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/move', methods=['POST'])
@require_auth
def move_file():
    """Move a file or folder to a new location."""
    filepath = request.form.get('filepath', '')
    target_dir = request.form.get('target_dir', '')
    
    if not filepath or not target_dir:
        return jsonify({'error': 'File path and target directory are required'}), 400
    
    # Decode URL-encoded paths
    filepath = urllib.parse.unquote(filepath)
    target_dir = urllib.parse.unquote(target_dir)
    
    # Construct paths
    source_full = os.path.join(ROOT_DIRECTORY, filepath)
    target_full = os.path.join(ROOT_DIRECTORY, target_dir)
    
    # Security checks
    if not is_safe_path(ROOT_DIRECTORY, source_full):
        return jsonify({'error': 'Invalid source path'}), 403
    if not is_safe_path(ROOT_DIRECTORY, target_full):
        return jsonify({'error': 'Invalid target directory'}), 403
    
    # Check if source exists
    if not os.path.exists(source_full):
        return jsonify({'error': 'File or folder does not exist'}), 404
    
    # Check if target is a directory
    if not os.path.isdir(target_full):
        return jsonify({'error': 'Target is not a directory'}), 400
    
    try:
        # Get filename/foldername
        item_name = os.path.basename(source_full)
        dest_path = os.path.join(target_full, item_name)
        
        # Check if destination already exists
        if os.path.exists(dest_path):
            return jsonify({'error': 'A file or folder with that name already exists in the destination'}), 400
        
        # Move
        shutil.move(source_full, dest_path)
        return jsonify({'success': True, 'message': 'Moved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/file_info/<path:filepath>')
@require_auth
def get_file_info_endpoint(filepath=''):
    """Get comprehensive file metadata and information."""
    if not filepath:
        return jsonify({'error': 'File path is required'}), 400
    
    # Decode URL-encoded path
    filepath = urllib.parse.unquote(filepath)
    
    # Construct the full path
    full_path = os.path.join(ROOT_DIRECTORY, filepath)
    
    # Security check
    if not is_safe_path(ROOT_DIRECTORY, full_path):
        return jsonify({'error': 'Invalid path'}), 403
    
    # Check if path exists
    if not os.path.exists(full_path):
        return jsonify({'error': 'File or folder does not exist'}), 404
    
    try:
        import stat
        import platform
        
        # Get comprehensive file statistics
        file_stat = os.stat(full_path)
        file_stat_lstat = os.lstat(full_path) if os.path.islink(full_path) else file_stat
        
        # Basic information
        info = {
            'name': os.path.basename(full_path),
            'full_path': full_path,
            'relative_path': filepath,
            'is_directory': os.path.isdir(full_path),
            'is_file': os.path.isfile(full_path),
            'is_link': os.path.islink(full_path),
            'is_symlink': os.path.islink(full_path),
        }
        
        # If it's a symlink, get the target
        if os.path.islink(full_path):
            try:
                info['symlink_target'] = os.readlink(full_path)
            except:
                info['symlink_target'] = 'Unable to read link target'
        
        # File size information
        if os.path.isfile(full_path):
            info['size_bytes'] = file_stat.st_size
            info['size_formatted'] = format_file_size(file_stat.st_size)
            info['size_kb'] = round(file_stat.st_size / 1024, 2)
            info['size_mb'] = round(file_stat.st_size / (1024 * 1024), 2)
        elif os.path.isdir(full_path):
            # Try to get directory size (may be slow for large directories)
            try:
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(full_path):
                    for filename in filenames:
                        try:
                            total_size += os.path.getsize(os.path.join(dirpath, filename))
                        except:
                            pass
                info['directory_size_bytes'] = total_size
                info['directory_size_formatted'] = format_file_size(total_size)
            except:
                info['directory_size_formatted'] = 'Unable to calculate'
        
        # Timestamps
        info['created'] = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        info['created_timestamp'] = file_stat.st_ctime
        info['modified'] = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        info['modified_timestamp'] = file_stat.st_mtime
        info['accessed'] = datetime.fromtimestamp(file_stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')
        info['accessed_timestamp'] = file_stat.st_atime
        
        # File extension and type
        file_ext = os.path.splitext(full_path)[1].lower()
        info['extension'] = file_ext
        info['extension_without_dot'] = file_ext.lstrip('.')
        info['filename_without_ext'] = os.path.splitext(os.path.basename(full_path))[0]
        
        # MIME type
        mime_type, encoding = mimetypes.guess_type(full_path)
        info['mime_type'] = mime_type or 'unknown'
        info['mime_encoding'] = encoding or 'none'
        
        # File permissions (Unix-style)
        if platform.system() != 'Windows':
            mode = file_stat.st_mode
            info['permissions_octal'] = oct(stat.S_IMODE(mode))
            info['permissions_string'] = stat.filemode(mode)
            
            # Detailed permission breakdown
            info['owner_read'] = bool(mode & stat.S_IRUSR)
            info['owner_write'] = bool(mode & stat.S_IWUSR)
            info['owner_execute'] = bool(mode & stat.S_IXUSR)
            info['group_read'] = bool(mode & stat.S_IRGRP)
            info['group_write'] = bool(mode & stat.S_IWGRP)
            info['group_execute'] = bool(mode & stat.S_IXGRP)
            info['other_read'] = bool(mode & stat.S_IROTH)
            info['other_write'] = bool(mode & stat.S_IWOTH)
            info['other_execute'] = bool(mode & stat.S_IXOTH)
            info['setuid'] = bool(mode & stat.S_ISUID)
            info['setgid'] = bool(mode & stat.S_ISGID)
            info['sticky_bit'] = bool(mode & stat.S_ISVTX)
            
            # Owner and group
            try:
                import pwd
                import grp
                owner = pwd.getpwuid(file_stat.st_uid)
                group = grp.getgrgid(file_stat.st_gid)
                info['owner_name'] = owner.pw_name
                info['owner_id'] = file_stat.st_uid
                info['group_name'] = group.gr_name
                info['group_id'] = file_stat.st_gid
            except:
                info['owner_id'] = file_stat.st_uid
                info['group_id'] = file_stat.st_gid
                info['owner_name'] = 'Unknown'
                info['group_name'] = 'Unknown'
        else:
            info['owner_id'] = file_stat.st_uid
            info['group_id'] = file_stat.st_gid
            info['owner_name'] = 'Unknown'
            info['group_name'] = 'Unknown'
        
        # Inode and device information (Unix)
        if platform.system() != 'Windows':
            info['inode'] = file_stat.st_ino
            info['device'] = file_stat.st_dev
            info['hard_links'] = file_stat.st_nlink
            mode = file_stat.st_mode
            info['device_type'] = file_stat.st_rdev if stat.S_ISCHR(mode) or stat.S_ISBLK(mode) else None
        
        # File type flags
        mode = file_stat.st_mode
        info['is_block_device'] = stat.S_ISBLK(mode) if platform.system() != 'Windows' else False
        info['is_char_device'] = stat.S_ISCHR(mode) if platform.system() != 'Windows' else False
        info['is_fifo'] = stat.S_ISFIFO(mode) if platform.system() != 'Windows' else False
        info['is_socket'] = stat.S_ISSOCK(mode) if platform.system() != 'Windows' else False
        
        # Additional metadata
        info['parent_directory'] = os.path.dirname(full_path)
        info['absolute_path'] = os.path.abspath(full_path)
        info['canonical_path'] = os.path.realpath(full_path)
        
        # Check if file is readable/writable/executable
        info['is_readable'] = os.access(full_path, os.R_OK)
        info['is_writable'] = os.access(full_path, os.W_OK)
        info['is_executable'] = os.access(full_path, os.X_OK)
        
        # File content type detection
        if os.path.isfile(full_path):
            info['is_text'] = False
            info['is_binary'] = False
            try:
                with open(full_path, 'rb') as f:
                    chunk = f.read(512)
                    if chunk:
                        # Check if file contains null bytes (binary indicator)
                        if b'\x00' in chunk:
                            info['is_binary'] = True
                        else:
                            # Try to decode as text
                            try:
                                chunk.decode('utf-8')
                                info['is_text'] = True
                            except:
                                try:
                                    chunk.decode('latin-1')
                                    info['is_text'] = True
                                except:
                                    info['is_binary'] = True
            except:
                pass
        
        # Line count for text files
        if info.get('is_text') and os.path.isfile(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    info['line_count'] = sum(1 for _ in f)
            except:
                try:
                    with open(full_path, 'r', encoding='latin-1', errors='ignore') as f:
                        info['line_count'] = sum(1 for _ in f)
                except:
                    info['line_count'] = 'Unable to count'
        
        # Platform information
        info['platform'] = platform.system()
        info['platform_version'] = platform.version()
        
        return jsonify({'success': True, 'info': info})
    
    except PermissionError:
        return jsonify({'error': 'Permission denied'}), 403
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
@require_auth
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
@require_auth
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


@app.route('/notes/<int:note_id>')
@require_auth
def view_note(note_id):
    """View a note (read-only)."""
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', 
                             error_code=500, 
                             error_message="Database connection failed"), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
        note = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not note:
            abort(404)
        
        return render_template('note_view.html', note=note)
    except Error as e:
        if connection:
            connection.close()
        return render_template('error.html', 
                             error_code=500, 
                             error_message=f"Error fetching note: {str(e)}"), 500


@app.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@require_auth
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
@require_auth
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
    # Ensure users table exists if passkey mode is enabled
    if USE_PASS_KEY:
        ensure_users_table()
    
    # Load server configuration from environment variables
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print("Flask File Explorer")
    print("=" * 60)
    print(f"Root directory: {ROOT_DIRECTORY}")
    print(f"Database: {DB_NAME} @ {DB_HOST}:{DB_PORT}")
    print(f"Environment: {FLASK_ENV}")
    print(f"Authentication: {'Production (Enabled)' if IS_PRODUCTION else 'Development (Disabled)'}")
    if IS_PRODUCTION:
        print(f"Passkey Mode: {'Enabled' if USE_PASS_KEY else 'Disabled (Password)'}")
    print(f"Server starting on http://{SERVER_HOST}:{SERVER_PORT}")
    print("\nTo access from another device:")
    print("1. Find your machine's IP address: hostname -I")
    print(f"2. Open http://<your-ip>:{SERVER_PORT} in a browser")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the Flask app
    # Bind to 0.0.0.0 to allow access from other devices on the network
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=FLASK_DEBUG)


from flask import Flask, render_template, request, redirect, url_for, flash

from modules.filters import Processor
from modules.storage import DatabaseStorage
import json

app = Flask(__name__)
storage = DatabaseStorage()

@app.route('/')
def index():
    searches = storage.get_all_searches()
    return render_template('index.html', searches=searches)

@app.route('/add_search', methods=['GET', 'POST'])
def add_search():
    if request.method == 'POST':
        name = request.form['name']
        search_type = request.form['type']
        notify = 'notify' in request.form

        usernames = []
        keywords = []
        if search_type == 'user':
            usernames = request.form.get('usernames', '').strip()
            usernames = [u.strip() for u in usernames.split(',') if u.strip()]
        else:
            keywords = request.form.get('keywords', '').strip()
            keywords = [k.strip() for k in keywords.split(',') if k.strip()]

        search_data = {
            "name": name,
            "type": search_type,
            "usernames": ', '.join(usernames) if usernames else None,
            "keyword": ', '.join(keywords) if keywords else None,
            "notify": notify
        }
        storage.save_search(search_data)
        flash('Search added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_search.html')

@app.route('/edit_search/<search_id>', methods=['GET', 'POST'])
def edit_search(search_id):
    search = storage.get_search(search_id)
    if not search:
        flash('Search not found!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        search_type = request.form['type']
        notify = 'notify' in request.form

        criteria = {'type': search_type}
        if search_type == 'user':
            usernames = request.form.get('usernames', '').strip()
            criteria['usernames'] = [u.strip() for u in usernames.split(',') if u.strip()]
        else:
            keywords = request.form.get('keywords', '').strip()
            criteria['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]

        search_data = {
            "id": search_id,
            "name": name,
            "type": search_type,
            "keyword": json.dumps(criteria),
            "notify": notify
        }
        storage.save_search(search_data)
        flash('Search updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_search.html', search=search, search_id=search_id)

@app.route('/delete_search/<search_id>')
def delete_search(search_id):
    if storage.delete_search(search_id):
        flash('Search deleted successfully!', 'success')
    else:
        flash('Error deleting search!', 'error')
    return redirect(url_for('index'))

@app.route('/view_matches/<search_id>')
def view_matches(search_id):
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Ensure per_page is either 10 or 20
    if per_page not in [10, 20]:
        per_page = 10

    search = storage.get_search(search_id)
    matches, total_matches = storage.get_matches_paginated(search_id, page=page, per_page=per_page)

    # Calculate total pages
    total_pages = (total_matches + per_page - 1) // per_page

    return render_template('view_matches.html', 
                          search=search, 
                          matches=matches, 
                          page=page, 
                          per_page=per_page,
                          total_matches=total_matches,
                          total_pages=total_pages)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_id = request.form['search_id']
        search = storage.get_search(search_id)

        if search:
            processor = Processor(storage)
            posts = storage.get_all_posts()
            processor.filter_by_search(posts, search)
            return redirect(url_for('view_matches', search_id=search_id))

    searches = storage.get_all_searches()
    return render_template('search.html', searches=searches)

@app.route('/posts')
def posts():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Ensure per_page is either 10 or 20
    if per_page not in [10, 20]:
        per_page = 10

    # Get posts with pagination
    posts, total_posts = storage.get_posts(page=page, per_page=per_page)

    # Calculate total pages
    total_pages = (total_posts + per_page - 1) // per_page

    return render_template('posts.html', 
                          posts=posts, 
                          page=page, 
                          per_page=per_page,
                          total_posts=total_posts,
                          total_pages=total_pages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

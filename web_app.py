from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from modules.storage import DatabaseStorage
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
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
            "keywords": ', '.join(keywords) if keywords else None,
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
            "keywords": json.dumps(criteria),
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
        search_id = int(request.form['search_id'])
        search = storage.get_search(search_id)

        if search:
            matched_post_ids = None
            if search.type == 'user' and search.usernames:
                usernames = search.usernames.split(',')
                matched_post_ids = storage.get_post_ids_by_users(usernames)
            elif (search.type == 'topic' or search.type == 'job') and search.keywords:
                keywords = search.keywords.split(',')
                matched_post_ids = storage.get_post_ids_by_users(keywords)

            if matched_post_ids:
                matches = list(map(lambda post_id: {
                    "search_id": search.id,
                    "post_id": post_id,
                    "matched_at": datetime.now()
                }, matched_post_ids))
                storage.save_matches(search.id, matches, True)

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

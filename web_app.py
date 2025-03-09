from flask import Flask, render_template, request, redirect, url_for, flash
from modules.config_manager import ConfigManager
from modules.storage import Storage
from modules.post_filter import PostFilter
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
config_manager = ConfigManager()
storage = Storage()
post_filter = PostFilter()

def load_sample_posts():
    try:
        with open('sample_posts.json', 'r') as f:
            data = json.load(f)
            return data.get('posts', [])
    except Exception as e:
        print(f"Error loading sample posts: {e}")
        return []

@app.route('/')
def index():
    searches = config_manager.get_all_searches()
    return render_template('index.html', searches=searches)

@app.route('/add_search', methods=['GET', 'POST'])
def add_search():
    if request.method == 'POST':
        name = request.form['name']
        search_type = request.form['type']
        notify = 'notify' in request.form

        criteria = {'type': search_type}
        if search_type == 'user':
            criteria['usernames'] = request.form['usernames'].split(',')
        else:
            criteria['keywords'] = request.form['keywords'].split(',')

        config_manager.add_search(name, criteria, notify)
        flash('Search added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_search.html')

@app.route('/edit_search/<search_id>', methods=['GET', 'POST'])
def edit_search(search_id):
    search = config_manager.get_search(search_id)
    if not search:
        flash('Search not found!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        search_type = request.form['type']
        notify = 'notify' in request.form

        criteria = {'type': search_type}
        if search_type == 'user':
            criteria['usernames'] = request.form['usernames'].split(',')
        else:
            criteria['keywords'] = request.form['keywords'].split(',')

        config_manager.update_search(search_id, name=name, criteria=criteria, notify=notify)
        flash('Search updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_search.html', search=search, search_id=search_id)

@app.route('/delete_search/<search_id>')
def delete_search(search_id):
    if config_manager.delete_search(search_id):
        flash('Search deleted successfully!', 'success')
    else:
        flash('Error deleting search!', 'error')
    return redirect(url_for('index'))

@app.route('/view_matches/<search_id>')
def view_matches(search_id):
    search = config_manager.get_search(search_id)
    matches = storage.get_matches(search_id)
    return render_template('view_matches.html', search=search, matches=matches)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_id = request.form['search_id']
        search = config_manager.get_search(search_id)

        if search:
            posts = load_sample_posts()
            matches = post_filter.filter_posts(posts, search['criteria'])

            # Save matches
            storage.save_matches(search_id, matches)

            # Redirect to view matches
            return redirect(url_for('view_matches', search_id=search_id))

    searches = config_manager.get_all_searches()
    return render_template('search.html', searches=searches)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
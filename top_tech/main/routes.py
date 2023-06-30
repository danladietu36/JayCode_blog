from flask import render_template, request, Blueprint
from top_tech.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('home', strict_slashes=False)
def home():
    page = request.args.get('Page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("about", strict_slashes=False)
def about():
    return render_template('about.html', title='About')
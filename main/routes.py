from flask import Blueprint , render_template,request
from run import Post,db

main=Blueprint('main',__name__)


@main.route('/')
@main.route('/home')
def home():
    db.create_all()
    page=request.args.get('page',1,type=int)
    all_posts = Post.query.paginate(page=page,per_page=2)
    return render_template("index.html", all_blog=all_posts)

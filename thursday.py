from datetime import datetime
import os
import markdown
import shutil
import urllib

from markdown.extensions.codehilite import CodeHiliteExtension
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from slugify import slugify


class PostContext(object):
    def __init__(self, base_dir, title, date, content):
        self.base_dir = base_dir
        self.title = title
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.content = content
    
    def local_path(self):
        return os.path.join(self.base_dir, str(self.date.year), str(self.date.month), str(self.date.day), self.url_safe_title())

    def url_safe_title(self):
        return slugify(self.title) + ".html"

    def post_link_path(self):
        return f'/{self.date.year}/{self.date.month}/{self.date.day}/{self.url_safe_title()}'

    def create_post_directory(self):
        os.makedirs(os.path.dirname(self.local_path()), mode=0o755, exist_ok=True)


class Thursday(object):
    def __init__(self):
        self.source_path='./content'
        self.template_path='./templates'
        self.output_path='./output'
        self.static_path='./static'

        self.md = markdown.Markdown(extensions = ['meta', 'extra', CodeHiliteExtension()], output_format='html5', tab_length=2)
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self.rendered_posts = []

        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

        if os.path.exists(self.static_path):
            os.makedirs(os.path.join(self.output_path, self.static_path))
            for f in os.listdir(self.static_path):
                shutil.copy2(os.path.join(self.static_path, f), os.path.normpath(os.path.join(self.output_path , self.static_path, f)))

    def render_post(self, in_file, template):
        try:
            html = self.md.convert(in_file.read())
            pc = PostContext(self.output_path, self.md.Meta['title'][0], self.md.Meta['date'][0], html)

            pc.create_post_directory()
            with open(pc.local_path(), "w") as f:
                f.write(template.render(post_body=pc.content, title=pc.title, post_date=pc.date))

            self.rendered_posts.append(pc)
        finally:
            self.md.reset()

    def write_posts(self):
        template = self.get_post_template(self.template_path)
        files = os.listdir(self.source_path)
        # TODO: probably need to run through first, rather than render as I go 
        for f in files:
            with open(os.path.join(self.source_path, f)) as input_file:
                self.render_post(input_file, template)

    def write_index(self):
        template = self.get_post_template(self.template_path, 'index.html')
        with open(os.path.join(self.output_path, 'index.html'), 'w') as f:
            f.write(template.render(posts=self.rendered_posts))

    def get_post_template(self, template_path, file='post.html'):
        return self.jinja_env.get_template(file)


if __name__ == "__main__":
    th = Thursday()
    th.write_posts()
    th.write_index()
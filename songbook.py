from datetime import datetime
import os
import shutil
import urllib

from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from slugify import slugify


class SongContext(object):
    def __init__(self, base_dir, title, date, content):
        self.base_dir = base_dir
        self.title = title
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.content = content
    
    def local_path(self):
        return os.path.join(self.base_dir, self.url_safe_title())

    def url_safe_title(self):
        return slugify(self.title) + ".html"

    def post_link_path(self):
        return f'/{self.url_safe_title()}'

    def create_song_directory(self):
        os.makedirs(os.path.dirname(self.local_path()), mode=0o755, exist_ok=True)


class Songbook(object):
    def __init__(self):
        self.source_path='./content'
        self.template_path='./templates'
        self.output_path='./output'
        self.static_path='./static'

        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self.source_files = os.listdir(self.source_path)

        self.rendered_posts = []

        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

        if os.path.exists(self.static_path):
            os.makedirs(os.path.join(self.output_path, self.static_path))
            for f in os.listdir(self.static_path):
                shutil.copy2(os.path.join(self.static_path, f), os.path.normpath(os.path.join(self.output_path , self.static_path, f)))

    def render_song(self, in_file, template):
        html = in_file.read()
        ctx = SongContext(self.output_path, self.md.Meta['title'][0], self.md.Meta['date'][0], html)

        ctx.create_song_directory()
        with open(ctx.local_path(), "w") as f:
            f.write(template.render(post_body=ctx.content, title=ctx.title, post_date=ctx.date))

        self.rendered_posts.append(ctx)

    def write_songs(self):
        template = self.get_template(self.template_path, file='song.html')
        # TODO: probably need to run through first, rather than render as I go 
        for f in self.source_files:
            with open(os.path.join(self.source_path, f)) as input_file:
                self.render_song(input_file, template)

    def write_index(self):
        template = self.get_template(self.template_path, 'index.html')
        with open(os.path.join(self.output_path, 'index.html'), 'w') as f:
            f.write(template.render(posts=self.rendered_posts))

    def get_template(self, template_path, file='post.html'):
        return self.jinja_env.get_template(file)


if __name__ == "__main__":
    th = Songbook()
    th.write_songs()
    th.write_index()

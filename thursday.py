from datetime import datetime
import os
import markdown
import urllib
from markdown.extensions.codehilite import CodeHiliteExtension
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape


class SiteContext(object):
    pass


class PostContext(object):
    def __init__(self, title, date, content):
        self.title = title
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.content = content
    
    def local_path(self):
        return os.path.join(str(self.date.year), str(self.date.month), str(self.date.day), self.url_safe_title())

    def url_safe_title(self):
        pass

    def post_link_path(self):
        pass


class Thursday(object):
    def __init__(self):
        self.source_path='./content'
        self.template_path='./templates'
        self.output_path='./output'

        self.md = markdown.Markdown(extensions = ['meta', 'extra', CodeHiliteExtension()], output_format='html5', tab_length=2)
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render_post(self, in_file, template, out_file):
        try:
            html = self.md.convert(in_file.read())
            print(template.render(post_body=html, title=self.md.Meta['title'][0], post_date=self.md.Meta['date'][0]))
        finally:
            self.md.reset()

    def load_posts(self):
        template = self.get_post_template(self.template_path)
        files = os.listdir(self.source_path)
        for f in files:
            with open(os.path.join(self.source_path, f)) as input_file:
                self.render_post(input_file, template, None)

    def get_post_template(self, template_path):
        return self.jinja_env.get_template('post.html')


if __name__ == "__main__":
    th = Thursday()
    th.load_posts()
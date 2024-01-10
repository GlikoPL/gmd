from pathlib import Path
import markdown
import pathlib
import os
import shutil

class Gmd:  
    def __init__(self, output_path, template_path, input_path):
        self.output_path = output_path
        template_file = open(template_path, 'r')
        self.template_str = template_file.read()
        template_file.close()
        self.input_path = input_path
        self.markdown = markdown.Markdown(
            extensions=['mdx_truly_sane_lists', 'mdx_breakless_lists'],
            output_format='html')
        if not output_path.exists():
            os.mkdir(output_path)
        
    def run(self):
        if (self.input_path / 'index.html').exists():
            shutil.copyfile(self.input_path / 'index.html', self.output_path / 'index.html')
        self.process_dir(Path(''))  

    def process_dir(self, dir):
        real_dir = self.input_path / dir
        real_out_dir = self.output_path / dir
        if not real_out_dir.exists():
            os.mkdir(real_out_dir)
        if real_dir == self.output_path:
            return
        files = os.listdir(real_dir)
        for file in files:
            if os.path.isfile(real_dir / file):
                fpath = Path(file)
                if fpath.suffix == '.md':
                    self.process_file(real_dir / fpath, real_out_dir / f'{fpath.stem}.html', (dir / f'{fpath.stem}.html').as_posix())
            else:
                self.process_dir(Path(dir / file))
        
    def process_file(self, input_path, output_path, web_path):
        print(f'Processing: {input_path}')
        in_text = open(input_path, 'r').read()
        in_text = in_text.replace('.md)', '.html)')
        process_text = self.markdown.convert(in_text)
        html_text = self.template_str
        
        if 'pl/' in web_path:
            html_text = html_text.replace('[GMD_PL]', 'Polski')
            html_text = html_text.replace('[GMD_EN]', 'Angielski')
            html_text = html_text.replace('[GMD_LINK_PL]', f'/{web_path}')
            html_text = html_text.replace('[GMD_LINK_EN]', web_path.replace('pl/', '/en/'))
        elif 'en/' in web_path:
            html_text = html_text.replace('[GMD_PL]', 'Polish')
            html_text = html_text.replace('[GMD_EN]', 'English')
            html_text = html_text.replace('[GMD_LINK_PL]', web_path.replace('en/', '/pl/'))
            html_text = html_text.replace('[GMD_LINK_EN]', f'/{web_path}')
        
        html_text = html_text.replace('[GMD_CONTENT]', process_text)
        open(output_path, 'w').write(html_text)

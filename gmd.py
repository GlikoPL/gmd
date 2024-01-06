from pathlib import Path
import markdown
import os
import shutil
import re

class Gmd:  
    def __init__(self, output_path, template_path, input_path, langs):
        self.output_path = output_path
        template_file = open(template_path, 'r')
        self.template_str = template_file.read()
        template_file.close()
        self.input_path = input_path
        self.markdown = markdown.Markdown(
            extensions=['mdx_truly_sane_lists', 'mdx_breakless_lists'],
            output_format='html')
        self.langs = langs
        if not output_path.exists():
            os.mkdir(output_path)
        for l in self.langs:
            if not (output_path / l).exists():
                os.mkdir(output_path / l)
        
    def run(self):
        if (self.input_path / 'index.html').exists():
            shutil.copyfile(self.input_path / 'index.html', self.output_path / 'index.html')
        for l in self.langs:
            self.process_dir(Path(''), l)
        
    def is_lang(self, lang):
        for l in self.langs:
            if l == lang: return True
        return False
        
    def process_dir(self, dir, lang):
        real_dir = self.input_path / dir
        real_out_dir = self.output_path / dir / lang
        files = os.listdir(real_dir)
        for file in files:
            if os.path.isfile(real_dir / file):
                fpath = Path(file)
                if fpath.suffix == '.md':
                    self.process_file(real_dir / fpath, real_out_dir / f'{fpath.stem}.html', lang)
            else:
                if dir.name == '':
                    if not self.is_lang(file):
                        self.process_dir(Path(dir / file), lang)
                else:
                    self.process_dir(Path(dir / file), lang)
        
    def find_gmd_match(self, text : str, type):
        output = []
        start = 0
        match_str = f'[{type}:'
        while True:
            result = text.find(match_str, start)
            if result == -1:
                return output
            else:
                result2 = text.find(']', result + len(match_str))
                if result2 != -1:
                    substr = text[result:(result2 + 1)]
                    value = substr[len(match_str):(result2 - result)]
                    tuple = (substr, value)
                    output.append(tuple)
                    start = result2
                else:
                    return output
        
    def process_file(self, input_path, output_path, lang):
        print(f'Processing: {input_path}')
        in_text = open(input_path, 'r').read()
        # results = re.findall('\[GMD_INCLUDE:(.*?)\]', in_text)
        
        include_matches = self.find_gmd_match(in_text, 'GMD_INCLUDE')
        for match in include_matches:
            print(match[0])
            print(match[1])
            include_path = (self.input_path / lang / f'{match[1]}.md')
            include_text = open(include_path, 'r').read()
            in_text = in_text.replace(match[0], include_text)
        
        process_text = self.markdown.convert(in_text)
        html_text = self.template_str.replace('[GMD_CONTENT]', process_text)
        open(output_path, 'w').write(html_text)

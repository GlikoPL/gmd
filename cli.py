from argparse import ArgumentParser
from pathlib import Path
import gmd

def parser() -> ArgumentParser:
    parser = ArgumentParser(
        description='Gliko Markdown Deployer'
    )
    parser.add_argument('-t', '--template', type=lambda s: Path(s), default='template.html',
                        help='path to html template')
    parser.add_argument('-o', '--output', type=lambda s: Path(s), default='out',
                        help='path to output folder')
    parser.add_argument('-i', '--input', type=lambda s: Path(s), default='',
                        help='path to input folder')
    
    return parser
    
def main() -> None:
    args = parser().parse_args()
    gmd_ctx = gmd.Gmd(args.output, args.template, args.input)
    gmd_ctx.run()
    print('Successfull deployment')

main()

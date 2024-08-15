import pathlib

def get_script_path(script_name: str) -> str:
    src_dir = pathlib.Path( __file__ ).parent.parent.resolve()
    return pathlib.Path( src_dir, 'scripts', script_name ).resolve()
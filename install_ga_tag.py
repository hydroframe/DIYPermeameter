"""
    Install a Google Analytics 4 tag into the installed Streamlit package of the virtual environment.
    Streamlit does not have a supported way to use Google Analytics tags. This
    inserts the Google Analytics tag into the HTML <head> tag of the index.html file of streamlit installed package.

    Usage:
        python install_ga_tag.py GA-000000000
    Pass the GA tag of the GA project to track DIYPermeameter.
    Make sure the python virtual environment being used is a VM private to DiyPermeameter and not
    a shared common virtual environment.
"""
import sys
import pathlib
import streamlit as st

def main():
    """Main routine to update the steamlit package of the python virtual environment"""

    ga_tag = sys.argv[1] if len(sys.argv) > 1 else None
    if ga_tag is None or "GA-" not in ga_tag:
        print("You must specify a google analytics tag in the form GA-xxxxxxx")
        return
    ga_script = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script id='google_analytics'>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '{ga_tag}');
    </script>
    """

    ga_script = ga_script.replace("{ga_tag}", ga_tag)
    
    path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    if "miniconda3" in str(path):
        print(f"Streamlit is installed a virtual environment in '{st.__file__}'.")
        print("You must use a DIYPermeameter specific python virtual environment for the GA- tag.")
        return
    contents = None
    with open(path, "r") as fp:
        contents = fp.read()
        if "googletagmanager" in contents:
            print("Streamlit package already contains GA tag")
            return
        contents = contents.replace("<head>", f"<head>{ga_script}")
    if contents:
        with open(path, "w") as fp:
            fp.write(contents)
            print(f"Updated streamlit package in '{path}'")

if __name__ == "__main__":
    main()
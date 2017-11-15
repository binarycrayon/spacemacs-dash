## Spacemacs docs for Dash.app

Package contribute to https://github.com/Kapeli/Dash-User-Contributions

### Requirement:
 * emacs + orgmode
 * python3 + bs4 (BeautifulSoup4)

### Steps to get doc source files
 * wget https://github.com/syl20bnr/spacemacs/archive/master.zip
 * unzip master.zip
 * pushd spacemacs-master/doc; for i in *.org; do emacs $i --batch -f org-html-export-to-html --kill; done; popd >>/dev/null
 * cp -r spacemacs-master/doc Spacemacs.docset/Contents/Resources/Documents/
 * python3 spacemacsdoc2set.py
 
### Icon assets:
 * http://spacemacs.org/favicons/favicon-16x16.png
 * http://spacemacs.org/favicons/favicon-32x32.png

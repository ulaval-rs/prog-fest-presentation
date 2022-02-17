if [ -d "./reveal.js" ]
then
    echo "reveal.js exists."
else
    echo "Downloading reveal.js"
    git clone https://github.com/hakimel/reveal.js
fi

cp my-theme.css ./reveal.js/dist/theme/my-theme.css

jupyter nbconvert presentation.ipynb \
  --to slides --no-prompt \
  --reveal-prefix reveal.js \
  --SlidesExporter.reveal_theme=my-theme \
  --SlidesExporter.reveal_scroll=False

echo '\n\nexport CAIRO_PATH="${CAIRO_PATH:+"$CAIRO_PATH:"}"${PWD}/lib:${PWD}' >> bin/activate
echo 'export CAIRO_PATH="${CAIRO_PATH}":${PWD}/libext' >> bin/activate
echo 'export PYTHONPATH="${PYTHONPATH:+"$PYTHONPATH:"}${PWD}/scripts"' >> bin/activate

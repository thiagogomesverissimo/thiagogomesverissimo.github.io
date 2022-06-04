# Instructions

Debian:

    sudo apt-get install libxml2-dev libxslt-dev build-essential libxml2 libxml2-dev libxslt1-dev
    gem install bundler

## To run locally 

 - Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
 - Run `bundle clean` to clean up the directory (no need to run `--force`)
 - Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.
 - Run `JEKYLL_ENV=development bundle exec jekyll serve` to generate the HTML and serve it from `localhost:4000` the local server will automatically rebuild and refresh the pages on change.

Drafts:

    JEKYLL_ENV=development bundle exec jekyll serve --drafts

Forked from: https://github.com/academicpages/academicpages.github.io

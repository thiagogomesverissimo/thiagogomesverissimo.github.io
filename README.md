# Instructions

Debian:

    sudo apt-get install libxml2-dev libxslt-dev build-essential libxml2 libxml2-dev libxslt1-dev ruby-dev ruby-bundler nodejs
    sudo gem install bundler

## To run locally 

    bundle config set --local path 'vendor/bundle'
    bundle install
    bundle exec jekyll serve

Dev:

    JEKYLL_ENV=development bundle exec jekyll serve

Drafts:

    JEKYLL_ENV=development bundle exec jekyll serve --drafts

Forked from: https://github.com/academicpages/academicpages.github.io


# Instructions

## To run locally 

 - Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
 - Run `bundle clean` to clean up the directory (no need to run `--force`)
 - Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.
 - Run `JEKYLL_ENV=development bundle exec jekyll serve` to generate the HTML and serve it from `localhost:4000` the local server will automatically rebuild and refresh the pages on change.

Debian:

    gem i bundler -v 1.17.3

Drafts:

    JEKYLL_ENV=development bundle exec jekyll serve --drafts


Forked from: https://github.com/academicpages/academicpages.github.io


``mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

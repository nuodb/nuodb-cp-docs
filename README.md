# nuodb-cp-docs

[![Build status](https://dl.circleci.com/status-badge/img/gh/nuodb/nuodb-cp-docs/tree/main.svg?style=svg&circle-token=CCIPRJ_5tty7eRh1TFHKvrtmiFdMm_2a61931164e7b88e933260a7edea62bad68f5176)](https://dl.circleci.com/status-badge/redirect/gh/nuodb/nuodb-cp-docs/tree/main)

This repository contains all of the code and content for NuoDB DBaaS Control Plane Software [documentation](https://nuodb.github.io/nuodb-cp-docs/).

## Suggest a Change

If you notice an issue with our documentation or would like to propose a documentation improvement the easiest way to make an impact is to create GitHub [issue](https://github.com/nuodb/nuodb-cp-docs/issues/new).

GitHub issues are triaged by NuoDB team promptly.
An additional information may be requested by th team to make sure that the issue is address in the best possible way.
Once an issue is addressed, you'll get a notification via GitHub that the issue has been closed and that a change is now live.

## Contribute

Any contributions to NuoDB DBaaS Control Plane documentation are welcome.
Feel free to make in impact and contribute directly by creating a [Pull request](https://github.com/nuodb/nuodb-cp-docs/compare) to this repository with your suggested changes.
To do so:

1. Fork the repository
2. Create branch of of `main` branch
3. Make you changes in that branch
4. Submit PR for a review with `nuodb-cp-docs/main` as a target branch

Once you have submitted your PR, CircleCI will build, verify and upload a staging version of the website with your changes.

Every update to the `main` branch of this repository will trigger a rebuild of our production documentation page.
It might take a few moments for your merged changes to appear.

## Project structure

This project follows [Thulite](https://docs.thulite.io/basics/project-structure/) and [Hugo](https://gohugo.io/getting-started/directory-structure/) project structure.
[Doks](https://getdoks.org/docs/basics/project-structure/) documentation theme for [Thulite](https://docs.thulite.io/getting-started/) framework empowers the look and feel for our documentation.

- `assets` - Project assets (scripts, styles, images, etc.)
- `config` - Project’s configuration files (Thulite, Hugo, PostCSS, etc.)
- `content` - Project content (pages, posts, etc.)
- `layouts` - Project layouts (partials, shortcodes, etc.)
- `static` - Non-code, unprocessed assets (fonts, icons, samples, etc.)
- `package.json` - A project manifest.

If you're working on a change in docs content, you should work primarily in `content/docs` directory.

## Build the docs locally

If you want to contribute documentation content, we recommend building and testing the change locally.

### Prerequisites

- [Hugo](https://gohugo.io/installation/) v0.132 or later
- [Node.js](https://nodejs.org/en/download/package-manager) v12.16.2 or later

### Authoring Content

Most of the documentation content is written using [Markdown](https://daringfireball.net/projects/markdown/) syntax with a [front-matter](https://gohugo.io/content-management/front-matter/) to define metadata such as title and description.
Please read the [Doks theme](https://getdoks.org/docs/basics/authoring-content/) documentation for available shortcodes and Markdown visualization features.

### Local Development

To serve a local version of the docs site with your changes, run:

```sh
npm run dev
```

This command both builds and serves your local changes.
By default, your local build is accessible at [localhost:1313](http://localhost:1313/).
From here, any changes you save in your text editor will render on this local site in real time.

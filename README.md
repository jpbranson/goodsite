# Joseph Branson's website

This is an R **blogdown** site using **Hugo** and the bundled `hugo-lithium`
theme. Open `My website.Rproj` in RStudio to work on it.

## How the site is built

There are two steps:

1. blogdown knits an `.Rmd` source into an `.html` file beside it, running any R
   code in that post. Both files belong in the repository.
2. Hugo combines those HTML files (and any plain `.md` pages) with the theme and
   configuration to generate the finished website in `public/`.

Edit the `.Rmd` source, then render it; do not write posts in the generated HTML
or in `public/`. Plain Markdown posts can be edited directly in their `.md` file
and do not need the R knitting step.

## Folder map

| Path | Purpose |
| --- | --- |
| `content/post/` | All blog posts. Put new posts here, using one folder per post. |
| `content/about.md` | The standalone About page, linked as “jpbranson” in the navigation. |
| `layouts/home.html` | The home page template. Lists all published pages in the `post` section, newest first, grouped by year. |
| `layouts/shortcodes/` | Small templates used inside posts, including the existing video and blogdown link helpers. |
| `themes/hugo-lithium/` | The site's theme: layouts, styles, fonts, and default images. Its `exampleSite/` contains samples, not your posts. Put new layout customizations in the top-level `layouts/` folder. |
| `static/` | Shared files copied directly to the finished site. For example, `static/map.html` becomes `/map.html`. Also contains existing widget libraries and PDFs. |
| `blogdown/` | Generated support files, currently cached R results from an older post. This is not a place to write posts. |
| `config.toml` | Hugo settings: site title, theme, menu links, URL rules, and files to ignore. |
| `.Rprofile` | Project defaults for blogdown: your author name, `.Rmd` posts, the `post` directory, and one folder per new post. Restart the R session after editing it. |
| `index.Rmd` | RStudio/blogdown project marker. Despite its name, this does not contain the home page or a post. Leave it in place. |
| `public/` | Generated website, ignored by Git. Build output for publishing; changes here are overwritten by later builds. |
| `.hugo_build.lock` | Hugo's build lock file; not content to edit. |

The older posts use pairs such as `content/post/OCLC-API-blogpost.Rmd` and
`OCLC-API-blogpost.html`. That layout still works. New posts use a **page bundle**:
a folder with an `index.Rmd`, its generated `index.html`, and any images or data
used by that post. There is no need to convert the older posts to start writing.

## Create a post

From the R console with this project open:

```r
blogdown::new_post("My next post", slug = "my-next-post")
```

The project defaults create a structure like this (with today's date):

```text
content/post/2026-09-10-my-next-post/
  index.Rmd        # write your text and R code here
  index.html       # generated when the Rmd is rendered
  photo.jpg        # optional image used only by this post
  data.csv         # optional data used only by this post
  index_files/     # generated figures/widgets, if the post needs them
```

You can also use RStudio's **New Post** addin. Keep the subdirectory as `post`
(singular). For a post with no R code, use
`blogdown::new_post("My next post", slug = "my-next-post", ext = ".md")`.

The metadata between the opening `---` lines controls the post's title, date,
URL, tags, and draft status. For example:

```yaml
---
title: "My next post"
author: "Joseph Branson"
date: '2026-09-10'
slug: my-next-post
draft: true
tags:
  - R
---
```

Use the actual intended publication date. Set `draft: false` (or remove the
`draft` line) when ready. Normal publishing builds omit drafts and future-dated
posts; local blogdown previews show them. Avoid copying a `build: ... never`
block into a new post: those settings prevent a page from appearing even in a
normal local preview.

Put a post-specific image beside `index.Rmd` and reference it as
`![Description of the image](photo.jpg)`. Keep files shared across posts in
`static/`, and link to them from the site root, for example `[Map](/map.html)`.
Bundle resources may be published with the post, so use that folder only for
files intended to accompany the public article.

## Preview and build

Start the local preview from the project root:

```r
blogdown::serve_site()
```

Leave it running while you write. Saving an `.Rmd` recompiles that post and
refreshes the preview. You can also use RStudio's **Knit** button on the post.

Before publishing, render the post you changed and build the production output:

```r
blogdown::build_site(
  build_rmd = "content/post/2026-09-10-my-next-post/index.Rmd"
)
```

Replace that example path with your post's actual path. For a layout change,
plain Markdown changes, or posts whose HTML is already up to date, use:

```r
blogdown::build_site()
```

The default build reuses existing rendered HTML. Avoid `build_rmd = TRUE` unless
you intend to rerun **every** R Markdown file: some older posts depend on data
files or external services from the original analysis. Keeping their generated
HTML lets Hugo publish them without rerunning that code.

Review `public/index.html` through a local server and check the post's link.
Commit the source, its rendered HTML, and required images/widget dependencies;
`public/` is deliberately ignored. Publish through your existing hosting
workflow. This repository does not currently include a deployment configuration,
and a local build alone does not update the live site.

If setting up another computer, install R, RStudio, and the blogdown package
(`install.packages("blogdown")`), then install Hugo with
`blogdown::install_hugo()`. Knitting an R post also needs Pandoc (included with
RStudio) and any R packages used by that particular post.

## Home page repair

The old theme used `.Data.Pages` on the home page. That collection contained the
`Posts` section, so the archive displayed a year and a single “Posts” link. The
home template now selects `.Site.RegularPages` from the `post` section instead.
The existing **Posts** navigation link already points to `/`.

All five posts now belong to that section:

- “back in the saddle” — its `build` settings that disabled rendering and
  listing were removed from both source and generated HTML, and its slug is
  explicitly `back-in-the-saddle`.
- “OAW City App Demo”
- “OCLC API Project”
- “Clips Collection” — moved into `content/post/`, with
  `url: /clips-collection/` to preserve its existing address.
- “Test Post”

The section archive also remains available at `/post/` (singular), and About
remains a standalone page. The `post = "/:year/:slug/"` setting in `config.toml`
means a new post with date `2026-09-10` and slug `my-next-post` has the address
`/2026/my-next-post/`. The folder's date prefix is for organization; the metadata
determines the published date and URL.

`config.toml` also allows generated `_files/` folders so figures and widgets in
new page bundles can be published. R Markdown sources and R caches remain
excluded from Hugo's content processing.

## References

- [blogdown: creating posts](https://pkgs.rstudio.com/blogdown/reference/hugo_cmd.html)
- [blogdown: local preview](https://pkgs.rstudio.com/blogdown/reference/serve_site.html)
- [blogdown: building and selectively knitting posts](https://pkgs.rstudio.com/blogdown/reference/build_site.html)
- [blogdown: page bundle defaults and generated resources](https://pkgs.rstudio.com/blogdown/news/index.html)
- [Hugo: regular pages](https://gohugo.io/methods/site/regularpages/)
- [Hugo: page build options](https://gohugo.io/content-management/build-options/)

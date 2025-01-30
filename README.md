# simple-site-localhoster

This Python app sets up a static server serving your website. It is designed to be simple yet flexible.

## Current support

This app currently only has support for frontends (HTML, CSS, JS).

Backend & database support is not planned, but may come at a later date.

Unbuilt projects (aka a directory containing files belonging to a web framework, such as .astro, .vue, or similar) will never be supported due to the sheer magnitude that requires.
Please build the sites using your framework's build functionality.

## Why?

Despite this seeming relatively useless at first, there are some use cases for it where it could be necessary or more convenient over traditional methods.

### For beginner web developers

Most beginner web developers start out with basic HTML, CSS stylesheets and JavaScript. However, references to them can be broken, especially when separating the CSS styles & JS scripts off to another file.

This app allows them to test their creations in a local environment similar to most online web servers.

### For advanced web developers

Most people in this category use a framework to make their sites (e.g. Astro, React, Preact, Nuxt, Vue, Svelte, Solid, Alpine, etc...) which already comes with a preview server built in.
However, they still require their preview/production servers to have the relevant software installed, and it can also be a hassle to try and work with coworkers who might not have the necessary modules installed (example: backend workers needing to test functionality of frontends).

This app allows everyone to have the same experience as long as each person has a copy of the built site.

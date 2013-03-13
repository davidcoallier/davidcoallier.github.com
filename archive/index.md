---
layout: page
title: Dave on Data
tagline: The Beauty of Data Science and Mathematics 
---
{% include JB/setup %}

## Writings

<ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>



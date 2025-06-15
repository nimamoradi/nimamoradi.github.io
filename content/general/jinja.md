Title: A look at Jinja templates
Date: 2025-02-16
Tags: Python,Jinja, templates, Nima Moradi
Category: Guide
Summary: Some examples of Jinja templates using for loop and if

# A look at Jinja templates
Just started playing around with Jinja2 templates, and I have to say—it’s pretty cool. I knew it could be used to fill in variables, kind of like Python string formatting, but what really surprised me was that you can also include basic logic like loops and conditionals right inside the template.

I was using it with LaTeX, but really, it works with anything—HTML, Markdown, or even plain text.

For example, say you want to generate a structured section dynamically by looping through a list:

```python

{% for entry in items %}
\section{ {{ entry.title }} }  
  \textbf{ {{ entry.subtitle }} } \hfill {{ entry.date }}  

  {{ entry.description }}
{% endfor %}
```

And if you need to conditionally display something, like only showing a special note if it exists:
```python
{% if entry.note %}
  \textit{Note: {{ entry.note }}}
{% endif %}
```

To use this, you just pass a dictionary to the template renderer:
```python
from jinja2 import Template

template_str = """{% for entry in items %}
\\section{ {{ entry.title }} }  
  \\textbf{ {{ entry.subtitle }} } \\hfill {{ entry.date }}  

  {{ entry.description }}

  {% if entry.note %}
    \\textit{Note: {{ entry.note }}}
  {% endif %}
{% endfor %}"""

data = {
    "items": [
        {"title": "Education", "subtitle": "B.Sc. Computer Science", "date": "2020-2024", "description": "Studied at XYZ University", "note": "Graduated with honors"},
        {"title": "Work Experience", "subtitle": "Software Engineer", "date": "2024-Present", "description": "Working at ABC Corp"},
    ]
}

template = Template(template_str)
output = template.render(data)

print(output)
```

This will generate properly formatted LaTeX (or whatever format you're using). It makes it really easy to automate document generation without writing complex logic outside the template.

If you've used Jinja2 before, what’s the most interesting way you've applied it?
(you can  comment on my Medium)
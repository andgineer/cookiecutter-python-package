# {{ cookiecutter.package_name }}

{{ cookiecutter.package_description }} 
{% if cookiecutter.pyproject %}

### Advanced

Use 
```bash
{{ cookiecutter.package_name }} --help
```
to see all available options.

!!! info "About"
    ![About](images/about.jpg)
    [About][{{ cookiecutter.project_slug }}.__about__]
{% endif %}

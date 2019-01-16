This administration app overrides some of Django's admin site.
Therefore, the templates/admin directory cannot be named templates/administration,
because Django is looking for an "admin" directory for overriding admin templates.
However, the static/administration/css directory cannot be named static/admin/css,
because Django provides static files for its admin package under static/admin/css.
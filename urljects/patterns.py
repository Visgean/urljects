
beginning = r'^'
end = r'$'

slug = r'(?P<slug>[\w-]+)'
pk = '(?P<pk>\d+)'
uuid4 = '(?P<uuid4>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'  # noqa

SEPARATOR = '/'  # separator for parts of the url

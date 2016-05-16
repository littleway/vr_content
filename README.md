just keep on fighting
# vr_content
crawl vr content


usage:
command line example: crawl movie -o movie_result -t csv --logfile=log
"movie" is the spider member varibale name's value.
you can choose the spider to crawl by spider's name, like "movie", "android_app" and so on.

item export:
change FIELDS_TO_EXPORT in setting.py if you want to export specified fields
or remember change it if you choose different spider


code description:
we have base class VrItem and ItemSpider because the app and movie html have some same fields and same processes
so we abstract VrItem and ItemSpider for clean code looking

